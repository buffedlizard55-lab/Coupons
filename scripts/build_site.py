#!/usr/bin/env python3
"""Build the published dataset and the static GitHub Pages site.

Inputs (all committed to the repository):
    data/meta.json            taxonomy, verification policy, dataset metadata
    data/entries/*.json       curated entry shards

Outputs:
    data/coupons.json         merged dataset (machine readable, for reuse)
    assets/data/coupons.js    the same dataset as a JS global, so the site works
                              from file:// as well as from GitHub Pages
    _site/                    deployable copy of the site (git-ignored)

The build is deliberately dumb: it merges, validates lightly, computes summary
statistics and copies files. It never invents, rewrites or "improves" offer
text. Every string that describes an offer comes from a shard file, which in
turn quotes an official source.

Usage:
    python3 scripts/build_site.py            # build in place + _site
    python3 scripts/build_site.py --check    # exit non-zero if outputs are stale
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
ENTRIES_DIR = DATA / "entries"
ASSETS_DATA = ROOT / "assets" / "data"
SITE_DIR = ROOT / "_site"

# Shards whose entries use the "excluded / rejected" schema instead of the offer schema.
EXCLUDED_SHARDS = {"10-excluded-unverified.json"}

REQUIRED_ENTRY_FIELDS = (
    "id",
    "title",
    "merchant",
    "publisher",
    "categories",
    "deal_types",
    "offer_text",
    "expires",
    "bay_area",
    "sources",
    "verification",
    "flags",
)
REQUIRED_EXCLUDED_FIELDS = (
    "id",
    "merchant",
    "claim",
    "status",
    "why_rejected",
    "urls_checked",
    "risk",
    "what_would_verify_it",
)


def load_json(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate(meta: dict, entries: list[dict], excluded: list[dict]) -> list[str]:
    """Return a list of human-readable problems. Empty list means the data is sound."""
    problems: list[str] = []
    known_categories = {c["id"] for c in meta["categories"]}
    known_deal_types = {d["id"] for d in meta["deal_types"]}
    known_levels = set(meta["verification"]["levels"])
    known_methods = set(meta["verification"]["methods"])
    known_severities = set(meta["flag_severities"])

    seen_ids: set[str] = set()

    for entry in entries:
        where = entry.get("id", "<missing id>")
        for field in REQUIRED_ENTRY_FIELDS:
            if field not in entry:
                problems.append(f"{where}: missing required field '{field}'")
        if where in seen_ids:
            problems.append(f"{where}: duplicate id")
        seen_ids.add(where)

        for cat in entry.get("categories", []):
            if cat not in known_categories:
                problems.append(f"{where}: unknown category '{cat}'")
        for dt in entry.get("deal_types", []):
            if dt not in known_deal_types:
                problems.append(f"{where}: unknown deal_type '{dt}'")

        level = entry.get("verification", {}).get("level")
        if level not in known_levels:
            problems.append(f"{where}: unknown verification level '{level}'")
        if not entry.get("verification", {}).get("verified_at"):
            problems.append(f"{where}: verification.verified_at is empty")
        checks = entry.get("verification", {}).get("checks") or []
        if not checks:
            problems.append(f"{where}: verification.checks is empty \u2014 nothing documents how this was checked")

        sources = entry.get("sources") or []
        if not sources:
            problems.append(f"{where}: no sources \u2014 an offer without a citation is not allowed")
        for src in sources:
            for field in ("url", "publisher", "accessed", "method", "evidence"):
                if not src.get(field):
                    problems.append(f"{where}: source missing '{field}'")
            if not str(src.get("url", "")).startswith(("http://", "https://")):
                problems.append(f"{where}: source url is not an absolute URL")
            if src.get("method") not in known_methods:
                problems.append(f"{where}: unknown source method '{src.get('method')}'")

        for flag in entry.get("flags") or []:
            if flag.get("severity") not in known_severities:
                problems.append(f"{where}: flag severity '{flag.get('severity')}' is unknown")
            if not flag.get("code") or not flag.get("detail"):
                problems.append(f"{where}: flag is missing code or detail")

        expires = entry.get("expires")
        if expires is not None:
            try:
                _dt.date.fromisoformat(expires)
            except ValueError:
                problems.append(f"{where}: expires '{expires}' is not ISO-8601 (YYYY-MM-DD)")

        bay = entry.get("bay_area") or {}
        if "available" not in bay or "confidence" not in bay:
            problems.append(f"{where}: bay_area is missing 'available' or 'confidence'")

        # Guard against unfinished work shipping to the public site.
        blob = json.dumps(entry, ensure_ascii=False)
        for token in ("TODO", "TBD-fill", "FIXME", "lorem ipsum", "XXX", "PLACEHOLDER"):
            if token in blob:
                problems.append(f"{where}: contains the unfinished-work marker '{token}'")

    for item in excluded:
        where = item.get("id", "<missing id>")
        for field in REQUIRED_EXCLUDED_FIELDS:
            if field not in item:
                problems.append(f"{where}: excluded item missing required field '{field}'")
        if where in seen_ids:
            problems.append(f"{where}: duplicate id")
        seen_ids.add(where)
        if not item.get("urls_checked"):
            problems.append(f"{where}: excluded item has no urls_checked \u2014 rejection must be evidenced")

    return problems


def summarise(meta: dict, entries: list[dict], excluded: list[dict]) -> dict:
    from collections import Counter

    cat_counts: Counter[str] = Counter()
    for entry in entries:
        for cat in entry.get("categories", []):
            cat_counts[cat] += 1

    level_counts: Counter[str] = Counter()
    for entry in entries:
        level_counts[entry.get("verification", {}).get("level", "?")] += 1

    severity_counts: Counter[str] = Counter()
    flag_codes: Counter[str] = Counter()
    for entry in entries:
        for flag in entry.get("flags") or []:
            severity_counts[flag.get("severity", "?")] += 1
            flag_codes[flag.get("code", "?")] += 1

    dated = [e for e in entries if e.get("expires")]
    publishers = sorted({s["publisher"] for e in entries for s in e.get("sources", [])})
    domains = sorted({s["url"].split("/")[2] for e in entries for s in e.get("sources", []) if "://" in s.get("url", "")})

    return {
        "entry_count": len(entries),
        "excluded_count": len(excluded),
        "entries_by_category": dict(cat_counts),
        "entries_by_verification_level": dict(level_counts),
        "flags_by_severity": dict(severity_counts),
        "flags_by_code": dict(flag_codes),
        "dated_offers": len(dated),
        "undated_offers": len(entries) - len(dated),
        "source_count": sum(len(e.get("sources", [])) for e in entries),
        "publishers": publishers,
        "source_domains": domains,
    }


def build() -> dict:
    meta = load_json(DATA / "meta.json")
    entries: list[dict] = []
    excluded: list[dict] = []

    for path in sorted(ENTRIES_DIR.glob("*.json")):
        items = load_json(path)
        shard = path.name
        for item in items:
            item["_shard"] = shard
        if shard in EXCLUDED_SHARDS:
            excluded.extend(items)
        else:
            entries.extend(items)

    problems = validate(meta, entries, excluded)
    if problems:
        print("Dataset validation FAILED:", file=sys.stderr)
        for problem in problems:
            print("  - " + problem, file=sys.stderr)
        raise SystemExit(1)

    stats = summarise(meta, entries, excluded)
    payload = {
        "meta": meta,
        "entries": entries,
        "excluded": excluded,
        "stats": stats,
        "built_at": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    return payload


def classify_host(url: str) -> str:
    host = url.split("/")[2].lower() if "://" in url else url
    return host[4:] if host.startswith("www.") else host


def render_sources_md(payload: dict) -> str:
    """Generate docs/SOURCES.md straight from the dataset so it can never drift."""
    meta = payload["meta"]
    stats = payload["stats"]
    entries = payload["entries"]
    excluded = payload["excluded"]
    compiled = meta["dataset"]["compiled_at"]

    POLICY_CATEGORIES = {"policy-debunk"}
    official: dict[str, list] = {}
    third_party: dict[str, list] = {}

    for entry in entries:
        is_policy = bool(set(entry.get("categories", [])) & POLICY_CATEGORIES)
        for src in entry.get("sources", []):
            row = {"url": src["url"], "title": src.get("title", ""), "publisher": src.get("publisher", ""),
                   "accessed": src.get("accessed", ""), "method": src.get("method", ""),
                   "evidence": src.get("evidence", ""), "entries": [], "policy": is_policy}
            host = classify_host(src["url"])
            bucket = third_party if is_policy else official
            bucket.setdefault(host, {})
            existing = bucket[host].get(src["url"])
            if existing is None:
                bucket[host][src["url"]] = row
                existing = row
            if (entry["id"], entry["title"]) not in existing["entries"]:
                existing["entries"].append((entry["id"], entry["title"]))

    for item in excluded:
        for src in item.get("urls_checked", []):
            host = classify_host(src["url"])
            third_party.setdefault(host, {})
            existing = third_party[host].get(src["url"])
            if existing is None:
                existing = {"url": src["url"], "title": src.get("title", ""), "publisher": src.get("publisher", ""),
                            "accessed": src.get("accessed", ""), "method": src.get("method", ""),
                            "evidence": src.get("evidence", ""), "entries": [], "policy": True}
                third_party[host][src["url"]] = existing
            if (item["id"], item.get("merchant", "")) not in existing["entries"]:
                existing["entries"].append((item["id"], item.get("merchant", "")))

    out: list[str] = []
    out.append("<!-- GENERATED FILE \u2014 do not edit by hand. -->")
    out.append("<!-- Produced by scripts/build_site.py from data/meta.json and data/entries/*.json. -->")
    out.append("")
    out.append("# Sources")
    out.append("")
    out.append(
        f"Every citation behind the dataset, so any offer can be checked by hand. "
        f"Verified **{compiled}**. {stats['entry_count']} offers, {stats['excluded_count']} rejected claims, "
        f"{stats['source_count']} citations across {len(stats['source_domains'])} domains."
    )
    out.append("")
    out.append(
        "The rule this list exists to prove: an offer is cited to **the party that has to honour it**. "
        "Aggregators, cashback portals, promo-code sites, listicles and social posts appear only in the "
        "second table, where they are the *evidence that a claim is not official*, never the source of an offer."
    )
    out.append("")
    out.append("## 1. Official issuer sources")
    out.append("")
    out.append("| Domain | URL | Publisher | Checked | Method | Cited by |")
    out.append("| --- | --- | --- | --- | --- | --- |")
    for host in sorted(official):
        for url in sorted(official[host]):
            row = official[host][url]
            cited = "<br>".join(f"`{eid}`" for eid, _ in row["entries"][:6])
            if len(row["entries"]) > 6:
                cited += f"<br>\u2026 and {len(row['entries']) - 6} more"
            title = (row["title"] or url).replace("|", "\|")
            out.append(
                f"| `{host}` | [{title}]({url}) | {row['publisher']} | {row['accessed']} | `{row['method']}` | {cited} |"
            )
    out.append("")
    out.append("### What each official source established")
    out.append("")
    for host in sorted(official):
        out.append(f"#### `{host}`")
        out.append("")
        for url in sorted(official[host]):
            row = official[host][url]
            out.append(f"- **[{row['title'] or url}]({url})** \u2014 checked {row['accessed']} via `{row['method']}`")
            out.append(f"  - Evidence read: {row['evidence']}")
            out.append(f"  - Supports: " + ", ".join(f"`{eid}`" for eid, _ in row["entries"]))
        out.append("")

    out.append("## 2. Third-party sources (rejection evidence and policy notes only)")
    out.append("")
    out.append(
        "These were consulted to establish what is *circulating* and to document scam vectors. "
        "None of them is the source of an available offer in this dataset."
    )
    out.append("")
    out.append("| Domain | URL | Publisher | Checked | Method | Used in |")
    out.append("| --- | --- | --- | --- | --- | --- |")
    for host in sorted(third_party):
        for url in sorted(third_party[host]):
            row = third_party[host][url]
            cited = ", ".join(f"`{eid}`" for eid, _ in row["entries"][:5])
            if len(row["entries"]) > 5:
                cited += f" \u2026 +{len(row['entries']) - 5}"
            title = (row["title"] or url).replace("|", "\|")
            out.append(
                f"| `{host}` | [{title}]({url}) | {row['publisher']} | {row['accessed']} | `{row['method']}` | {cited} |"
            )
    out.append("")

    # link-rot log
    out.append("## 3. Official URLs that failed on the verification date")
    out.append("")
    out.append(
        "Recorded so that nobody treats them as working citations. Each was fetched on "
        f"{compiled} and the failure observed directly."
    )
    out.append("")
    out.append("| URL that failed | What came back | Working replacement |")
    out.append("| --- | --- | --- |")
    for entry in entries:
        for broken in entry.get("broken_urls", []) or []:
            result = (broken.get("result") or "").replace("|", "\|")
            replacement = (broken.get("working_replacement") or "\u2014").replace("|", "\|")
            out.append(f"| `{broken.get('url')}` | {result} | {replacement} |")
    out.append("")

    out.append("## 4. Re-running the checks yourself")
    out.append("")
    out.append("```bash")
    out.append("# re-fetch every URL in this document and report what resolves")
    out.append("python3 scripts/verify_links.py")
    out.append("")
    out.append("# only the citations for one merchant or entry id")
    out.append("python3 scripts/verify_links.py --filter costco")
    out.append("")
    out.append("# fail if something outside the documented link-rot log breaks")
    out.append("python3 scripts/verify_links.py --strict")
    out.append("")
    out.append("# enforce the sourcing rules mechanically")
    out.append("python3 -m unittest discover -s tests -v")
    out.append("```")
    out.append("")
    out.append(
        "The weekly GitHub Actions run (`.github/workflows/verify.yml`) repeats the link check every Monday "
        "and files a `link-rot` issue when a citation outside the documented log stops resolving."
    )
    out.append("")
    return "\n".join(out)


def canonical(payload: dict) -> str:
    """Serialise the payload without the volatile build timestamp."""
    stable = {k: v for k, v in payload.items() if k != "built_at"}
    return json.dumps(stable, ensure_ascii=False, separators=(",", ":"))


def write_outputs(payload: dict, make_site: bool = True) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "coupons.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    ASSETS_DATA.mkdir(parents=True, exist_ok=True)
    js = (
        "/* GENERATED FILE \u2014 do not edit by hand.\n"
        "   Produced by scripts/build_site.py from data/meta.json and data/entries/*.json.\n"
        "   Every offer string in here is quoted from an official source; see the\n"
        "   'sources' array on each entry for the citation and the evidence text. */\n"
        "window.COUPON_DATA = "
        + json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        + ";\n"
    )
    (ASSETS_DATA / "coupons.js").write_text(js, encoding="utf-8")

    if make_site:
        if SITE_DIR.exists():
            shutil.rmtree(SITE_DIR)
        SITE_DIR.mkdir(parents=True)
        for name in ("index.html", "assets", "data", ".nojekyll"):
            src = ROOT / name
            if not src.exists():
                continue
            dst = SITE_DIR / name
            if src.is_dir():
                shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))
            else:
                shutil.copy2(src, dst)
        # The site needs the generated JS and the merged JSON inside _site/data too.
        (SITE_DIR / "data").mkdir(parents=True, exist_ok=True)
        shutil.copy2(ASSETS_DATA / "coupons.js", SITE_DIR / "assets" / "data" / "coupons.js")
        shutil.copy2(DATA / "coupons.json", SITE_DIR / "data" / "coupons.json")

    docs = ROOT / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "SOURCES.md").write_text(render_sources_md(payload), encoding="utf-8")

    stats = payload["stats"]
    print(
        f"built: {stats['entry_count']} verified entries, {stats['excluded_count']} rejected items, "
        f"{stats['source_count']} citations across {len(stats['source_domains'])} domains"
    )
    print("       verification levels:", stats["entries_by_verification_level"])
    print("       flags by severity:  ", stats["flags_by_severity"])


def outputs_current() -> bool:
    """True if data/coupons.json and assets/data/coupons.js match the shards."""
    payload = build()
    js_path = ASSETS_DATA / "coupons.js"
    json_path = DATA / "coupons.json"
    if not js_path.exists() or not json_path.exists():
        return False
    text = js_path.read_text(encoding="utf-8")
    marker = "window.COUPON_DATA = "
    if marker not in text:
        return False
    existing_js = json.loads(text.split(marker, 1)[1].rstrip().rstrip(";"))
    existing_json = json.loads(json_path.read_text(encoding="utf-8"))
    expected = canonical(payload)
    if canonical(existing_js) != expected or canonical(existing_json) != expected:
        return False
    sources_md = ROOT / "docs" / "SOURCES.md"
    if not sources_md.exists():
        return False
    return sources_md.read_text(encoding="utf-8") == render_sources_md(payload)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify generated output is up to date and exit")
    parser.add_argument("--no-site", action="store_true", help="skip building the _site directory")
    args = parser.parse_args()

    if args.check:
        if outputs_current():
            print("generated dataset is up to date")
            return
        print("generated dataset is STALE \u2014 run: python3 scripts/build_site.py", file=sys.stderr)
        raise SystemExit(1)

    payload = build()
    write_outputs(payload, make_site=not args.no_site)


if __name__ == "__main__":
    main()

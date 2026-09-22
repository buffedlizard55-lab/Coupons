#!/usr/bin/env python3
"""Re-check every URL cited in the dataset.

The project's whole guarantee rests on citations that a human can open. Links rot
fast in the coupon world (Costco rotates its offer pages, Safeway moved /foru/coupons,
the California Academy's free-Sunday page is gone), so this script re-fetches every
citation and reports what it finds.

It is deliberately conservative:

* It never edits the dataset. It only reports.
* URLs already recorded as broken in the link-rot entry
  (``policy-link-rot-observed-2026-09-22``) are treated as *expected* failures and
  do not fail a ``--strict`` run. Everything else that fails does.
* A page that returns HTTP 200 but whose body is an error shell is reported as
  ``soft_404`` so that "technically resolves" is not confused with "still live".

Usage:
    python3 scripts/verify_links.py                  # check everything, write report
    python3 scripts/verify_links.py --strict         # also exit 1 on new failures
    python3 scripts/verify_links.py --workers 4      # be politer
    python3 scripts/verify_links.py --limit 20       # smoke test
    python3 scripts/verify_links.py --filter costco  # only URLs matching a substring
"""

from __future__ import annotations

import argparse
import concurrent.futures as futures
import datetime as _dt
import html.parser
import json
import pathlib
import sys
import time
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA_JSON = ROOT / "data" / "coupons.json"
REPORT_DIR = ROOT / "reports"

USER_AGENT = (
    "Mozilla/5.0 (compatible; BayAreaVerifiedCoupons-LinkChecker/1.0; "
    "+https://github.com/buffedlizard55-lab/Coupons)"
)

LINK_ROT_ENTRY = "policy-link-rot-observed-2026-09-22"

# Bodies that mean "HTTP 200 but the page is gone".
SOFT_404_MARKERS = (
    "page not found",
    "404 not found",
    "oops! looks like this page",
    "we can't find the page you're looking for",
    "someone pulled the plug on this page",
    "looks like someone took the last slice",
    "there's no fried chicken on this page",
    "error 404",
    "page you are looking for doesn't exist",
)


class TitleParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._in_title = False
        self.title = ""

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title and len(self.title) < 300:
            self.title += data


def collect(dataset: dict) -> list[dict]:
    """Every URL in the dataset, with the context it was cited in."""
    rows: list[dict] = []
    seen: set[tuple[str, str]] = set()

    def add(url: str | None, kind: str, owner: str, detail: str = "") -> None:
        if not url or not str(url).startswith(("http://", "https://")):
            return
        url = str(url).strip()
        key = (url, kind)
        if key in seen:
            return
        seen.add(key)
        rows.append({"url": url, "kind": kind, "entry": owner, "detail": detail})

    for entry in dataset.get("entries", []):
        eid = entry["id"]
        for src in entry.get("sources", []):
            add(src.get("url"), "source", eid, src.get("publisher", ""))
        bay = entry.get("bay_area") or {}
        add(bay.get("locator_url"), "locator", eid)
        venue = entry.get("venue") or {}
        add(venue.get("website"), "venue_site", eid)
        for ex in entry.get("verified_price_examples", []) or []:
            add(ex.get("url"), "price_example", eid, ex.get("drug", ""))
        for broken in entry.get("broken_urls", []) or []:
            add(broken.get("url"), "known_broken", eid, broken.get("result", ""))

    for item in dataset.get("excluded", []):
        for checked in item.get("urls_checked", []) or []:
            add(checked.get("url"), "rejected_evidence", item["id"], checked.get("publisher", ""))

    return rows


def known_broken_urls(dataset: dict) -> set[str]:
    urls: set[str] = set()
    for entry in dataset.get("entries", []):
        if entry["id"] != LINK_ROT_ENTRY:
            continue
        for broken in entry.get("broken_urls", []) or []:
            if broken.get("url"):
                urls.add(broken["url"].strip())
    return urls


def check(row: dict, timeout: float) -> dict:
    url = row["url"]
    result = dict(row)
    result["checked_at"] = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    result["status"] = None
    result["final_url"] = None
    result["title"] = None
    result["verdict"] = "unknown"
    result["note"] = ""

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    started = time.time()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read(400_000)
            result["status"] = getattr(response, "status", response.getcode())
            result["final_url"] = response.geturl()
            text = body.decode("utf-8", errors="replace").lower()
            parser = TitleParser()
            try:
                parser.feed(body.decode("utf-8", errors="replace")[:200_000])
            except Exception:  # malformed HTML is not a link failure
                pass
            result["title"] = (parser.title or "").strip()[:200] or None
            if result["status"] == 200:
                if any(marker in text for marker in SOFT_404_MARKERS):
                    result["verdict"] = "soft_404"
                    result["note"] = "HTTP 200 but the body is an error page"
                elif len(body) < 600 and "<html" not in text:
                    result["verdict"] = "suspicious"
                    result["note"] = f"HTTP 200 with a {len(body)}-byte non-HTML body"
                else:
                    result["verdict"] = "ok"
            else:
                result["verdict"] = "http_error"
                result["note"] = f"HTTP {result['status']}"
    except urllib.error.HTTPError as exc:
        result["status"] = exc.code
        result["verdict"] = "http_error"
        result["note"] = f"HTTP {exc.code} {exc.reason}"
    except urllib.error.URLError as exc:
        result["verdict"] = "unreachable"
        result["note"] = str(exc.reason)
    except TimeoutError:
        result["verdict"] = "timeout"
        result["note"] = f"no response within {timeout}s"
    except Exception as exc:  # noqa: BLE001 - a link checker must not crash on one URL
        result["verdict"] = "error"
        result["note"] = f"{type(exc).__name__}: {exc}"
    result["elapsed_s"] = round(time.time() - started, 2)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--strict", action="store_true", help="exit 1 if a URL outside the known-broken list fails")
    parser.add_argument("--workers", type=int, default=6, help="parallel requests (default 6)")
    parser.add_argument("--timeout", type=float, default=25.0, help="per-request timeout in seconds")
    parser.add_argument("--limit", type=int, default=0, help="check at most N URLs (smoke test)")
    parser.add_argument("--filter", default="", help="only check URLs containing this substring")
    parser.add_argument("--report", default=str(REPORT_DIR / "link-check.json"), help="where to write the report")
    parser.add_argument("--no-network", action="store_true", help="collect and report URLs without fetching (offline CI)")
    args = parser.parse_args()

    if not DATA_JSON.exists():
        print(f"missing {DATA_JSON} \u2014 run: python3 scripts/build_site.py", file=sys.stderr)
        return 2

    dataset = json.loads(DATA_JSON.read_text(encoding="utf-8"))
    rows = collect(dataset)
    if args.filter:
        needle = args.filter.lower()
        rows = [r for r in rows if needle in r["url"].lower() or needle in r["entry"].lower()]
    if args.limit:
        rows = rows[: args.limit]

    expected_failures = known_broken_urls(dataset)
    print(f"{len(rows)} URLs to check ({len(expected_failures)} already recorded as broken)")

    if args.no_network:
        results = [dict(r, verdict="not_checked", note="--no-network") for r in rows]
    else:
        results = []
        with futures.ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
            for res in pool.map(lambda r: check(r, args.timeout), rows):
                results.append(res)
                mark = {"ok": ".", "soft_404": "S", "http_error": "H", "unreachable": "U",
                        "timeout": "T", "suspicious": "?", "error": "E"}.get(res["verdict"], "x")
                print(f"  {mark} {res['status'] or '---'} {res['url'][:96]}", flush=True)

    bad = [r for r in results if r["verdict"] not in ("ok", "not_checked")]
    new_bad = [r for r in bad if r["url"] not in expected_failures]

    report = {
        "generated_at": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "dataset_verified_at": dataset.get("meta", {}).get("dataset", {}).get("compiled_at"),
        "no_network": args.no_network,
        "checked": len(results),
        "ok": sum(1 for r in results if r["verdict"] == "ok"),
        "failed": len(bad),
        "failed_expected": len(bad) - len(new_bad),
        "failed_new": len(new_bad),
        "results": results,
    }
    report_path = pathlib.Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"\nreport: {report_path}")
    print(f"  ok {report['ok']} / checked {report['checked']}")
    print(f"  failing {report['failed']} (already documented as broken: {report['failed_expected']}, new: {report['failed_new']})")
    if new_bad:
        print("\nnew failures (not in the documented link-rot log):")
        for r in new_bad[:40]:
            print(f"  [{r['verdict']}] {r['url']}  <- {r['entry']}")
        if len(new_bad) > 40:
            print(f"  ... and {len(new_bad) - 40} more")

    if args.strict and new_bad and not args.no_network:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

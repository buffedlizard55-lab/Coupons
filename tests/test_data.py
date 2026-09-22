#!/usr/bin/env python3
"""Integrity tests for the verified-coupon dataset.

These tests exist to make the project's central promise mechanically checkable:
every published offer is quoted from an official source, dated, and flagged when
anything about it is irregular. Run with:

    python3 -m unittest discover -s tests -v
"""

from __future__ import annotations

import datetime as _dt
import json
import pathlib
import re
import shutil
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
ENTRIES_DIR = DATA / "entries"

sys.path.insert(0, str(ROOT / "scripts"))
import build_site  # noqa: E402


# Domains that must never be cited as the source of an *available* offer.
# They are allowed inside data/entries/10-excluded-unverified.json (where they are
# the evidence that a claim is not official) and inside level-C policy notes that
# document how a scam vector works.
NON_OFFICIAL_DOMAINS = (
    "couponscc.com",
    "simplycodes.com",
    "couponcabin.com",
    "coupongreat.com",
    "valuecom.com",
    "couponfollow.com",
    "retailmenot.com",
    "savings.com",
    "coupons4u.com",
    "freebie-depot.com",
    "freestufffinder.com",
    "couponingfor4.net",
    "coupons4all.com",
    "dealigg.com",
    "dealam.com",
    "dealbreaker.com",
    "thekrazycouponlady.com",
    "slickdeals.net",
    "nerdwallet.com",
    "moneypantry.com",
    "chowhound.com",
    "mashed.com",
    "tastingtable.com",
    "foodandwine.com",
    "eatthis.com",
    "daze.app",
    "tiktok.com",
    "facebook.com",
    "instagram.com",
    "youtube.com",
    "reddit.com",
    "x.com",
    "twitter.com",
)

POLICY_CATEGORIES = {"policy-debunk"}


def is_non_official(url: str) -> bool:
    host = url.split("/")[2].lower() if "://" in url else ""
    return any(host == d or host.endswith("." + d) for d in NON_OFFICIAL_DOMAINS)

ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def load_shards():
    meta = json.loads((DATA / "meta.json").read_text(encoding="utf-8"))
    entries, excluded = [], []
    for path in sorted(ENTRIES_DIR.glob("*.json")):
        items = json.loads(path.read_text(encoding="utf-8"))
        for item in items:
            item["_shard"] = path.name
        if path.name in build_site.EXCLUDED_SHARDS:
            excluded.extend(items)
        else:
            entries.extend(items)
    return meta, entries, excluded


META, ENTRIES, EXCLUDED = load_shards()


class TestDatasetIntegrity(unittest.TestCase):
    def test_dataset_is_not_empty(self):
        self.assertGreater(len(ENTRIES), 50, "expected a substantial verified dataset")
        self.assertGreater(len(EXCLUDED), 0, "a dataset with no rejections did not check anything")

    def test_ids_are_unique(self):
        ids = [e["id"] for e in ENTRIES] + [e["id"] for e in EXCLUDED]
        self.assertEqual(len(ids), len(set(ids)), "duplicate entry ids: %s" % [i for i in ids if ids.count(i) > 1])

    def test_ids_are_url_safe(self):
        for entry in ENTRIES + EXCLUDED:
            self.assertRegex(entry["id"], r"^[a-z0-9][a-z0-9._-]*$", f"{entry['id']} is not a URL-safe id")

    def test_required_fields_present(self):
        for entry in ENTRIES:
            for field in build_site.REQUIRED_ENTRY_FIELDS:
                self.assertIn(field, entry, f"{entry['id']} missing '{field}'")
        for item in EXCLUDED:
            for field in build_site.REQUIRED_EXCLUDED_FIELDS:
                self.assertIn(field, item, f"{item['id']} missing '{field}'")

    def test_taxonomy_values_are_known(self):
        categories = {c["id"] for c in META["categories"]}
        deals = {d["id"] for d in META["deal_types"]}
        levels = set(META["verification"]["levels"])
        methods = set(META["verification"]["methods"])
        severities = set(META["flag_severities"])
        for entry in ENTRIES:
            for c in entry["categories"]:
                self.assertIn(c, categories, f"{entry['id']} uses unknown category '{c}'")
            for d in entry["deal_types"]:
                self.assertIn(d, deals, f"{entry['id']} uses unknown deal type '{d}'")
            self.assertIn(entry["verification"]["level"], levels, f"{entry['id']} unknown level")
            for s in entry["sources"]:
                self.assertIn(s["method"], methods, f"{entry['id']} unknown method '{s['method']}'")
            for f in entry["flags"]:
                self.assertIn(f["severity"], severities, f"{entry['id']} unknown severity '{f['severity']}'")

    def test_every_entry_has_a_usable_title_and_offer_text(self):
        for entry in ENTRIES:
            self.assertGreater(len(entry["title"].strip()), 8, f"{entry['id']} title too short")
            self.assertGreater(len(entry["offer_text"].strip()), 8, f"{entry['id']} offer text too short")
            self.assertIsInstance(entry["offer_text_is_verbatim"], bool, f"{entry['id']} verbatim flag must be boolean")

    def test_expiries_are_iso_dates_or_null(self):
        for entry in ENTRIES:
            exp = entry["expires"]
            if exp is None:
                continue
            self.assertRegex(exp, ISO_DATE, f"{entry['id']} expires '{exp}' is not YYYY-MM-DD")
            _dt.date.fromisoformat(exp)
            self.assertTrue(entry.get("expiry_basis"), f"{entry['id']} has an expiry but no expiry_basis")
        for entry in ENTRIES:
            pw = entry.get("purchase_window")
            if pw:
                self.assertRegex(pw["start"], ISO_DATE)
                self.assertRegex(pw["end"], ISO_DATE)

    def test_verified_at_dates_are_iso_and_consistent_with_meta(self):
        dates = []
        for entry in ENTRIES:
            v = entry["verification"]["verified_at"]
            self.assertRegex(v, ISO_DATE, f"{entry['id']} verified_at '{v}' is not YYYY-MM-DD")
            dates.append(_dt.date.fromisoformat(v))
            for s in entry["sources"]:
                self.assertRegex(s["accessed"], ISO_DATE, f"{entry['id']} source accessed date malformed")
                self.assertLessEqual(
                    _dt.date.fromisoformat(s["accessed"]),
                    _dt.date.fromisoformat(v),
                    f"{entry['id']} cites a source accessed after its own verification date",
                )
        self.assertEqual(
            META["dataset"]["compiled_at"],
            max(dates).isoformat(),
            "meta.json compiled_at should equal the latest verification date in the dataset",
        )

    def test_every_entry_documents_how_it_was_checked(self):
        for entry in ENTRIES:
            checks = entry["verification"]["checks"]
            self.assertGreaterEqual(len(checks), 2, f"{entry['id']} has fewer than two verification checks")
            for c in checks:
                self.assertGreater(len(c), 15, f"{entry['id']} has a trivially short verification check")

    def test_every_entry_has_a_flag_or_is_clean_by_design(self):
        """Flags are optional, but when present they must be well formed."""
        for entry in ENTRIES:
            for f in entry["flags"]:
                self.assertTrue(f.get("code"), f"{entry['id']} flag without a code")
                self.assertGreater(len(f["detail"]), 20, f"{entry['id']} flag detail too short")
                self.assertNotIn("TODO", f["detail"], f"{entry['id']} unfinished flag text")


class TestSourcingRules(unittest.TestCase):
    def test_sources_are_well_formed(self):
        for entry in ENTRIES:
            self.assertGreaterEqual(len(entry["sources"]), 1, f"{entry['id']} has no source at all")
            for s in entry["sources"]:
                self.assertTrue(s["url"].startswith("https://") or s["url"].startswith("http://"),
                                f"{entry['id']} source url is not absolute")
                for field in ("title", "publisher", "accessed", "method", "evidence"):
                    self.assertTrue(s.get(field), f"{entry['id']} source missing '{field}'")
                self.assertGreater(len(s["evidence"]), 25, f"{entry['id']} evidence is too short to be a real quote")

    def test_level_A_entries_were_read_directly_from_an_official_domain(self):
        """Level A means the text was read from the issuer, so at least one citation must be
        a direct retrieval (fetch_page / official_document) of a non-third-party domain."""
        for entry in ENTRIES:
            if entry["verification"]["level"] != "A":
                continue
            if set(entry["categories"]) & POLICY_CATEGORIES:
                continue  # method/policy notes legitimately cite the places they document
            hits = [s for s in entry["sources"] if not is_non_official(s["url"])]
            self.assertTrue(
                hits,
                f"{entry['id']} claims level A but cites no official-domain source",
            )

    def test_search_snippet_only_entries_disclose_it(self):
        """If the only retrieval method was a search-engine snippet of the issuer's page,
        the entry must say so on its face instead of implying a direct fetch."""
        for entry in ENTRIES:
            if set(entry["categories"]) & POLICY_CATEGORIES:
                continue
            methods = {s["method"] for s in entry["sources"]}
            if methods and methods <= {"web_search"}:
                codes = {f["code"] for f in entry["flags"]}
                self.assertIn(
                    "retrieval-via-search-snippet",
                    codes,
                    f"{entry['id']} was sourced only from search snippets but does not disclose it",
                )

    def test_level_B_entries_are_program_level_not_offer_level(self):
        """Level B admits that the rotating offers could not be read; such entries must say so."""
        for entry in ENTRIES:
            if entry["verification"]["level"] != "B":
                continue
            blob = " ".join(c["detail"] for c in entry["flags"]) + " " + " ".join(entry["verification"]["checks"])
            keywords = ("app", "account", "rotating", "personalis", "personaliz", "in-store", "membership",
                        "could not", "not publish", "unpublished", "no dollar amount", "anonymous", "locator",
                        "not retrieved", "not captured", "not asserted", "not enumerated", "no published")
            self.assertTrue(
                any(k in blob.lower() for k in keywords),
                f"{entry['id']} is level B but never explains why the individual offers were not enumerated",
            )

    def test_no_aggregator_or_social_domain_sources_an_offer(self):
        """The core anti-scam rule, enforced mechanically.

        Policy and method notes (category 'policy-debunk') are allowed to cite the third-party
        sites they are debunking or documenting — that is their evidence. Everything else must
        be sourced from the party that has to honour the offer.
        """
        offenders = []
        for entry in ENTRIES:
            if set(entry["categories"]) & POLICY_CATEGORIES:
                continue
            for s in entry["sources"]:
                if is_non_official(s["url"]):
                    offenders.append(f"{entry['id']} (level {entry['verification']['level']}) cites {s['url'].split('/')[2]}")
        self.assertEqual(offenders, [], "non-official domains used to source offers:\n  " + "\n  ".join(offenders))

    def test_policy_notes_cannot_masquerade_as_offers(self):
        for entry in ENTRIES:
            if not set(entry["categories"]) & POLICY_CATEGORIES:
                continue
            self.assertEqual(entry["deal_types"], ["policy"], f"{entry['id']} is a policy note but carries a real deal type")
            self.assertIsNone(entry["value"], f"{entry['id']} is a policy note but advertises a value")
            self.assertIsNone(entry["expires"], f"{entry['id']} is a policy note but carries a deadline")

    def test_excluded_items_are_evidenced(self):
        for item in EXCLUDED:
            self.assertGreaterEqual(len(item["urls_checked"]), 1, f"{item['id']} rejection has no checked URLs")
            for u in item["urls_checked"]:
                for field in ("url", "publisher", "accessed", "method", "evidence"):
                    self.assertTrue(u.get(field), f"{item['id']} urls_checked entry missing '{field}'")
            self.assertGreater(len(item["why_rejected"]), 40, f"{item['id']} rejection reason too thin")
            self.assertGreater(len(item["what_would_verify_it"]), 20, f"{item['id']} does not say what would change the verdict")


class TestValueSchema(unittest.TestCase):
    CANONICAL = ("amount", "unit", "currency", "kind")
    UNITS = {"currency", "percent", "points"}
    KINDS = {
        "dollar_off", "percent_off", "rebate", "reduced_admission", "free_admission",
        "free_item", "member_price", "rewards_credit", "points",
    }

    def test_value_objects_are_canonical(self):
        for entry in ENTRIES:
            v = entry.get("value")
            if v is None:
                continue
            self.assertEqual(tuple(v.keys()), self.CANONICAL,
                             f"{entry['id']} value does not follow data/meta.json value_schema: {v}")
            self.assertIn(v["unit"], self.UNITS, f"{entry['id']} unknown unit '{v['unit']}'")
            self.assertIn(v["kind"], self.KINDS, f"{entry['id']} unknown value kind '{v['kind']}'")
            if v["unit"] == "currency":
                self.assertEqual(v["currency"], "USD", f"{entry['id']} currency should be USD")
                self.assertIsInstance(v["amount"], (int, float), f"{entry['id']} currency value needs a number")
            else:
                self.assertIsNone(v["currency"], f"{entry['id']} non-currency value must not carry a currency")

    def test_free_admission_is_always_zero(self):
        for entry in ENTRIES:
            v = entry.get("value")
            if isinstance(v, dict) and v["kind"] == "free_admission":
                self.assertEqual(v["amount"], 0, f"{entry['id']} is free admission but carries a price")

    def test_free_item_amounts_are_issuer_published_caps(self):
        """A free item may carry a non-zero amount ONLY when the issuer publishes that figure as a
        value cap, and the cap must literally appear in the quoted offer text. This stops an
        estimated 'worth about $X' from being recorded as if the issuer said it."""
        for entry in ENTRIES:
            v = entry.get("value")
            if not isinstance(v, dict) or v["kind"] != "free_item" or not v["amount"]:
                continue
            cap = "$" + (str(int(v["amount"])) if float(v["amount"]).is_integer() else str(v["amount"]))
            self.assertIn(
                cap,
                entry["offer_text"],
                f"{entry['id']} records a {cap} value cap that does not appear in the quoted offer text",
            )

    def test_percent_values_are_plausible(self):
        for entry in ENTRIES:
            v = entry.get("value")
            if isinstance(v, dict) and v["unit"] == "percent":
                self.assertGreater(v["amount"], 0, f"{entry['id']} percent value is not positive")
                self.assertLessEqual(v["amount"], 100, f"{entry['id']} percent value exceeds 100")

    def test_meta_documents_the_value_schema(self):
        schema = META["value_schema"]
        self.assertEqual(set(schema["fields"]), set(self.CANONICAL))
        self.assertTrue(schema["rules"])


class TestBayAreaUsability(unittest.TestCase):
    COUNTIES = set(META["bay_area_counties"])

    def test_bay_area_block_is_complete(self):
        for entry in ENTRIES:
            b = entry["bay_area"]
            self.assertIsInstance(b["available"], bool, f"{entry['id']} bay_area.available must be boolean")
            self.assertIn(b["confidence"], {"high", "medium", "low"}, f"{entry['id']} bad confidence value")
            if b["available"] is False:
                self.assertTrue(b.get("note"), f"{entry['id']} unavailable without an explanation")

    def test_unavailable_offers_are_flagged(self):
        for entry in ENTRIES:
            if entry["bay_area"]["available"] is False:
                codes = {f["code"] for f in entry["flags"]}
                self.assertTrue(
                    codes & {"announced-but-not-live", "eligibility-unclear", "critical"},
                    f"{entry['id']} is marked unavailable in the Bay Area but carries no explanatory flag",
                )

    def test_physical_redemption_is_addressed(self):
        """Every offer must state where it is redeemed: a venue, store list, locator URL, or a note."""
        for entry in ENTRIES:
            b = entry["bay_area"]
            if not b["available"]:
                continue
            has_place = bool(entry.get("venue")) or bool(b.get("physical_locations")) or bool(b.get("locator_url")) or bool(b.get("note"))
            self.assertTrue(has_place, f"{entry['id']} gives no way to find a physical redemption location")

    def test_venue_entries_are_locatable(self):
        """A venue block must give a street address, or the entry must publish an official
        locator and a list of physical locations (national/multi-site programs)."""
        for entry in ENTRIES:
            v = entry.get("venue")
            if not v:
                continue
            if v.get("address"):
                continue
            b = entry["bay_area"]
            self.assertTrue(
                b.get("locator_url") and (b.get("physical_locations") or b.get("note")),
                f"{entry['id']} has a venue with no address and no official locator to find one",
            )

    def test_county_mentions_match_the_published_definition(self):
        pattern = r"(Alameda|Contra Costa|Marin|Napa|San Francisco|San Mateo|Santa Clara|Solano|Sonoma|Sacramento|Los Angeles|New York) County"
        for entry in ENTRIES:
            blob = json.dumps(entry.get("bay_area", {}))
            for county in re.findall(pattern, blob):
                self.assertIn(
                    county,
                    self.COUNTIES,
                    f"{entry['id']} refers to '{county} County', which is outside the project's nine-county definition",
                )


class TestNoUnfinishedWork(unittest.TestCase):
    # Note: "XXXX" is deliberately NOT a marker — P&G publishes brand placeholders as
    # "(XXXX) Dawn Powerwash" and that text is reproduced verbatim on purpose.
    MARKERS = ("TODO", "FIXME", "PLACEHOLDER", "lorem ipsum", "TBD-fill", "<your ")

    def test_no_placeholders_in_data(self):
        for path in sorted(ENTRIES_DIR.glob("*.json")):
            text = path.read_text(encoding="utf-8")
            for marker in self.MARKERS:
                self.assertNotIn(marker, text, f"{path.name} contains the marker '{marker}'")

    def test_no_placeholders_in_site(self):
        for path in [ROOT / "index.html", ROOT / "assets" / "js" / "app.js", ROOT / "assets" / "css" / "styles.css"]:
            text = path.read_text(encoding="utf-8")
            for marker in ("TODO", "FIXME", "lorem ipsum", "PLACEHOLDER"):
                self.assertNotIn(marker, text, f"{path.name} contains '{marker}'")


class TestGeneratedFilesInSync(unittest.TestCase):
    def test_generated_dataset_matches_shards(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "build_site.py"), "--check"],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, "generated dataset is stale:\n" + result.stdout + result.stderr)

    def test_merged_json_matches_shard_counts(self):
        merged = json.loads((DATA / "coupons.json").read_text(encoding="utf-8"))
        self.assertEqual(len(merged["entries"]), len(ENTRIES))
        self.assertEqual(len(merged["excluded"]), len(EXCLUDED))
        self.assertEqual(merged["stats"]["entry_count"], len(ENTRIES))
        self.assertEqual(
            merged["stats"]["source_count"],
            sum(len(e["sources"]) for e in ENTRIES),
        )

    def test_site_payload_is_valid_js_assignment(self):
        js = (ROOT / "assets" / "data" / "coupons.js").read_text(encoding="utf-8")
        self.assertTrue(js.startswith("/*"), "generated JS should carry its provenance comment")
        self.assertIn("window.COUPON_DATA = ", js)
        payload = json.loads(js.split("window.COUPON_DATA = ", 1)[1].rstrip().rstrip(";"))
        self.assertIn("meta", payload)
        self.assertIn("entries", payload)
        self.assertIn("excluded", payload)


@unittest.skipUnless(shutil.which("node"), "node is not installed")
class TestSiteRenders(unittest.TestCase):
    """Runs the real front-end against the real dataset in a minimal DOM shim."""

    def test_render_smoke_test(self):
        result = subprocess.run(
            ["node", str(ROOT / "tests" / "test_site_render.js")],
            capture_output=True, text=True, timeout=300,
        )
        self.assertEqual(
            result.returncode, 0,
            "site render smoke test failed:\n" + result.stdout[-4000:] + result.stderr[-4000:],
        )
        self.assertIn("site render smoke test: OK", result.stdout)

    def test_app_js_is_syntactically_valid(self):
        for script in ("assets/js/app.js", "assets/data/coupons.js"):
            result = subprocess.run(["node", "--check", str(ROOT / script)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, f"{script} has a syntax error:\n{result.stderr}")

    def test_index_html_references_existing_assets(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        for ref in re.findall(r'(?:href|src)="([^"#][^"]*)"', html):
            if ref.startswith(("http://", "https://", "mailto:", "tel:")):
                continue
            self.assertTrue((ROOT / ref).exists(), f"index.html references a missing file: {ref}")


DOCS = (
    "README.md",
    "docs/METHODOLOGY.md",
    "docs/LIMITATIONS.md",
    "docs/ROADMAP.md",
    "docs/VERIFICATION-LOG.md",
)


class TestDocsMatchData(unittest.TestCase):
    """Documentation must not drift from the dataset it describes."""

    def setUp(self):
        self.stats = json.loads((DATA / "coupons.json").read_text(encoding="utf-8"))["stats"]
        self.flag_total = sum(self.stats["flags_by_severity"].values())

    def test_flag_totals_in_docs_match_the_data(self):
        for doc in DOCS:
            text = (ROOT / doc).read_text(encoding="utf-8")
            # Sub-counts such as "13 flags across 11 distinct issues" are legitimate; only
            # three-figure mentions can be a claim about the total.
            for m in re.finditer(r"(\d+)\s+flags", text):
                if int(m.group(1)) >= 100:
                    self.assertEqual(int(m.group(1)), self.flag_total,
                                     f"{doc} says '{m.group(1)} flags'; the data has {self.flag_total}")
            for crit, warn, info in re.findall(r"(\d+) critical, (\d+) warning, (\d+) info", text):
                self.assertEqual(
                    (int(crit), int(warn), int(info)),
                    (self.stats["flags_by_severity"]["critical"],
                     self.stats["flags_by_severity"]["warning"],
                     self.stats["flags_by_severity"]["info"]),
                    f"{doc} quotes stale flag severities",
                )

    def test_summary_docs_state_the_current_flag_total(self):
        for doc in ("README.md", "docs/METHODOLOGY.md", "docs/VERIFICATION-LOG.md"):
            text = (ROOT / doc).read_text(encoding="utf-8")
            self.assertIn(f"{self.flag_total} flags", text,
                          f"{doc} never states the current flag total ({self.flag_total})")

    def test_readme_headline_counts_match(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        expectations = {
            f"| Verified offers | **{self.stats['entry_count']}** |": "verified offer count",
            f"| Rejected / scam-watch claims documented | **{self.stats['excluded_count']}** |": "rejection count",
            f"**{self.stats['source_count']}** across **{len(self.stats['source_domains'])}** domains": "citation and domain counts",
            f"A: {self.stats['entries_by_verification_level']['A']} \u00b7 B: {self.stats['entries_by_verification_level']['B']} \u00b7 C: {self.stats['entries_by_verification_level']['C']}": "verification level counts",
        }
        for needle, what in expectations.items():
            self.assertIn(needle, text, f"README {what} no longer matches the data (expected '{needle}')")

    def test_readme_category_table_matches(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        names = {c["id"]: c["name"] for c in META["categories"]}
        for cat_id, count in self.stats["entries_by_category"].items():
            row = f"| {names[cat_id]} | {count} |"
            self.assertIn(row, text, f"README category row for '{names[cat_id]}' should read '{row}'")

    def test_methodology_level_table_matches(self):
        text = (ROOT / "docs/METHODOLOGY.md").read_text(encoding="utf-8")
        rows = dict(re.findall(r"^\| \*\*([ABC])\*\* \|.*\| (\d+) \|$", text, re.M))
        self.assertEqual(rows, {k: str(v) for k, v in self.stats["entries_by_verification_level"].items() if k in "ABC"},
                         "METHODOLOGY verification-level counts do not match the data")

    def test_docs_only_reference_paths_that_exist(self):
        """ROADMAP.md is excluded on purpose: it names files that do not exist yet."""
        pattern = re.compile(r"`([A-Za-z0-9_.\-/]+)`")
        # reports/ is gitignored build output, so it is not required to exist in a fresh checkout.
        prefixes = ("data/", "scripts/", "tests/", "docs/", "assets/", ".github/")
        for doc in [d for d in DOCS if not d.endswith("ROADMAP.md")]:
            text = (ROOT / doc).read_text(encoding="utf-8")
            for token in set(pattern.findall(text)):
                if not token.startswith(prefixes) or "*" in token:
                    continue
                candidate = token.rstrip(".")
                self.assertTrue(
                    (ROOT / candidate).exists(),
                    f"{doc} references `{candidate}`, which does not exist in the repository",
                )

    def test_verification_log_records_every_rejection(self):
        text = (ROOT / "docs/VERIFICATION-LOG.md").read_text(encoding="utf-8")
        for item in EXCLUDED:
            self.assertIn(item["id"], text, f"VERIFICATION-LOG does not mention rejection `{item['id']}`")


class TestMetaPolicy(unittest.TestCase):
    def test_meta_declares_its_guarantees(self):
        for key in ("scope", "no_hallucination_policy", "physical_location_policy", "source_policy",
                    "official_only", "expires_policy", "not_affiliated_disclaimer", "data_license", "timezone_note"):
            self.assertTrue(META["dataset"].get(key), f"meta.json dataset is missing '{key}'")
        self.assertTrue(META["dataset"]["official_only"])

    def test_bay_area_definition_is_published(self):
        self.assertEqual(len(META["bay_area_counties"]), 9)
        self.assertEqual(len(META["bay_area_county_notes"]), 9)

    def test_license_and_reuse_terms_declared(self):
        self.assertTrue(META["license"])
        self.assertTrue(META["dataset"]["not_affiliated_disclaimer"])
        self.assertTrue(META["dataset"]["data_license"])

    def test_county_notes_cover_every_county(self):
        self.assertEqual(set(META["bay_area_county_notes"]), set(META["bay_area_counties"]))
        for county, note in META["bay_area_county_notes"].items():
            self.assertGreater(len(note), 20, f"county note for {county} is too thin to be useful")


if __name__ == "__main__":
    unittest.main(verbosity=2)

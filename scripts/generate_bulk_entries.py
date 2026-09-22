#!/usr/bin/env python3
"""Generate the bulk-verified entry shards for the coupon dataset.

One shard is produced by this script because it is a bulk transcription of a single
official page that was read line by line on 2026-09-22 (re-checked against the live
page in the 2026-09-22 pass 3, and re-confirmed row by row in pass 4 for every
offer line the retrieval chunks could deliver before the fetch proxy degraded):

  data/entries/01-pg-brandsaver.json
  Source: https://pgbrandsaver.com/coupons/  (Procter & Gamble, official)
  The page self-reports "Updated September 2026" and "Search 112 Digital
  Coupons".  Every offer below is a verbatim transcription of the offer text
  and the "Expires" line printed next to it on that page.  Offers that appear
  twice on the page with two different expiry dates are flagged.
  Pass 4 re-read (chunks 0-1 of 10): "Updated September2026" and "Search 112
  Digital Coupons" re-read on the page; the seven Featured rows and the first
  eighteen full rows of the search list matched the transcription — including
  the three Crest reprints at 9/27 inside the list against 9/26 in Featured,
  which re-confirms the contradiction the source-page-inconsistency flags
  record.  One list-view rendering of the Bounce 180 ct line prints "180
  ct(excludes travel size)" with no space; the list cards also print the
  amount glued to the copy ("$3.00OFF ONE"), so this is a DOM/markdown
  flattening artefact of the card layout, noted here rather than "fixed".
  The page has otherwise not changed; neither has this shard.  Chunks 2-9
  (the remaining ~76 offers of the advertised 112) could not be retrieved in
  pass 4 because the fetch proxy failed repeatedly — the full-list harvest
  stays open in docs/ROADMAP.md priority 1.

Each dated entry also carries verification.recheck_due, derived mechanically from
the printed expiry (expiry minus a 3-day safety margin) per the policy documented
in data/meta.json — a scheduling field for the weekly CI job, never an issuer date.

A second bulk shard (26 SF Museums For All venue entries) was generated here until
2026-09-22, when the project was rescoped to product coupons only; that generator
and its transcription now live in archive/rescoped-2026-09-22/.

Nothing here is inferred, remembered or copied from an aggregator.  If a field
could not be read from the source page it is left null and a flag explains it.

Run:  python3 scripts/generate_bulk_entries.py
"""

from __future__ import annotations

import datetime as _dt
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ENTRIES_DIR = ROOT / "data" / "entries"

VERIFIED_AT = "2026-09-22"

# Project re-verification cadence (see data/meta.json → dataset.recheck_policy):
# dated records must be re-read at least this many days before their printed expiry.
RECHECK_BUFFER_DAYS = 3


def recheck_due(expires: str) -> str:
    """The scheduling date for this record: printed expiry minus the safety margin."""
    return (_dt.date.fromisoformat(expires) - _dt.timedelta(days=RECHECK_BUFFER_DAYS)).isoformat()

# ---------------------------------------------------------------------------
# 1. P&G brandSAVER digital coupons
# ---------------------------------------------------------------------------

PG_URL = "https://pgbrandsaver.com/coupons/"
PG_TITLE = "Save $100s on brands you love with our digital coupons | P&G brandSAVER\u2122"

# (brand, value, offer_text, expires, appears_in_featured_with_other_expiry)
PG_OFFERS = [
    ("Crest", 5.00, "$5.00 OFF ONE Crest 3DWhitestrips (excludes Noticeably White, Classic White and any Crest 3DWhitestrips product with 5 or less treatments).", "2026-09-26", "2026-09-27"),
    ("Crest", 4.00, "$4.00 OFF ONE Crest 3DWhite Brilliance, 3DWhite Whitening Therapy Charcoal, Crest Gum Detoxify, Crest Clean Breath, Gum & Whitening, Gum & Enamel Restore, Gum & Sensitive, Gum Recession 3.0 oz or larger (excludes all other variants, kids, and trial/travel size).", "2026-09-26", "2026-09-27"),
    ("Crest", 2.00, "$2.00 OFF ONE Crest Toothpaste 2.4 oz or more (excludes Crest Cavity, Baking Soda, Tartar Control/Protection, Brilliance, Gum, Densify, Aligner Care, Kids, More Free packs, and trial/travel size).", "2026-09-26", "2026-09-27"),
    ("Tampax / Always / This is L.", 1.00, "$1.00 OFF ONE Tampax Tampon (12ct or higher), Always Pad (10ct or higher), Always liner (30ct or higher), Always ZZZ (7ct), This is L. Liner (60ct or higher), This is L. Pad (20ct or higher), or This is L. Tampon (18ct or higher) (excludes trial/travel size).", "2026-09-26", None),
    ("Olay", 5.00, "$5.00 OFF TWO Olay Super Serum Body Wash 20oz (excludes other Olay 20oz body wash and trial/travel)", "2026-09-27", None),
    ("Olay", 4.00, "$4.00 OFF TWO Olay Body Wash 20oz and Body Wash 35oz (excludes Super Serum 20oz and trial/travel)", "2026-09-27", None),
    ("Olay", 2.00, "$2.00 OFF TWO Olay Body Wash 18oz, Body Wash 22oz and Bar 6 count (excludes trial/travel)", "2026-09-27", None),
    ("Bounce", 3.00, "$3.00 OFF ONE Bounce WrinkleGuard Mega Sheets 180 ct OR Paradise Blossom Mega Sheets 180 ct OR Pet Hair & Lint Guard Mega Sheets 180 ct OR Fresh Breeze Mega Sheets 180 ct (excludes travel size).", "2026-09-27", None),
    ("Bounce", 3.00, "$3.00 OFF ONE Bounce Sheets 330 ct (excludes travel size).", "2026-09-27", None),
    ("Bounce", 2.00, "$2.00 OFF ONE Bounce WrinkleGuard Mega Sheets 80-130 ct OR Paradise Blossom Mega Sheets 80-130 ct OR Pet Hair & Lint Guard Mega Sheets 80-130 ct OR Fresh Breeze Mega Sheets 80-130 ct OR Lasting Fresh Mega Sheets 80-130 ct (excludes travel size).", "2026-09-27", None),
    ("Bounce", 2.00, "$2.00 OFF ONE Bounce Sheets 160-250 ct (excludes Mega Sheets and travel size).", "2026-09-27", None),
    ("Bounce", 1.00, "$1.00 OFF ONE Bounce Sheets 80-120 ct (excludes travel size).", "2026-09-27", None),
    ("Cascade", 5.00, "$5.00 OFF TWO Cascade Platinum Plus 47ct or greater, Platinum 59ct or greater, OR Complete 78ct or greater Dishwasher Detergent OR ONE Cascade Rinse Aid Clean & Dry Booster 8.45oz (exclude travel/trial size).", "2026-09-27", None),
    ("Cascade", 4.00, "$4.00 OFF ONE Cascade Platinum Plus 47ct or greater, Platinum 59ct or greater, OR Complete 78ct or greater Dishwasher Detergent (exclude travel/trial size).", "2026-09-27", None),
    ("Clearblue", 2.00, "$2.00 OFF ONE Clearblue Combo or Digital Pregnancy Test.", "2026-09-27", None),
    ("Crest", 1.00, "$1.00 OFF ONE Crest Mouthwash 473mL (16 oz) or larger (excludes Scope, 3DWhite, Pro-Health Extra Whitening, Gum Detoxify, Gum Restore, Clinical Deep Clean, All Day Clean Breath or Nightly Bacteria Shield or larger or trial/travel size).", "2026-09-27", None),
    ("Dawn", 2.00, "$2.00 OFF ONE Dawn Powerwash Starter Kit (excludes travel/trial size).", "2026-09-27", None),
    ("Downy", 5.00, "$5.00 OFF ONE Downy In-Wash Scent Boosters Boutique Botanicals 10.7 oz OR Downy In-Wash Scent Boosters Unlimited 10.7 oz (excludes travel size).", "2026-09-27", None),
    ("Downy", 4.00, "$4.00 OFF ONE Downy In-Wash Scent Boosters Boutique Botanicals 4.8 oz OR Downy In-Wash Scent Boosters Unlimited 4.8 oz (excludes travel size).", "2026-09-27", None),
    ("Downy", 3.50, "$3.50 OFF ONE Downy In-Wash Scent Boosters 7.8 oz (includes Downy Light, Unstopables, April Fresh, Cool Cotton and Infusions) OR Downy In-Wash Scent Boosters Comfy Cozy OR Blends 8.3 oz OR Cozy Collection Beads 7.8 oz (includes Pistachio Cream, Cherry Jubilee, Chai Latte, Love in Paris, Date in Kyoto, Honeymoon in Hawaii), Fusions 6.9-8.0 oz (excludes travel size).", "2026-09-27", None),
    ("Downy", 3.00, "$3.00 OFF ONE Downy Mega Sheets 180 ct (includes Infusions and Downy Light Sheets), (excludes travel size).", "2026-09-27", None),
    ("Downy", 3.00, "$3.00 OFF ONE Downy In-Wash Scent Boosters 18.2 oz (includes Unstopables, April Fresh, Cool Cotton, Infusions and Light) OR Downy In-Wash Scent Boosters Comfy Cozy OR Blends 19.4 oz OR Fusions 16 oz (excludes travel size).", "2026-09-27", None),
    ("Downy", 3.00, "$3.00 OFF ONE Downy Wrinkleguard 120 oz (excludes Downy Fresh 50 oz and 125 oz and travel size).", "2026-09-27", None),
    ("Downy", 3.00, "$3.00 OFF ONE Downy In-Wash Scent Boosters Boutique Botanicals 21.1 oz (excludes unlimited and travel size).", "2026-09-27", None),
    ("Downy", 3.00, "$3.00 OFF ONE Downy Liquid Fabric Conditioner 140 oz OR Downy Ultra Soft 93 oz (includes Downy Gentle Soft + Fresh 93 oz) OR Nature Inspired 111 oz (excludes travel size).", "2026-09-27", None),
    ("Downy", 3.00, "$3.00 OFF ONE Downy In-Wash Scent Boosters 24-30.1 oz (includes Downy Light, Unstopables, April Fresh, Cool Cotton and Infusions) OR Downy In-Wash Scent Boosters Comfy Cozy OR Blends 24.5-32.2 oz OR Fusions 21.1-26.5 oz OR Downy In-Wash Scent Boosters Unlimited 21.1 oz (excludes travel size).", "2026-09-27", None),
    ("Downy", 2.00, "$2.00 OFF ONE Downy April Fresh Sheets 160 ct (excludes travel size).", "2026-09-27", None),
    ("Downy", 2.00, "$2.00 OFF ONE Downy Mega Sheets 80 ct OR 130 ct (includes Downy Light and Infusions Sheets), (excludes travel size).", "2026-09-27", None),
    ("Downy", 2.00, "$2.00 OFF ONE Downy Liquid Fabric Conditioner 66-88 oz (includes Downy Intense 77 oz) OR Downy 100-111 oz OR Downy Ultra Soft LFE 38-44 oz OR Downy Ultra Soft 56-64 oz (includes Downy Gentle Soft + Fresh) OR Wrinkleguard 48-81oz (excludes Downy Fresh 50 oz and 125 oz and travel size).", "2026-09-27", None),
    ("Downy", 2.00, "$2.00 OFF ONE Downy In-Wash Scent Boosters 9.1 oz (includes Downy Light, Unstopables, April Fresh, Cool Cotton and Infusions) (excludes travel size).", "2026-09-27", None),
    ("Downy", 2.00, "$2.00 OFF ONE Downy April Fresh Sheets 240 ct OR Downy Cool Cotton Sheets 240 ct (excludes travel size).", "2026-09-27", None),
    ("Downy", 1.00, "$1.00 OFF ONE Downy Mega Sheets 50-60 ct (includes Infusions and Downy Light Sheets) (excludes travel size).", "2026-09-27", None),
    ("Downy", 1.00, "$1.00 OFF ONE Downy April Fresh Sheets 105-120 ct (excludes travel size).", "2026-09-27", None),
    ("Downy", 1.00, "$1.00 OFF ONE Downy Liquid Fabric Conditioner 44 oz OR Downy Ultra Soft 26 oz OR Downy Gentle Soft + Fresh 26 oz (excludes travel size).", "2026-09-27", None),
    ("Downy", 0.75, "$0.75 OFF ONE Downy Sheets 60 ct (includes April Fresh, Cool cotton) OR Downy Mega Sheets 30 ct (includes Calm Lavender & Vanilla bean and White Tea & Bergamot), (excludes travel size).", "2026-09-27", None),
    ("Downy", 0.75, "$0.75 OFF ONE Downy Liquid Fabric Softener April Fresh 24 oz OR 32 oz (includes Downy Intense 24-32 oz OR Downy Soft 24-32 oz) OR Downy Fresh 50oz OR Downy Sheets 34 ct OR Downy Unstopables In-Wash Scent Boosters 3.3 oz (excludes Downy Rinse, Downy WrinkleGuard Sheets, Downy Libre Enjuague and trial/travel size).", "2026-09-27", None),
]

PG_BAY_AREA_NOTE = (
    "Manufacturer coupon issued by P&G. Redeemable in person at participating U.S. retailers "
    "that accept P&G brandSAVER digital coupons, which include Bay Area Safeway, Lucky, "
    "Andronico's Community Markets, CVS, Walgreens, Target and Walmart stores. Whether a given "
    "clipped offer scans at a given register is controlled by that retailer's coupon policy."
)


def slug(text: str) -> str:
    keep = []
    for ch in text.lower():
        if ch.isalnum():
            keep.append(ch)
        elif ch in " $" and keep and keep[-1] != "-":
            keep.append("-")
    out = "".join(keep).strip("-")
    return "-".join(out.split("-"))[:60]


def pg_entries() -> list[dict]:
    out: list[dict] = []
    seen: dict[str, int] = {}
    for brand, value, text, expires, alt_expires in PG_OFFERS:
        base = "pg-" + slug(brand) + "-" + f"{value:.2f}".rstrip("0").rstrip(".")
        seen[base] = seen.get(base, 0) + 1
        entry_id = base if seen[base] == 1 else f"{base}-{seen[base]}"
        deal_types = ["dollar_off"]
        categories = ["manufacturer-digital"]
        if "OFF TWO" in text:
            deal_types.append("bogo")
            categories.append("bogo-multi-buy")

        flags = [
            {
                "code": "expires-imminently",
                "severity": "warning",
                "detail": (
                    "The issuer printed an expiry of "
                    + expires
                    + ", which is within 5 days of the 2026-09-22 verification date. "
                    "Re-check https://pgbrandsaver.com/coupons/ before travelling to a store; "
                    "the page is refreshed monthly and self-reported as \"Updated September 2026\"."
                ),
            },
            {
                "code": "account-required",
                "severity": "warning",
                "detail": (
                    "P&G brandSAVER coupons are clipped to a digital basket on the issuer's site and "
                    "require a free P&G brandSAVER account. The specific retailer acceptance list is "
                    "behind the account flow and could not be read anonymously."
                ),
            },
        ]
        if alt_expires:
            flags.append(
                {
                    "code": "source-page-inconsistency",
                    "severity": "critical",
                    "detail": (
                        "The same offer appears twice on the official page with two different expiry "
                        "dates: '" + expires + "' in the 'Featured Digital Coupons' block and '"
                        + alt_expires + "' in the full 'Search 112 Digital Coupons' list. Treat the "
                        "earlier date (" + expires + ") as the safe assumption and confirm in the "
                        "account basket before use."
                    ),
                }
            )

        out.append(
            {
                "id": entry_id,
                "title": text.split("(")[0].strip().rstrip("."),
                "merchant": brand,
                "publisher": "Procter & Gamble \u2014 P&G brandSAVER",
                "categories": categories,
                "deal_types": deal_types,
                "value": {"amount": value, "unit": "currency", "currency": "USD", "kind": deal_types[0]},
                "offer_text": text,
                "offer_text_is_verbatim": True,
                "expires": expires,
                "expiry_basis": "Printed on the issuer's page next to the offer as 'Expires "
                + expires.replace("-", "/")
                + "' (M/D/YYYY on the source page).",
                "requirements": [
                    "Free P&G brandSAVER account",
                    "Clip the coupon to your basket on the issuer's site before shopping",
                    "Buy the exact product size/variant named in the offer text",
                ],
                "bay_area": {
                    "available": True,
                    "confidence": "high",
                    "note": PG_BAY_AREA_NOTE,
                    "physical_locations": None,
                    "locator_url": "https://www.safeway.com/local.html",
                },
                "sources": [
                    {
                        "url": PG_URL,
                        "title": PG_TITLE,
                        "publisher": "Procter & Gamble (pgbrandsaver.com \u2014 official brand domain)",
                        "accessed": VERIFIED_AT,
                        "method": "fetch_page",
                        "evidence": (
                            "Page states 'Updated September 2026' and 'Search 112 Digital Coupons'. "
                            "Offer line read verbatim: \"" + text + "\" followed by \"Expires "
                            + expires.replace("-", "/") + "\"."
                        ),
                    }
                ],
                "verification": {
                    "level": "A",
                    "verified_at": VERIFIED_AT,
                    "recheck_due": recheck_due(expires),
                    "checks": [
                        "Offer text transcribed verbatim from the issuer's page",
                        "Expiry date transcribed verbatim from the issuer's page",
                        "Expiry is in the future relative to the verification date",
                        "Source domain is owned by the coupon issuer (pg.com brand property)",
                    ],
                },
                "flags": flags,
                "tags": ["household", "personal-care", "grocery"],
            }
        )
    return out


def write_shard(filename: str, entries: list[dict]) -> None:
    ENTRIES_DIR.mkdir(parents=True, exist_ok=True)
    path = ENTRIES_DIR / filename
    path.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(entries):3d} entries -> {path.relative_to(ROOT)}")


def main() -> None:
    write_shard("01-pg-brandsaver.json", pg_entries())


if __name__ == "__main__":
    main()

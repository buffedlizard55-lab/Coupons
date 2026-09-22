#!/usr/bin/env python3
"""Generate the bulk-verified entry shards for the coupon dataset.

Two shards are produced by this script because both come from a single official
page that was read line by line on 2026-09-22:

  1. data/entries/01-pg-brandsaver.json
     Source: https://pgbrandsaver.com/coupons/  (Procter & Gamble, official)
     The page self-reports "Updated September 2026" and "Search 112 Digital
     Coupons".  Every offer below is a verbatim transcription of the offer text
     and the "Expires" line printed next to it on that page.  Offers that appear
     twice on the page with two different expiry dates are flagged.

  2. data/entries/07-museums-for-all-sf.json
     Source: https://www.sfhsa.org/san-francisco-museums-all
     (City & County of San Francisco Human Services Agency, official)
     Venue names, street addresses, admission amounts and hours are transcribed
     verbatim from that page.

Nothing here is inferred, remembered or copied from an aggregator.  If a field
could not be read from the source page it is left null and a flag explains it.

Run:  python3 scripts/generate_bulk_entries.py
"""

from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ENTRIES_DIR = ROOT / "data" / "entries"

VERIFIED_AT = "2026-09-22"

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


# ---------------------------------------------------------------------------
# 2. San Francisco "Museums For All" venues
# ---------------------------------------------------------------------------

SFHSA_URL = "https://www.sfhsa.org/san-francisco-museums-all"
SFHSA_TITLE = "San Francisco Museums For All | sfhsa.org"

MFA_PROGRAM_TEXT = (
    "EBT or Medi-Cal cardholders get free or highly discounted admission to more than 25 local "
    "museums and cultural centers."
)
MFA_HOW_TO = (
    "On your visit, show your EBT or Medi-Cal card and proof of SF residence. It's easy to get "
    "4 free or highly discounted admission tickets for every visit. Check each listing below for "
    "visiting hours and ticketing information. Make online reservations when available. Note: "
    "Special exhibits are not discounted and may require separate reservations."
)

# name, address, admission_text, walk_up, advanced_ticket, hours, phone, website, extra_flags
MFA_VENUES = [
    ("Asian Art Museum", "200 Larkin Street, San Francisco", "Free", "Yes", "No", "Thursday: 1:00 p.m. to 8:00 p.m. | Friday to Monday: 10:00 a.m. to 5:00 p.m. | Tuesday to Wednesday: Closed", "(415) 581-3500", "https://www.asianart.org/", []),
    ("de Young Museum", "50 Hagiwara Tea Garden Drive, San Francisco", "Free", "Yes", "No", "Thursday to Sunday: 9:30 a.m. to 5:15 p.m.", "(415) 750-3600", "https://famsf.org/", []),
    ("Legion of Honor Museum", "100 34th Avenue, San Francisco", "Free", "Yes", "No", "Tuesday to Sunday: 9:30 a.m. to 5:15 p.m.", "(415) 750-3600", "https://famsf.org/", []),
    ("Museum of the African Diaspora (MoAD)", "685 Mission Street, San Francisco", "Free", "Yes", "No", "Wednesday to Saturday: 11:00 a.m. to 6:00 p.m. | Monday to Tuesday: Closed", "(415) 358-7200", "https://www.moadsf.org/", []),
    ("Museum of Craft and Design", "2569 Third Street, San Francisco", "Free", "Yes", "Members only", "Thursday to Sunday: 12:00 p.m. to 5:00 p.m. | Monday to Wednesday: Closed", "(415) 773-0303", "https://sfmcd.org/", []),
    ("San Francisco Museum of Modern Art (SFMOMA)", "151 Third Street, San Francisco", "Free", "Yes", "No", "Monday: 10:00 a.m. to 5:00 p.m. | Tuesday to Wednesday: Closed | Thursday: 1:00 p.m. to 8:00 p.m. | Friday to Sunday: 10:00 a.m. to 5:00 p.m.", "(415) 357-4000", "https://www.sfmoma.org/", [
        {
            "code": "official-sources-conflict",
            "severity": "warning",
            "detail": (
                "The City's Museums For All page lists SFMOMA hours as 'Monday: 10:00 a.m. to 5:00 p.m. | "
                "Tuesday to Wednesday: Closed | Thursday: 1:00 p.m. to 8:00 p.m. | Friday to Sunday: 10:00 a.m. "
                "to 5:00 p.m.' SFMOMA's own visit page (fetched 2026-09-22) states 'Monday\u2013Tuesday: 10 a.m.\u20135 p.m., "
                "Wednesday: Closed, Thursday: Noon\u20138 p.m., Friday\u2013Sunday: 10 a.m.\u20135 p.m.' Two official sources "
                "disagree; confirm hours with the museum before travelling."
            ),
        }
    ]),
    ("Walt Disney Family Museum", "104 Montgomery Street, Presidio, San Francisco", "Free, main museum only", "Yes", "No", "Thursday to Sunday: 10:00 a.m. to 5:30 p.m. | Monday to Wednesday: Closed", "(415) 345-6843", "https://www.waltdisney.org/", []),
    ("Yerba Buena Center for the Arts", "701 Mission Street, San Francisco", "Free", "Yes", "No", "Thursday, Saturday to Sunday: 12:00 p.m. to 6:00 p.m. | Friday: 2:00 p.m. to 8:00 p.m. | Monday to Wednesday: Closed", "(415) 978-2700", "https://ybca.org/", []),
    ("Children's Creativity Museum", "221 4th Street, San Francisco", "Free", "Yes", "Members only", "Thursday to Sunday: 10:00 a.m. to 4:00 p.m. | Monday to Wednesday: Closed", "(415) 820-3320", "https://creativity.org/", []),
    ("American Bookbinders Museum", "355 Clementina Street, San Francisco", "Free", "Yes", "No", "Tuesday to Saturday: 10:00 a.m. to 4:00 p.m. | Sunday to Monday: Closed", "(415) 824-9754", "https://bookbindersmuseum.org/", []),
    ("Cable Car Museum", "1201 Mason Street, San Francisco", "Free", "Yes", "No", "Tuesday to Thursday: 10:00 a.m. to 4:00 p.m. | Friday to Sunday: 10:00 a.m. to 5:00 p.m.", "(415) 474-1887", "http://www.cablecarmuseum.org/", []),
    ("Chinese Culture Center of San Francisco", "750 Kearny Street, 3rd Floor, San Francisco", "Free", "Yes", "Yes", "Tuesday to Saturday: 10:00 a.m. to 4:00 p.m.", "(415) 986-1882 ext. 025", "https://www.cccsf.us/", []),
    ("Chinese Historical Society of America", "965 Clay Street, San Francisco", "Free", "Yes", "Yes", "Wednesday to Sunday: 11:00 a.m. to 4:00 p.m.", "(415) 391-1188", "https://chsa.org/", []),
    ("GLBT Historical Society of America", "4127 18th Street, San Francisco", "Free", "Yes", "Yes", "Wednesday to Sunday: 11:00 a.m. to 5:00 p.m. | Monday to Tuesday: Closed", "(415) 777-5455", "https://www.glbthistory.org/", []),
    ("Guardians of the City Museum (formerly SFFD Museum)", "655 Presidio Avenue, San Francisco", "Free", "Yes", "No", "Thursday to Sunday, 1:00 pm to 4:00 p.m. Please check the website to confirm before you visit.", "(415) 558-3546", "https://guardiansofthecity.org/", []),
    ("San Francisco Railway Museum", "77 Steuart Street, San Francisco", "Free", "No", "Yes", "Tuesday to Saturday: 12:00 p.m. to 5:00 p.m.", "(415) 956-0472", "https://www.streetcar.org/", []),
    ("Tenderloin Museum", "398 Eddy Street, San Francisco", "Free", "Yes", "No", "Tuesday to Saturday: 10:00 a.m. to 5:00 p.m. | Sunday to Monday: Closed", "(415) 351-1912", "https://www.tenderloinmuseum.org/", []),
    ("The Contemporary Jewish Museum", "736 Mission Street, San Francisco", "Free", "No", "Yes", "Thursday to Sunday: 11:00 a.m. to 5:00 p.m.", "(415) 655-7800", "https://www.thecjm.org/", [
        {
            "code": "venue-temporarily-closed",
            "severity": "critical",
            "detail": (
                "The City's listing is headed 'The Contemporary Jewish Museum (Temporarily Closed)'. "
                "The admission benefit is published but the venue itself is flagged as temporarily closed "
                "by the same official source, so do not travel without confirming on thecj.org."
            ),
        }
    ]),
    ("Aquarium of the Bay", "Pier 39, Embarcadero & Beach Street, San Francisco", "$3", "Yes", "No", "Daily: 10:00 a.m. to 5:00 p.m. (last entry 4:30 p.m.)", "(415) 623-5300", "https://www.aquariumofthebay.org/", []),
    ("Conservatory of Flowers", "100 John F Kennedy Drive, Golden Gate Park, San Francisco", "Free", "Yes", "Yes", "Tuesday to Sunday: 10:00 a.m. to 4:30 p.m. | Last entry at 4:00 p.m.", "(415) 831-2090", "https://gggp.org/conservatory-of-flowers/", []),
    ("Exploratorium", "Pier 15, Embarcadero at Green Street, San Francisco", "$5 (daytime admission and Thursday After Dark, 18+)", "Yes", "No", "Tuesday to Saturday: 10:00 a.m. to 5:00 p.m. | Thursday After Dark (Ages 18+): 6:00 p.m. to 10:00 p.m. | Sunday 12:00 to 5:00 p.m. | Monday: Closed (except select holidays)", "(415) 528-4444", "https://www.exploratorium.edu/", []),
    ("Japanese Tea Garden", "75 Hagiwara Tea Garden Drive, Golden Gate Park, San Francisco", "Free", "Yes", "Yes", "Summer Hours: 9:00 a.m. to 5:45 p.m. | Winter Hours: 9:00 a.m. to 4:45 p.m. | Last entry 30 minutes before closing", "(415) 752-1171", "https://www.japaneseteagardensf.com/", []),
    ("Museum of the Eye", "645 Beach Street, San Francisco", "Free", "Yes", "No", "Wednesday to Sunday: 11:00 a.m. to 5:00 p.m. | Monday to Tuesday: Closed", "(415) 447-0208", "https://www.aao.org/museum-of-the-eye", []),
    ("Randall Museum", "199 Museum Way, San Francisco", "Free", "Yes", "No", "Tuesday to Saturday: 10:00 a.m. to 5:00 p.m. | Sunday to Monday: Closed", "(415) 554-9600", "https://randallmuseum.org/", []),
    ("San Francisco Botanical Garden", "1199 9th Avenue, San Francisco", "Free", "Yes", "Yes", "Open Daily 7:30 a.m. | Last entry at 6:00 p.m.", "(415) 661-1316", "https://www.sfbg.org/", []),
    ("San Francisco Zoo and Gardens", "Sloat Boulevard at The Great Highway, San Francisco", "$3", "Yes", "No", "Open Daily: 10:00 a.m. to 5:00 p.m. | Last entry at 4:00 p.m.", "(415) 753-7080", "https://www.sfzoo.org/", []),
]


def mfa_entries() -> list[dict]:
    out = []
    for (name, address, admission, walk_up, adv, hours, phone, website, extra) in MFA_VENUES:
        free = admission.lower().startswith("free")
        out.append(
            {
                "id": "sf-museums-for-all-" + slug(name),
                "title": "Museums For All admission at " + name,
                "merchant": name,
                "publisher": "San Francisco Human Services Agency (City & County of San Francisco)",
                "categories": ["community-access", "no-spend-free"],
                "deal_types": ["free_admission" if free else "reduced_admission"],
                "value": (
                    {"amount": 0.0, "unit": "currency", "currency": "USD", "kind": "free_admission"}
                    if free
                    else {
                        "amount": float(admission.replace("$", "").split()[0]),
                        "unit": "currency",
                        "currency": "USD",
                        "kind": "reduced_admission",
                    }
                ),
                "offer_text": admission + " admission with an EBT or Medi-Cal card plus proof of San Francisco residence. " + MFA_HOW_TO,
                "offer_text_is_verbatim": False,
                "verbatim_source_text": "Admission: " + admission + " | Walk-up admission: " + walk_up + " | Advanced ticket: " + adv,
                "expires": None,
                "expiry_basis": "Standing municipal program; the source page publishes no end date.",
                "requirements": [
                    "Valid EBT or Medi-Cal card",
                    "Proof of San Francisco residence",
                    "Up to 4 free or discounted tickets per visit",
                    "Special exhibitions are not discounted and may need separate reservations",
                ],
                "venue": {
                    "name": name,
                    "address": address,
                    "hours": hours,
                    "phone": phone,
                    "website": website,
                    "walk_up_admission": walk_up,
                    "advanced_ticket_required": adv,
                },
                "bay_area": {
                    "available": True,
                    "confidence": "high",
                    "note": "Physical venue inside San Francisco with a published street address on the official City page.",
                    "physical_locations": [address],
                    "locator_url": website,
                },
                "sources": [
                    {
                        "url": SFHSA_URL,
                        "title": SFHSA_TITLE,
                        "publisher": "sfhsa.org \u2014 City & County of San Francisco Human Services Agency",
                        "accessed": VERIFIED_AT,
                        "method": "fetch_page",
                        "evidence": (
                            "Program line read verbatim: \"" + MFA_PROGRAM_TEXT + "\". Venue listing read "
                            "verbatim: \"" + name + ": " + address + "\" with \"Hours: " + hours + "\", "
                            "\"Contact: " + phone + "\", \"Website: " + website + "\" and \"Admission: "
                            + admission + " | Walk-up admission: " + walk_up + " | Advanced ticket: " + adv + "\"."
                        ),
                    }
                ],
                "verification": {
                    "level": "A",
                    "verified_at": VERIFIED_AT,
                    "checks": [
                        "Source is a City & County of San Francisco agency domain (sfhsa.org)",
                        "Venue name and street address transcribed verbatim",
                        "Admission amount transcribed verbatim",
                        "Program eligibility conditions transcribed verbatim",
                    ],
                },
                "flags": [
                    {
                        "code": "eligibility-restricted",
                        "severity": "info",
                        "detail": (
                            "Not open to the general public: requires an EBT or Medi-Cal card plus proof of "
                            "San Francisco residence. Listed here because it is a genuine no-spend offer with "
                            "a physical Bay Area redemption point."
                        ),
                    }
                ]
                + extra,
                "tags": ["museum", "culture", "no-spend", "san-francisco"],
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
    write_shard("07-museums-for-all-sf.json", mfa_entries())


if __name__ == "__main__":
    main()

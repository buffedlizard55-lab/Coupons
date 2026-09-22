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
  Pass 5 (2026-09-22, this shard's current state): the FULL-LIST HARVEST IS
  COMPLETE.  All 10 content chunks of https://pgbrandsaver.com/coupons/ were
  retrieved live and every list-view row transcribed, giving 112 rows — exactly
  the count the page advertises in its own heading, "Search 112 Digital
  Coupons".  That equality is now pinned by TestPgHarvestCompleteness, so a
  future re-harvest that drops or invents a row fails the build.  Chunks 0-2
  re-confirmed the 36 rows transcribed in passes 1-4 with zero drift.
  Seven coupons are printed TWICE on the page with two different expiry dates
  (Crest 3DWhitestrips $5.00, Crest 3DWhite Brilliance $4.00 and Crest
  Toothpaste $2.00 at 9/26 in Featured vs 9/27 in the list; Tampax/Always/This
  is L. $1.00 at 9/26 in Featured vs 9/27 in the list; and the three Olay "OFF
  TWO" body-wash coupons at 9/27 in Featured vs 9/28 in the list).  Each is kept
  once, carrying both printed dates and a critical source-page-inconsistency
  flag; the earlier date is the one stored in `expires`.
  Pass 5 also read the page's "How to use" and FAQ sections, which changed two
  things in this shard: (a) the redemption flow is the issuer's five-step
  Coupon24 sequence, not "clip to a store loyalty card", and (b) the issuer
  publishes an explicit answer to "Which retailers accept brandSAVER™ coupons?"
  — CVS, Discount Drug Mart, Dorothy Lane Market, Food Depot, Hartig Drug
  Stores, Lagree's Food Stores, Other Avenues Coop, Western Drug Store.  The
  bay_area note in passes 1-4 asserted that Bay Area Safeway, Lucky, Andronico's,
  CVS, Walgreens, Target and Walmart accept these coupons; the issuer's own list
  names only CVS among those, so the claim was CORRECTED (confidence lowered to
  "medium", every entry now carries a retailer-list-published warning, and
  policy-pg-brandsaver-retailer-acceptance records the correction).  Nothing was
  substituted from memory or from a third-party page.
  List-view rendering artefacts are preserved, not "fixed": the cards print the
  amount glued to the copy ("$3.00OFF ONE"), "Expires9/27/2026" with no space,
  "180 ct(excludes travel size)", and two genuine issuer typos ("trial/trial
  sizes" on Secret Clinical, "TIde Rinse" on Tide Simply).  Offer text below is
  the de-glued, correctly spaced card copy; the raw artefacts are documented here
  so a reviewer comparing against the page is not misled.

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


def days_to_expiry(expires: str) -> int:
    """Whole days between the verification date and the issuer's printed expiry."""
    return (_dt.date.fromisoformat(expires) - _dt.date.fromisoformat(VERIFIED_AT)).days

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
    ("Tampax / Always / This is L.", 1.00, "$1.00 OFF ONE Tampax Tampon (12ct or higher), Always Pad (10ct or higher), Always liner (30ct or higher), Always ZZZ (7ct), This is L. Liner (60ct or higher), This is L. Pad (20ct or higher), or This is L. Tampon (18ct or higher) (excludes trial/travel size).", "2026-09-26", "2026-09-27"),
    ("Olay", 5.00, "$5.00 OFF TWO Olay Super Serum Body Wash 20oz (excludes other Olay 20oz body wash and trial/travel)", "2026-09-27", "2026-09-28"),
    ("Olay", 4.00, "$4.00 OFF TWO Olay Body Wash 20oz and Body Wash 35oz (excludes Super Serum 20oz and trial/travel)", "2026-09-27", "2026-09-28"),
    ("Olay", 2.00, "$2.00 OFF TWO Olay Body Wash 18oz, Body Wash 22oz and Bar 6 count (excludes trial/travel)", "2026-09-27", "2026-09-28"),
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
    # ---- pass 5 (2026-09-22): rows harvested from list-view chunks 3-8 ----
    ("Dreft", 3.00, "$3.00 OFF ONE Dreft Power PODS 45 ct (excludes trial/travel size).", "2026-09-27", None),
    ("Dreft", 3.00, "$3.00 OFF ONE Dreft Power PODS 25 ct (excludes trial/travel size).", "2026-09-27", None),
    ("Dreft", 3.00, "$3.00 OFF ONE Dreft Newborn Laundry Detergent 60-65 oz OR Dreft Active Baby Laundry Detergent 60-65 oz OR Dreft Free and Gentle Laundry Detergent 60-65 oz OR Dreft Pure Gentleness Laundry Detergent 60-65 oz (excludes Dreft Rinse and trial/travel size).", "2026-09-27", None),
    ("Dreft", 2.00, "$2.00 OFF ONE Dreft Power PODS 18 ct (excludes trial/travel size).", "2026-09-27", None),
    ("Dreft", 1.00, "$1.00 OFF ONE Dreft Newborn Laundry Detergent 42 oz OR Dreft Active Baby Laundry Detergent 42 oz OR Dreft Free and Gentle Laundry Detergent 42 oz OR Dreft Pure Gentleness Laundry Detergent 42 oz (excludes Dreft Rinse and trial/travel size).", "2026-09-27", None),
    ("Febreze", 5.00, "$5.00 OFF ONE Febreze Plug Scent Booster OR Febreze Scent Booster Starter Kit (excludes trial/travel size).", "2026-09-27", None),
    ("Febreze", 3.00, "$3.00 OFF ONE Febreze Bathroom 2ct or 3cts (excludes trial/travel size).", "2026-09-27", None),
    ("Fixodent", 1.00, "$1.00 OFF ONE FIXODENT ADHESIVE SINGLE, OR TWIN/TRIPLE PACK 1.4 oz or larger (excludes trial/travel size).", "2026-09-27", None),
    ("Gain", 5.00, "$5.00 OFF ONE Gain In-Wash Scent Beads 10.7-12.2 oz (excludes Gain Plus Liquid Laundry, Gain Rinse, Gain Flings, Gain Powder, Gain Liquid Fabric Softeners, Gain Sheets and trial/travel size).", "2026-09-27", None),
    ("Downy / Tide / Gain / Dreft Rinse", 5.00, "$5.00 OFF ONE Downy or Tide or Gain or Dreft Rinse 36.7oz (excludes travel size).", "2026-09-27", None),
    ("Gain", 4.00, "$4.00 OFF ONE Gain Plus Liquid Laundry Detergent 170 oz OR Gain Flings Laundry Detergent 102-112 ct OR Gain Powder Laundry Detergent 154 oz (excludes Gain Liquid Laundry Detergent, Gain Liquid Fabric Softeners, Gain Fireworks, Gain Sheets, Gain Flings 9 ct and below and travel size).", "2026-09-27", None),
    ("Gain", 4.00, "$4.00 OFF ONE Gain Plus Liquid Laundry Detergent 60 oz (excludes Gain Rinse, Gain Flings, Gain Liquid Fabric Softeners, Gain Fireworks, Gain Sheets and trial/travel size).", "2026-09-27", None),
    ("Gain", 3.00, "$3.00 OFF ONE Gain Liquid Laundry Detergent 99 oz OR 132 oz OR 144 oz (includes Gain Plus 99-117 oz) OR Gain Powder Laundry Detergent 104 oz OR 135 oz (excludes Gain Rinse, Gain Flings, Gain Liquid Fabric Softeners, Gain Fireworks, Gain Sheets and trial/travel size).", "2026-09-27", None),
    ("Gain", 3.00, "$3.00 OFF ONE Gain Flings Laundry Detergent 42 ct OR Gain Plus Flings Laundry Detergent 25 ct (includes Super Flings) (excludes Gain Liquid/Powder Laundry Detergent, Gain Liquid Fabric Softeners, Gain Fireworks, Gain Sheets, Gain Flings 9 ct and below and trial/travel size).", "2026-09-27", None),
    ("Gain", 3.00, "$3.00 OFF ONE Gain Liquid Fabric Softener 101 OR 140 oz OR Gain In-Wash Scent Boosters 16 oz OR 18.2 oz (excludes Gain Rinse, Gain Flings, Gain Liquid/Powder Laundry Detergent and trial/travel size).", "2026-09-27", None),
    ("Gain", 3.00, "$3.00 OFF ONE Gain Liquid Laundry Detergent 177-194 oz (includes Gain Plus 133-147 oz) OR Gain Powder Laundry Detergent 123 oz (excludes Gain Rinse, Gain Flings, Gain Liquid Fabric Softeners, Gain Fireworks, Gain Sheets and trial/travel size).", "2026-09-27", None),
    ("Gain", 3.00, "$3.00 OFF ONE Gain Flings Laundry Detergent 60 ct OR Gain Plus Flings 32 ct (includes Super Flings) (excludes Gain Liquid/Powder Laundry Detergent, Gain Liquid Fabric Softeners, Gain Fireworks, Gain Sheets, Gain Flings 9 ct and below and travel size).", "2026-09-27", None),
    ("Gain", 3.00, "$3.00 OFF ONE Gain Liquid Laundry Detergent 107-113 oz OR Gain Powder Laundry Detergent 82 oz (excludes Gain Rinse, Gain Flings, Gain Liquid Fabric Softeners, Gain Fireworks, Gain Sheets and trial/travel size).", "2026-09-27", None),
    ("Gain", 3.00, "$3.00 OFF ONE Gain Liquid Fabric Softener 127 oz OR Gain In-Wash Scent Boosters 21.1-30.1 oz (excludes Gain Liquid/Powder Laundry Detergent, Gain Sheets and trial/travel size).", "2026-09-27", None),
    ("Gain", 3.00, "$3.00 OFF ONE Gain Flings Laundry Detergent 76 ct OR Gain Plus Flings 45 ct (includes Super Flings) (excludes Gain Liquid/Powder Laundry Detergent, Gain Liquid Fabric Softeners, Gain Fireworks, Gain Sheets, Gain Flings 9 ct and below and travel size).", "2026-09-27", None),
    ("Downy / Tide / Gain Rinse", 3.00, "$3.00 OFF ONE Downy or Tide or Gain Rinse 62 oz (excludes travel size).", "2026-09-27", None),
    ("Downy / Tide / Dreft / Gain Rinse", 3.00, "$3.00 OFF ONE Downy or Tide or Dreft or Gain Rinse 48 oz (excludes travel size).", "2026-09-27", None),
    ("Gain", 2.50, "$2.50 OFF ONE Gain In-Wash Scent Boosters 4.3-6.5 oz (excludes Gain Rinse, Gain Flings, Gain Liquid/Powder Laundry Detergent and trial/travel size).", "2026-09-27", None),
    ("Gain", 2.50, "$2.50 OFF ONE Gain Plus Flings 9 ct (includes Super Flings) (excludes Gain Liquid/Powder Laundry Detergent, Gain Liquid Fabric Softeners, Gain Fireworks, Gain Sheets, travel size).", "2026-09-27", None),
    ("Downy / Tide / Gain Rinse", 2.50, "$2.50 OFF ONE Downy or Tide or Gain Rinse 16 oz (excludes travel size).", "2026-09-27", None),
    ("Gain", 2.00, "$2.00 OFF ONE Gain Liquid Fabric Softener 72 oz OR Gain In-Wash Scent Boosters 7.8-9.1 oz OR Gain Sheets 180 ct (excludes Gain Rinse, Gain Flings, Gain Liquid/Powder Laundry Detergent and trial/travel size).", "2026-09-27", None),
    ("Gain", 2.00, "$2.00 OFF ONE Gain Liquid Laundry Detergent 60-65 oz (excludes Gain Plus Liquid Laundry, Gain Rinse, Gain Flings, Gain Powder, Gain Liquid Fabric Softeners, Gain Fireworks, Gain Sheets and trial/travel size).", "2026-09-27", None),
    ("Gain", 2.00, "$2.00 OFF ONE Gain Liquid Laundry Detergent 81-88 oz OR Gain Plus Liquid Laundry Detergent 60-66 oz OR Gain Powder Laundry Detergent 63 oz (excludes Gain Rinse, Gain Flings, Gain Liquid Fabric Softeners, Gain Fireworks, Gain Sheets and trial/travel size).", "2026-09-27", None),
    ("Gain", 2.00, "$2.00 OFF ONE Gain Liquid Fabric Softener 71 oz OR 100 oz OR Gain Sheets 240 ct OR Mega Sheets 130 ct (excludes Gain Rinse, Gain Flings, Gain Liquid/Powder Laundry Detergent and trial/travel size).", "2026-09-27", None),
    ("Gain", 2.00, "$2.00 OFF ONE Gain Flings Laundry Detergent 24 ct (excludes Gain Liquid/Powder Laundry Detergent, Gain Liquid Fabric Softeners, Gain Fireworks, Gain Sheets, Gain Flings 9 ct and below and trial/travel size).", "2026-09-27", None),
    ("Gain", 2.00, "$2.00 OFF ONE Gain Flings Laundry Detergent 31 ct OR Gain Plus Flings 18 ct (includes Super Flings) (excludes Gain Liquid/Powder Laundry Detergent, Gain Liquid Fabric Softeners, Gain Fireworks, Gain Sheets, Gain Flings 9 ct and below and trial/travel size).", "2026-09-27", None),
    ("Gain", 1.00, "$1.00 OFF ONE Gain Liquid Fabric Softener 44 oz OR Gain Sheets 105-120 ct OR Gain Mega Sheets 60 ct (excludes Gain Rinse, Gain Flings, Gain Liquid/Powder Laundry Detergent and trial/travel size).", "2026-09-27", None),
    ("Gain", 1.00, "$1.00 OFF ONE Gain Liquid Laundry Detergent 39-46 oz OR Gain Powder Laundry Detergent 30 oz (excludes Gain Rinse, Gain Flings, Gain Liquid Fabric Softeners, Gain Fireworks, Gain Sheets and trial/travel size).", "2026-09-27", None),
    ("Gain", 1.00, "$1.00 OFF ONE Gain Flings Laundry Detergent 14-19 ct (excludes Gain Liquid/Powder Laundry Detergent, Gain Liquid Fabric Softeners, Gain Fireworks, Gain Sheets, travel size).", "2026-09-27", None),
    ("Gillette", 2.00, "$2.00 OFF ONE Gillette Clinical Antiperspirant or Deodorant (excludes trial/travel size).", "2026-09-27", None),
    ("Gillette", 2.00, "$2.00 OFF ONE Gillette SkinShield Clear Gel 3.8oz Antiperspirant/Deodorant.", "2026-09-27", None),
    ("Gillette", 1.00, "$1.00 OFF ONE Gillette Clear Gel Antiperspirant/Deodorant (excludes Gillette SkinShield Clear Gel 3.8oz and trial/travel size).", "2026-09-27", None),
    ("Ivory", 1.00, "$1.00 OFF ONE Ivory Body Wash 27oz or Larger (Gentle or Moisturizing) OR Bar Soap 4ct or Larger.", "2026-09-27", None),
    ("Ivory", 1.00, "$1.00 OFF ONE Ivory Body Lotion 18oz or Larger.", "2026-09-27", None),
    ("Mr. Clean", 3.00, "$3.00 OFF ONE Mr. Clean Shower & Tub Starter Kit or Mr Clean Magic Eraser 6ct or Higher.", "2026-09-27", None),
    ("Mr. Clean", 2.00, "$2.00 OFF ONE Mr. Clean Multi-Surface Cleaner 41oz or Larger(excludes trial/travel size).", "2026-09-27", None),
    ("Mr. Clean", 2.00, "$2.00 OFF ONE Mr. Clean Magic Eraser 3ct or Larger (excludes Trial/Travel Size).", "2026-09-27", None),
    ("Mr. Clean", 1.00, "$1.00 OFF ONE Mr. Clean Multi-Surface Cleaner 21 or 23oz OR Mr. Clean Clean Freak Starter Kit (excludes trial/travel size).", "2026-09-27", None),
    ("Old Spice", 5.00, "$5.00 OFF THREE Old Spice 1ct 5.0oz Bar Soaps.", "2026-09-27", None),
    ("Old Spice", 2.00, "$2.00 OFF ONE Old Spice Body Wash Pump 25oz or Larger (excludes Super Hydration and trial/travel size).", "2026-09-27", None),
    ("Old Spice", 1.00, "$1.00 OFF ONE Old Spice Antiperspirant/Deodorant or Body Wash (excludes Items under 2oz, Gift-packs, High Endurance or Base Antiperspirant/Deodorant, Whole Body Deodorant, Sprays, Super Hydration, Alchemist, Bar Soap, Pump Body Wash 25oz or larger and trial/travel size).", "2026-09-27", None),
    ("Oral-B", 1.00, "$1.00 OFF ONE Oral-B Glide Manual Floss OR Oral-B Expanding Floss OR Oral-B Glide Floss Picks OR Satin Floss (Excludes Essential Floss, Oral-B Fresh Mint Picks and trial/travel size).", "2026-09-27", None),
    ("Oral-B", 1.00, "$1.00 OFF ONE Oral-B Adult Manual Toothbrush (excludes Oral-B Dual Clean, Oral-B Essential and Oral-B Pulsar toothbrushes).", "2026-09-27", None),
    ("Oral-B", 10.00, "$10.00 OFF ONE Oral-B iO Rechargeable Electric Toothbrush iO7 only.", "2026-09-27", None),
    ("Oral-B", 10.00, "$10.00 OFF ONE Oral-B iO Refills OR Oral-B non-iO Replacement Brush Heads 5ct or greater.", "2026-09-27", None),
    ("Oral-B", 10.00, "$10.00 OFF ONE Oral-B iO Rechargeable Electric Toothbrush iO2, iO Kids, iO2 Starter Kit, iO3, iO4, or iO5.", "2026-09-27", None),
    ("Oral-B", 5.00, "$5.00 OFF ONE Oral-B iO Refills OR Oral-B non-iO Replacement Brush Heads 2ct or greater.", "2026-09-27", None),
    ("Secret", 3.00, "$3.00 OFF ONE Secret Whole Body Deodorant (excludes trial/travel size).", "2026-09-27", None),
    ("Secret", 3.00, "$3.00 OFF ONE Secret Clinical Antiperspirant/Deodorant (excludes trial/trial sizes).", "2026-09-27", None),
    ("Secret", 1.00, "$1.00 OFF ONE Secret Fresh, Outlast, Aluminum Free, or Dry Spray Antiperspirant/Deodorant (excludes trial/travel size).", "2026-09-27", None),
    ("Swiffer", 10.00, "$10.00 OFF ONE Swiffer PowerMop Starter Kit (excludes trial/travel size).", "2026-09-27", None),
    ("Swiffer", 5.00, "$5.00 OFF ONE Swiffer Sweeper Deluxe or 8ct 6ft Duster Starter Kits (excludes 3ft Dusters, short handle Dusters, 1-2ct Dusters and trial/travel size).", "2026-09-27", None),
    ("Swiffer", 2.00, "$2.00 OFF ONE Swiffer Refill Product OR 3ft Duster Starter Kit (includes 20ct or Larger Dry and Wet cloth refills, 10ct or Larger XL Dry and Wet cloth refills, 5ct or Larger PowerMop pad refills, 12 or Larger WetJet pad refills, 2ct or Larger PowerMop and WetJet solution refills, and 6ct or larger Duster refills).", "2026-09-27", None),
    ("Tide", 4.00, "$4.00 OFF ONE Tide Liquid Laundry Detergent 148 oz OR 158 oz OR 166oz OR Tide Powder Laundry Detergent 151 oz (excludes Tide EVO, Tide Rinse, Tide PODS, Tide Simply Laundry Detergent, Tide Detergent 10 oz and trial/travel size).", "2026-09-27", None),
    ("Tide", 4.00, "$4.00 OFF ONE Tide PODS Laundry Detergent 77-85 ct OR 102 ct TO 112 ct OR Tide Power PODS 57 ct TO 63 ct (excludes Tide EVO, Tide Clean Boost Rinse, Tide Liquid/Powder Laundry Detergent, Tide Simply and trial/travel size).", "2026-09-27", None),
    ("Tide", 3.00, "$3.00 OFF ONE Tide EVO Laundry Detergent 42 ct (excludes trial and travel size).", "2026-09-27", None),
    ("Tide", 3.00, "$3.00 OFF ONE Tide Liquid Laundry Detergent 117-142 oz OR 149 oz OR Tide Powder Laundry Detergent 108-132 oz (excludes Tide EVO, Tide Rinse, Tide purclean, Tide PODS, Tide Simply Laundry Detergent, Tide Detergent 10 oz and trial/travel size).", "2026-09-27", None),
    ("Tide", 3.00, "$3.00 OFF ONE Tide Liquid Laundry Detergent 73-84 oz (excludes Tide EVO, Tide Rinse, Tide purclean, Tide Powder, Tide PODS, Tide Simply Laundry Detergent, Tide Detergent 10 oz and trial/travel size).", "2026-09-27", None),
    ("Tide", 3.00, "$3.00 OFF ONE Tide PODS Laundry Detergent 32 ct OR 42 ct (excludes 35 ct) OR Tide Power PODS 25 ct (excludes Tide EVO, Tide Rinse, Tide Liquid/Powder Laundry Detergent, Tide Simply and trial/travel size).", "2026-09-27", None),
    ("Tide", 3.00, "$3.00 OFF ONE Tide PODS Laundry Detergent 43-57 ct OR Tide Power PODS 32 ct (excludes Ultra OXI PODS, Tide EVO, Tide Clean Boost Rinse, Tide Liquid/Powder Laundry Detergent, Tide Simply and trial/travel size).", "2026-09-27", None),
    # ---- pass 5 (2026-09-22): rows harvested from list-view chunk 8 (Tide tail, PURE Zzzs, Vicks, ZzzQuil) ----
    ("Tide", 3.00, "$3.00 OFF ONE Tide Laundry Detergent 92-105 oz OR Tide Powder Laundry Detergent 77-85 oz (excludes Tide EVO, Tide Rinse, Tide purclean, Tide PODS, Tide Simply Laundry Detergent, Tide Detergent 10 oz and trial/travel size).", "2026-09-27", None),
    ("Tide", 3.00, "$3.00 OFF ONE Tide PODS Laundry Detergent 76 ct OR Tide Ultra Oxi PODS 57 ct OR Tide Power PODS 45 ct (excludes Tide EVO, Tide Clean Boost Rinse, Tide Liquid/Powder Laundry Detergent, Tide Simply and trial/travel size).", "2026-09-27", None),
    ("Tide", 2.00, "$2.00 OFF ONE Tide EVO Laundry Detergent 16 ct (excludes trial and travel size).", "2026-09-27", None),
    ("Tide", 2.00, "$2.00 OFF ONE Tide Laundry Detergent 55-63 oz OR Tide purclean 63 oz OR Tide Powder Laundry Detergent 50-55 oz (excludes Tide EVO, Tide PODS, Tide Simply Laundry Detergent, Tide Detergent 10 oz and trial/travel size).", "2026-09-27", None),
    ("Tide", 1.00, "$1.00 OFF ONE Tide Simply Laundry Detergent 59-117 oz (excludes TIde Rinse, Tide Detergent, Tide PODS and trial/travel size).", "2026-09-27", None),
    ("Tide", 1.00, "$1.00 OFF ONE Tide PODS Laundry Detergent 11 ct TO 20 ct OR Tide Power PODS Laundry Detergent 9-10 ct (excludes Tide EVO, Tide Rinse, Tide Liquid/Powder Laundry Detergent, Tide Simply Laundry Detergent, Tide PODS 9 ct and below and trial/travel size).", "2026-09-27", None),
    ("Tide", 1.00, "$1.00 OFF ONE Tide Laundry Detergent 27-42 oz (excludes Tide EVO, Tide Rinse, Tide PODS, Tide purclean, Tide Simply Laundry Detergent, Tide Detergent 10 oz and trial/travel size).", "2026-09-27", None),
    ("PURE Zzzs", 1.00, "$1.00 OFF ONE PURE Zzzs product (excludes trial/travel sizes).", "2026-09-27", None),
    ("Vicks", 1.50, "$1.50 OFF TWO DayQuil, NyQuil Adult & Kids, Sinex, Vapo, Vapo Drops, VapoCOOL Drops, (excludes 1oz, 4oz, 2ct & 8ct DayQuil or NyQuil products, NyQuil Adult Chews, VapoCOOL Drops 12 & 18ct, VapoRub 12g, Vapo Pops Kids, and trial/travel sizes).", "2026-09-27", None),
    ("ZzzQuil", 1.00, "$1.00 OFF ONE ZzzQuil product (excludes Nasal Strips, Pure Zzzs, and trial/travel size).", "2026-09-27", None),
    ("ZzzQuil", 1.00, "$1.00 OFF ONE ZzzQuil Nasal Strips product (excludes trial/travel sizes).", "2026-09-27", None),
]

PG_RETAILER_LIST_VERBATIM = (
    "CVS, Discount Drug Mart, Dorothy Lane Market, Food Depot, Hartig Drug Stores, "
    "Lagree's Food Stores, Other Avenues Coop, Western Drug Store"
)

PG_BAY_AREA_NOTE = (
    "Manufacturer coupon issued by P&G and presented through the Coupon24 app at the register. "
    "The issuer's own page answers \"Which retailers accept brandSAVER(TM) coupons?\" with an "
    "explicit list — \"" + PG_RETAILER_LIST_VERBATIM + "\" — and adds \"we're working on adding "
    "more!\". Of those eight named retailers, only CVS was confirmed during this project to operate "
    "stores inside the nine-county Bay Area (see the Walgreens/CVS entries in this dataset); the "
    "others could not be confirmed as Bay Area chains and no Bay Area store is asserted for them. "
    "Whether a clipped coupon scans at a given register is controlled by that retailer's coupon "
    "policy, and the issuer publishes no per-store participation list."
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
                    + ", which is " + str(days_to_expiry(expires)) + " day"
                    + ("s" if days_to_expiry(expires) != 1 else "")
                    + " after the " + VERIFIED_AT + " verification date. "
                    "Re-check https://pgbrandsaver.com/coupons/ before travelling to a store; "
                    "the page is refreshed monthly and self-reported as \"Updated September 2026\"."
                ),
            },
            {
                "code": "account-required",
                "severity": "warning",
                "detail": (
                    "P&G brandSAVER coupons are added to a digital basket on the issuer's site, sent to "
                    "the third-party Coupon24 app and scanned at the register. That requires a free P&G "
                    "brandSAVER account, a Coupon24 account, and a phone number: the issuer states "
                    "'brandSAVER\u2122 coupons can only be accessed through one verified phone number per "
                    "account'."
                ),
            },
            {
                "code": "retailer-list-published",
                "severity": "warning",
                "detail": (
                    "The issuer publishes an explicit acceptance list — '" + PG_RETAILER_LIST_VERBATIM
                    + "' — and no Bay Area Safeway, Lucky, Andronico's, Walgreens, Target or Walmart "
                    "appears on it. Only CVS among the eight could be confirmed to operate Bay Area "
                    "stores. An earlier version of this dataset asserted those other chains accepted "
                    "brandSAVER coupons; the issuer's page does not support that and it was corrected on "
                    "2026-09-22 (pass 5). Confirm at the register before relying on this coupon."
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
                    "Create a free P&G brandSAVER account (issuer's step 1: 'Create a P&G brandSAVER\u2122 Account')",
                    "Download the Coupon24 app and set up a Coupon24 account (issuer's step 2)",
                    "Link the Coupon24 account to the brandSAVER account (issuer's step 3)",
                    "Add the coupon to your basket and send your brandSAVER coupons to the Coupon24 app (issuer's step 4)",
                    "Use the app to scan your digital coupons at checkout (issuer's step 5: 'Use your app to scan your digital coupons at checkout. Voil\u00e0!')",
                    "Shop at one of the retailers the issuer names in its acceptance list (see the Bay Area note)",
                    "Buy the exact product size/variant named in the offer text",
                ],
                "bay_area": {
                    "available": True,
                    "confidence": "medium",
                    "note": PG_BAY_AREA_NOTE,
                    "physical_locations": None,
                    "locator_url": "https://www.cvs.com/store-locator",
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

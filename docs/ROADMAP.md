# Roadmap

Next work, in priority order. Each item states what to do, why it matters, and what "done"
looks like — including the evidence that must be captured, because an entry without a citation
cannot be merged.

Current state: **128 verified offers, 9 documented rejections, 141 citations across 30 domains,
223 flags**, all verified 2026-09-22.

---

## Priority 1 — close the California Academy of Sciences gap

**Why first:** a headline Golden Gate Park attraction has *no* verified free-admission entry,
while 26 smaller Museums For All venues do. It is the most visible hole in the dataset.

**Do:**
1. Retrieve `calacademy.org/plan-your-visit`, the tickets/admission pages, and the Academy's
   accessibility and membership pages.
2. Establish, from the Academy's own text: whether Museums For All pricing applies and at what
   price; whether neighbourhood/free days still run and on which days; whether the transit
   discount exists; what the general admission price ladder is.
3. Record each as its own entry with `venue` (address, hours, phone) transcribed.

**Done when:** at least one level-A entry exists for the Academy, or the absence of any free or
reduced program is itself recorded as a level-A policy note quoting the Academy's published
admission terms. The existing `UNVERIFIED` rejection record is then either promoted or updated
with the retrieved evidence.

## Priority 2 — re-harvest the manufacturer coupon block

**Why:** all 36 P&G brandSAVER coupons expired 26–27 September 2026, within days of
verification. This is the dataset's most time-sensitive asset.

**Do:**
1. Re-read `pgbrandsaver.com/coupons/` (and the featured block, which published *different*
   expiries for three Crest coupons — see `source-page-inconsistency`).
2. Update the `PG_OFFERS` transcription in `scripts/generate_bulk_entries.py` and re-run it; CI
   proves the shards match the generator.
3. Add the same pattern for the other manufacturer hubs: General Mills (Betty Crocker, Pillsbury,
   Cheerios), Kellanova, Unilever, Nestlé/Purina, Huggies/Kimberly-Clark, Colgate, Clorox,
   Johnson & Johnson, and Coupons.com's printable index (whose deep URLs 404 — use the homepage
   "View all Printable Coupons" link).

**Done when:** the block's printed expiries are at least 30 days out, each entry keeps its
verbatim evidence, and any publisher-side expiry contradiction is flagged rather than averaged.

## Priority 3 — headless-browser verification path

**Why:** six large merchants are currently unverifiable by plain HTTP: Raley's (JS shell), CVS
(anti-bot interstitial), Pizza Hut, KFC, Papa Johns and Domino's (client-rendered or 404 offer
pages). This converts several "no entry at all" gaps into level-A entries.

**Do:**
1. Add an optional Playwright mode to `scripts/verify_links.py` (or a sibling
   `scripts/verify_rendered.py`) that waits for network idle and dumps the rendered DOM text.
2. Gate it behind a CI input so the weekly job stays fast; run it monthly or on demand.
3. Store rendered-page evidence the same way as static evidence, with method `fetch_page` and a
   note that the page was rendered.

**Done when:** at least Raley's current circular and one quick-service restaurant's live offers
page are cited from their rendered official pages.

## Priority 4 — Lucky Supermarkets and the ethnic grocers

**Why:** Lucky, 99 Ranch Market, H Mart, Mitsuwa and Nijiya have dense Bay Area store networks
and none is verified. Lucky's `foru-guest.html` path 404s, and 99 Ranch was only ever seen via
third-party code aggregators (rejected).

**Do:** start from each retailer's own homepage and follow its offers/weekly-ad/rewards links;
do not search for "<brand> coupons". Record store counts and the official store locator.

**Done when:** each retailer either has a level-A/B entry from its own domain, or an explicit
note recording that no official coupon program could be located (which is itself useful — it
tells a shopper to stop looking).

## Priority 5 — enumerate Bay Area store addresses

**Why:** chain entries currently link to official locators because locator pages are
JavaScript-driven. Addresses would enable a map view and a "near me" filter.

**Do:** capture addresses from the retailers' own store pages or their locator JSON endpoints
(never from an aggregator), store them under `bay_area.physical_locations`, and add a
per-county filter to the site.

**Done when:** the top 10 chains in the dataset have verified Bay Area store lists with county
tags, and the site filters by county.

## Priority 6 — East Bay, South Bay and North Bay institutions

**Why:** coverage outside San Francisco is chain-level only.

**Do:** verify, from each institution's own site: Oakland Museum of California, Bay Area
Discovery Museum (Sausalito), San Jose Museum of Art / The Tech Interactive / Children's
Discovery Museum, Sonoma County Museum, Lawrence Hall of Science, Berkeley Art Museum / PFA,
Cal Performances, and municipal free-day calendars. Check each against the nine-county
definition in `data/meta.json`.

**Done when:** every county in the definition has at least one independently verified local
institution, or a recorded note explaining why not.

## Priority 7 — birthday freebies, verified properly

**Why:** every birthday claim found in this pass was third-party. Starbucks' Birthday Reward is
verified from official terms (with a `partial-capture` flag on the Green-level wording); Denny's
"free birthday Grand Slam" is **not** on the issuer's BoothBucks page and was rejected; the
McDonald's birthday/first-order claim conflicts with the official rewards ladder and was
rejected.

**Do:** verify from each issuer's own rewards terms: Krispy Kreme, Jamba, Baskin-Robbins,
Panera, Chick-fil-A, Yogurtland, Cold Stone, TGI Fridays. Where the terms are silent, record the
silence instead of the folk claim.

**Done when:** a `birthday` tag exists in `data/meta.json`, every entry carrying it cites
official rewards terms, and the rejected birthday claims list what was checked.

## Priority 8 — authenticated social review workflow

**Why:** the brief asked for Facebook/Instagram research; neither can be crawled anonymously.
Social is also where fabricated coupons concentrate, so the workflow must be evidence-first.

**Do:** define a submission form (post URL, poster, date, the brand's official confirmation URL,
a screenshot) and a reviewer checklist; accept an offer only when the *issuer's* page confirms
it. Social stays a lead source, never a citation — enforced by
`tests/test_data.py → NON_OFFICIAL_DOMAINS`.

**Done when:** `docs/METHODOLOGY.md §1` documents the workflow and at least one social-sourced
lead has been promoted or rejected through it, with the audit trail committed.

## Priority 9 — weekly verification with a public health signal

**Why:** `.github/workflows/verify.yml` already produces `reports/link-check.json` and files a
`link-rot` issue on new failures, but the result is not visible on the site.

**Do:** publish a small health badge in the site header ("166/167 citations resolving as of
<date>") generated from the last link-check report; open an issue automatically per failing
domain; track time-to-fix.

**Done when:** the site header shows the last check date and counts, sourced from a committed
report or a Pages-build step that runs the checker.

## Priority 10 — adjacent categories with physical redemption

**Why:** natural extensions that already have Bay Area physical redemption points and official
publishers.

**Do:** Clipper/BART/Muni fare programs and discounts; Costco and Chevron/Safeway fuel pricing;
UPSIDE-style fuel cash back; library book-sale calendars; municipal utility rebates; California
state park passes (e.g. library-lended passes); transit-linked museum discounts like FAMSF's $3
offer.

**Done when:** each new category has at least three level-A entries with venue or locator data.

---

## Backlog (smaller, still worth doing)

- **Resolve the CVS ExtraCare contradiction** by requesting the current Program Rules PDF; until
  then both thresholds stay quoted with the `official-sources-conflict` flag.
- **Resolve the FAMSF first-Tuesday/de Young hours contradiction** by contacting FAMSF press or
  reading the ticketing calendar directly; the flag stays until an official answer exists.
- **Complete the Starbucks Birthday Reward capture** (Green-level baseline sentence and the list
  of what the reward covers) and remove `partial-capture`.
- **Re-read the truncated FAMSF transit-discount passage** to capture the full terms.
- **Find the live Costco offer channel** (app → Warehouse tab) and document the cycle from a
  Costco-published page rather than community scans.
- **Mollie Stone's store list** — `molliestones.com/stores/` 404s; locate the official list and
  add addresses. Also re-check the stale 2025 voucher expiry in its rewards terms.
- **Define Rainbow Grocery's NOBAWC acronym and Helping Hands eligibility** from the co-op
  directly; both are currently flagged as undefined/unpublished.
- **Add `docs/SOURCES.md` diffing to CI** so a citation change always shows up in review.
- **Add an OpenGraph/Twitter card and a favicon** to `index.html` for sharing.
- **Add a printable one-page view** (the stylesheet already has `@media print` rules) for
  shoppers without a phone at the register.
- **i18n**: Spanish and Chinese translations of the UI for the highest-need Bay Area audiences.
  Offer text stays verbatim in English, since that is what the issuer publishes.

## Maintenance schedule

| Cadence | Job | Owner |
| --- | --- | --- |
| Weekly (Mon 09:00 UTC) | `.github/workflows/verify.yml` re-fetches all 167 cited URLs; files `link-rot` issues for new failures | GitHub Actions |
| Monthly | Re-harvest manufacturer coupon hubs (Priority 2); re-check every dated offer in the dataset | Maintainer |
| Quarterly | Re-verify level-B programs for changes in mechanics; re-read the policy notes (Trader Joe's, insert landscape) | Maintainer |
| On demand | Headless-browser pass over the JS-only merchants (Priority 3) | Maintainer |

## Definition of done for any new entry

1. `sources[]` with url, title, publisher, accessed date, method, and a verbatim `evidence`
   passage.
2. `verification.level` justified, with at least two specific `checks`.
3. `expires` and `expiry_basis` — a real published date, or `null` with the basis stated.
4. `bay_area` determination with confidence, and a venue address, a store list, or an official
   locator.
5. `value` following the canonical `{amount, unit, currency, kind}` schema, with `amount: null`
   rather than an estimate when the issuer publishes no figure.
6. Flags for every irregularity found, at the right severity.
7. `python3 scripts/build_site.py` and `python3 -m unittest discover -s tests` both pass.

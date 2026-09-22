# Methodology

How every line in this dataset was produced and checked. Verification date: **2026-09-22**.

The short version: an offer is published here only if the party that must honour it publishes
it, the text was read from that party's own page on the verification date, the passage read is
stored verbatim as evidence, and anything irregular about it is flagged rather than fixed.

---

## 1. Source hierarchy

The single most important rule in the project. Sources are ranked, and only tier 1 may establish
an offer.

| Tier | Source type | Examples | May establish an offer? |
| --- | --- | --- | --- |
| 1 | The issuer's own website, app store listing, published terms of use, or an official microsite | `pgbrandsaver.com`, `kellanovaus.com/us/en/coupons.html`, `safeway.com/foru-guest.html`, `starbucks.com/terms/rewards`, `jimmyjohns.com/terms-and-conditions`, `getpgoffer.com` | **Yes** |
| 2 | The issuer's corporate newsroom or investor-relations pages publishing program terms | `ir.chipotle.com`, `news.baskinrobbins.com`, `generalmills.com/news` | **Yes**, for the program it announces (dated press releases are re-checked like any page) |
| 3 | Coupon media and deal journalists | The Krazy Coupon Lady, MoneyPantry | No — only to establish *which channels exist*, recorded as level-C policy notes |
| 4 | Aggregators, cashback portals, promo-code sites | Coupons.com promo-code pages, simplycodes, couponcabin, valuecom, dealigg | **Never.** Used only as evidence inside a rejection record |
| 5 | Social media and forums | Facebook, Instagram, Reddit, TikTok | **Never.** Leads only; every lead was then verified on a tier-1/2 domain or rejected |
| 6 | Model knowledge / memory | — | **Never.** Explicitly prohibited by `data/meta.json → dataset.no_hallucination_policy` |

Tier 4 and 5 sources are enumerated in `tests/test_data.py → NON_OFFICIAL_DOMAINS`. Citing one
as the source of an available offer **fails the test suite**, so the rule cannot be broken by
accident in a later edit.

### Why social media is leads-only

Facebook and Instagram require authentication, so their content is not retrievable by an
anonymous crawler: no post was read and therefore none is cited. Reddit was read, and produced
exactly two leads — the `getpgoffer.com` P&G × Costco rebate (verified as an official P&G
microsite and **included**) and Costco Instant Savings cycle dates (not confirmable on any
Costco page and therefore **excluded**). Social platforms are also the dominant distribution
channel for fabricated coupons and gift-card giveaways, so treating a post as a source would
import that risk directly. The full reasoning is in the entry
`policy-social-media-sourcing`.

## 2. Verification levels

Recorded on every entry as `verification.level`.

| Level | Meaning | Count |
| --- | --- | --- |
| **A** | Offer text, value and expiry were read verbatim from the issuer's own official page on the verification date. | 85 |
| **B** | The program or policy was confirmed on the issuer's official page, but the specific rotating offers behind it require an app, an account or an in-store visit and could not be read anonymously. No individual offer is asserted. | 14 |
| **C** | Only third-party evidence was found. Kept **only** in `10-excluded-unverified.json` and `11-policy-notes.json`, never presented as a usable coupon. | 2 |

Level B exists because pretending otherwise would be a hallucination of a different kind:
Safeway for U, Target Circle, Costco Instant Savings and the quick-service restaurant apps all
publish real offers that are generated per account and per store. The honest record is
"this program is official and this is how it works", not "here are its offers".

The test suite additionally requires that:

- a level-A entry cites at least one official (non-third-party) domain;
- a level-B entry states in its own checks or flags *why* the offers could not be enumerated;
- an entry whose only retrieval method was a search-engine snippet of the issuer's page carries
  the flag `retrieval-via-search-snippet`, so it never implies a direct fetch it did not do
  (16 entries disclose this).

## 3. Retrieval methods

Stored per citation as `sources[].method`.

| Method | Meaning |
| --- | --- |
| `fetch_page` | Live retrieval of the official page; the page title and quoted text were captured. |
| `web_search` | Search-engine retrieval of the official page; the quoted text is the snippet returned **from the official domain**. Always paired with the `retrieval-via-search-snippet` disclosure flag. |
| `official_document` | A document published by the issuer: terms of use, program rules, advertised circular. |

Each citation also stores `url`, `title`, `publisher`, `accessed` (date) and `evidence` — the
verbatim passage that was read. The evidence string is what the "Show the evidence that was
read" control reveals on every card and in the Sources view, so a reviewer can compare the
offer text against the passage it came from without re-reading a whole page.

## 4. Line-by-line procedure

For each candidate offer:

1. **Identify the issuer.** Who has to honour this? If the answer is "a coupon site", stop —
   the claim goes to the excluded shard.
2. **Find the issuer's own page.** Prefer the offer's canonical location (a brand coupon hub, a
   program-rules page, a rewards terms page, a published circular).
3. **Retrieve and transcribe.** Offer text, value, expiry, conditions, exclusions and, where
   published, address and hours are transcribed verbatim. `offer_text_is_verbatim` is set `false`
   when the text had to be assembled from more than one part of the page, and the raw passage is
   kept in `verbatim_source_text` (the Kellanova coupon cards do this: each is a heading, a brand
   line and an 'on any ONE/TWO' line joined in page order).
4. **Check the dates.** Compare every published expiry, purchase window and event date against
   the verification date. Expired, closed and not-yet-live states are recorded, never hidden.
5. **Check physical redemption.** Confirm the offer can be redeemed in person within the
   nine-county Bay Area, and transcribe the address, hours or phone number the issuer publishes.
   If only an official locator exists, link to it instead of inventing addresses.
6. **Look for contradictions.** Compare the issuer's pages against each other and against any
   agency page describing the same program. When they disagree, quote both and raise a
   `critical` flag. Do not pick a winner.
7. **Record how it was checked.** At least two `verification.checks` per entry, each a specific
   statement of what was compared or confirmed (enforced by tests).
8. **Flag everything irregular.** See §5.
9. **Otherwise reject it**, into `10-excluded-unverified.json`, with `why_rejected`,
   `urls_checked` (each with its own evidence), `risk` and `what_would_verify_it`.

## 5. Flag taxonomy

207 flags across the dataset: **12 critical, 142 warning, 53 info**.

| Severity | Meaning | Examples in this dataset |
| --- | --- | --- |
| `critical` | Do not rely on this without resolving the problem first. | P&G/Costco rebate purchase window closed before verification; two official CVS pages state different reward thresholds; three Crest coupons printed twice on one official P&G page with two different expiries; a retailer announcing a discount that is "not live yet"; Costco item-level offers not verifiable anonymously; a 19-month-old Raley's circular used as the only source; Colgate's own pages disagree about whether coupons exist; documented scam vectors (Trader Joe's impersonators, insert-site staleness, social 'coupon' density) |
| `warning` | Material caveat. | Expiry not published; account or app required; source retrieved only via search snippet; source page carries a stale date; partial capture of a terms page; availability varies by store; paid membership required; affiliate parameters on outbound links |
| `info` | Context for a reviewer that does not undermine the offer. | Age-restricted purchase; small fixed value; program replaced an older birthday offer; benefit is a payment-method change rather than a discount |

The 12 critical flags are listed in full on the site's **Irregularities** view and in
`docs/VERIFICATION-LOG.md §5`.

## 6. Bay Area definition

The nine counties used throughout are the standard nine-county Bay Area definition (the list used
by the region's transit and metro agencies) — a fixed official list rather than an invented one:

**Alameda, Contra Costa, Marin, Napa, San Francisco, San Mateo, Santa Clara, Solano, Sonoma.**

`data/meta.json → bay_area_county_notes` records how deeply each county is actually covered,
which is uneven: San Francisco is covered in depth (independents, co-ops, and every chain
locator that resolves there); Alameda, Contra Costa, San Mateo, Santa Clara, Marin, Sonoma,
Solano and Napa are covered mainly through chain-level programs. No offer was invented to
balance the map.

## 7. Value schema

Every `value` object has exactly four keys, so the site can label and sort without guessing:

```json
{ "amount": 1.0, "unit": "currency", "currency": "USD", "kind": "dollar_off" }
```

- `unit` ∈ `currency | percent | points`
- `kind` ∈ `dollar_off | percent_off | rebate | free_item | member_price | rewards_credit | points`
- `amount` is `null` when the issuer publishes no figure — a "cash back ladder" with no single
  stated amount is stored as `null`, never estimated.
- `free_item` may carry a non-zero amount **only** when the issuer publishes it as a maximum
  value cap and that figure appears verbatim in `offer_text` (Starbucks' "single free
  customization, up to a $2 maximum value"). The test suite enforces this.

## 8. Expiry handling

`expires` is an ISO date exactly as published, or `null`. `expiry_basis` records *why* that date
was chosen ("Printed expiry on the coupon as published on 2026-09-22", "Standing loyalty
program", "Rolling 7-day expiry printed in the offer's own footnote"). Rebates carry a separate `purchase_window`
because the qualifying-purchase deadline and the submission deadline are different things — the
P&G × Costco rebate is the case in point: purchases 2026-08-24 → 2026-09-20 (closed),
submissions until 2026-10-31 (open).

The site derives status at view time from the visitor's clock, so nothing needs a redeploy to
retire: `Active` → `Expires soon` (≤ 7 days) → `Expired`, plus `Window closed` and
`Not redeemable yet`.

## 9. Bulk shards and reproducibility

One shard is large enough to be generated rather than hand-written: 36 P&G brandSAVER coupons.
`scripts/generate_bulk_entries.py` builds it from the transcription taken on the verification date
(the brand, value, offer text and printed expiry read from pgbrandsaver.com), with provenance
stored on every entry and collision-safe IDs. A second bulk generator (26 SF Museums For All
venues) was removed from this script when the project was rescoped to products on 2026-09-22;
its code and data are preserved in `archive/rescoped-2026-09-22/`. The generator is deterministic: CI re-runs it and fails if the committed
shards no longer match, so the bulk data cannot silently drift from its transcription.

## 10. Build and enforcement

```bash
python3 scripts/build_site.py            # validate → data/coupons.json, assets/data/coupons.js, docs/SOURCES.md, _site/
python3 scripts/build_site.py --check    # fail if generated files are stale
python3 -m unittest discover -s tests    # 46 tests
python3 scripts/verify_links.py          # re-fetch every citation (72 unique URLs) → reports/link-check.json
```

`build_site.py` refuses to emit a site if any entry is missing a citation, an evidence passage,
a verification level, a Bay Area determination or a well-formed flag. The test suite then
enforces the sourcing rules (§1), the level rules (§2), the value schema (§7), the Bay Area
rules, the absence of placeholder text, and — via `tests/test_site_render.js` running the real
front-end in a DOM shim with the clock pinned to 2026-10-05 — that the site actually renders
every offer, filters correctly, labels expired offers as expired, and routes all six views.

`.github/workflows/pages.yml` builds, tests and publishes on every push to `main`.
`.github/workflows/verify.yml` re-runs the integrity tests on every push and pull request and,
every Monday, re-fetches all citations and files a `link-rot` issue when something outside the
documented link-rot log stops resolving.

## 11. What was deliberately not done

- No offer was taken from memory, from a training corpus, or from a "typical" value for a
  brand. If it was not read on 2026-09-22, it is not here.
- No expiry was estimated for an offer that publishes none.
- No store address was invented for a chain whose locator is JavaScript-driven; the official
  locator is linked instead.
- No attempt was made to reconcile two official pages that disagree; both are quoted and the
  conflict is flagged.
- No rejected claim was quietly deleted. All fifteen remain published with their reasoning, because
  a shopper who has seen the claim needs to find the rebuttal.

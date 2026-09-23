# Roadmap

Next work, in priority order. Each item states what to do, why it matters, and what "done"
looks like — including the evidence that must be captured, because an entry without a citation
cannot be merged.

Current state after **pass 6 (2026-09-22)**: **227 verified product offers, 20 documented
rejections, 265 citations across 72 domains, 612 flags (20 critical, 497 warning, 96 info)**, every line re-checked this date. Scope:
**product coupons only** — no events, museums or venue admission (see
`archive/rescoped-2026-09-22/`).

---

## Priority 1 — monthly manufacturer re-harvest (and finish the P&G page)

**Why first:** the dataset's value is perishable. All 36 P&G brandSAVER coupons expire
26–27 September 2026; the 8 Kellanova printables carry no published expiry; the P&G page itself
says **"Search 112 Digital Coupons"** — only 36 were transcribed, so 76+ live manufacturer
coupons sit one careful pass away. This is the single biggest expansion *and* retention lever.

**Status after pass 5 (2026-09-22):** DONE for P&G. All 10 content chunks of `pgbrandsaver.com/coupons/` were retrieved live and every row transcribed — 112 rows, exactly the page's advertised "Search 112 Digital Coupons" headline, with zero drift on the 36 previously transcribed. Seven expiry contradictions newly documented (Crest ×3, Tampax/Always ×1, Olay ×3: 9/26 vs 9/27 and 9/27 vs 9/28). The issuer's own FAQ was also read and revealed an explicit eight-retailer acceptance list (CVS, Discount Drug Mart, Dorothy Lane Market, Food Depot, Hartig Drug Stores, Lagree's Food Stores, Other Avenues Coop, Western Drug Store) — only CVS overlaps with the Safeway/Lucky/Andronico's/Walgreens/Target/Walmart claim from passes 1–4 — so every P&G entry was corrected (confidence medium, locator repointed to CVS, retailer-list-published warning added, policy note `policy-pg-brandsaver-retailer-acceptance` records the correction). The 112-row equality is now pinned by `TestPgHarvestCompleteness`. The front-end expiry bug (`daysUntil` using T23:59:59 + Math.round making yesterday round to 0) was found because the new Mollie Stone's 4-Items-on-the-4th entry (expires 2026-10-04) rendered as "Expires today" on pinned date 2026-10-05 and was fixed to UTC-midnight floor.

Kellanova: page re-fetched whole in pass 4 (8/8 cards matched, headline still 8/$7.00) but in pass 5 the same URL intermittently served the grid unpopulated (headline tokens unresolved, print control "PRINT COUPONS0") — client-rendered via Quotient.com. Flagged `coupon-grid-not-re-readable` rather than treated as retracted. A new live Kellanova offer was also verified: $1 off two products via Barcode Buck$ (expires 9/30/26) at promotions.kellanovaus.com, with its own terms page — added as `kellanova-barcode-bucks-1-off-two`.

P&G Back to School rebates: three tiers ($25/$15/$5) verified from pgbrandsaver.com/rebates/ and r192963.pg.promosvcs.com/en-US/terms — purchase window Jul 1–Sep 30, 2026, submission due Oct 14, 2026. Tier 1 carries an internal contradiction ($50 in body vs $75 in heading/bold requirement) and the terms say "two (2) ways" then list three tiers. Added as `pg-back-to-school-rebate-*` with critical one-reward-per-household flag.

Mollie Stone's: homepage and dedicated pages verified two new program mechanics — "4 Items on the 4th" (40% off, in-store one day only, next instance Sunday Oct 4 2026, confirmed weekday) and the existing Rewards page listing Sandwich/Salad/Soup clubs (buy 9 get 10th free) and weekly free item — added as three entries.

Clorox: Gift of Clean page says sold out, reward is a cleaning SERVICE (out of scope), and clorox.com/coupons/ still 404s — rejected as `excl-clorox-gift-of-clean-sold-out`.

**Do:**
1. ~~Re-read `pgbrandsaver.com/coupons/` in full~~ — DONE in pass 5: 112 rows, headline pinned, contradictions flagged, retailer list corrected.
2. ~~Re-read `kellanovaus.com/us/en/coupons.html`~~ — done in pass 4, regression observed in pass 5 and flagged. Add a headless re-check for the Quotient-powered grid.
3. Monthly re-harvest loop in `scripts/generate_bulk_entries.py` (P&G + Kellanova) is now the retention lever; let CI prove shards match. P&G side complete, Kellanova generator remains tidy.
4. Sweep the remaining manufacturer hubs: Unilever, Nestlé/Purina, Kimberly-Clark, General Mills, Campbell's, Post, Hershey, Mars, Mondelez, Colgate (see Priority 2). Clorox is now rejected (sold-out service + 404 coupons hub).

**Done when:** every dated manufacturer block's printed expiries are ≥ 30 days out, each entry
keeps verbatim evidence, and any publisher-side expiry contradiction is flagged rather than averaged.

## Priority 2 — resolve the Colgate contradiction

`colgate.com/en-us/special-offers` says **"Coupons Temporarily Unavailable — We're updating our
online coupon experience"** while `smiles.colgate.com/page/content/special-offers` advertises
"Print coupons for your favorite Colgate® oral care products". The microsite failed live fetch
twice on 2026-09-22 and is today evidenced only by a search snippet.

**Status after pass 5 (2026-09-22):** main page fetched a THIRD time in full — identical text ("Coupons Temporarily Unavailable — We're updating our online coupon experience"); smiles.colgate.com failed a fifth retrieval attempt (proxy signature error — recorded as retrieval failure, not as evidence the site is gone) and a targeted search returned only the main-site suspension page, no organic result from smiles.colgate.com. The contradiction stays flagged (not deleted) because the issuer's own page promises updated offers "soon" — until the microsite disappears or republishes, both readings must remain visible. The policy note now documents three full fetches of the main page and five failed microsite attempts.

**Do:** keep re-fetching both URLs on every monthly pass (and via headless later); if printable
coupons ever render, transcribe each as a level-A entry (brand, amount, wording, expiry) the same
way Kellanova's were.

**Done when:** the `source-page-inconsistency` critical flag on `policy-colgate-coupons-suspended`
can be removed because both pages now say the same thing — or the dataset carries Colgate's real
coupons.

## Priority 3 — headless-browser verification path

**Why:** six-plus merchants are currently unverifiable by plain HTTP: Raley's (JS shell), CVS
(anti-bot interstitial), Pizza Hut, KFC, Papa Johns, Domino's (404s), 7-Eleven deal pages (JS),
Coupons.com printable grid (login wall), Target Circle (login wall). Level B entries exist for
several of them; headless rendering + account-less scrolling converts them to level A offer
entries — or proves offers unavailable and retires the entry honestly.

**Do:** add `scripts/headless_capture.py` (Playwright, cookie-blocked) that snapshots an official
page, extracts offer-card text, and prints a transcription block to paste into a generator. Keep
it out of the data pipeline: a human (or the agent) reviews the dump before it becomes an entry.

**Done when:** at least Raley's live member deals, the Coupons.com printable index, and one QSR
deals page (KFC or Pizza Hut) have offer-level level-A entries with fetch timestamps, or each is
recorded as "checked, nothing published" in the link-rot log.

## Priority 4 — Bay Area store depth

**Why:** chain entries link to official locators instead of addresses. "Where exactly can I use
this in Oakland / San Jose / Santa Rosa?" is the project's central unanswered question.

**Do:** for P&G-accepting retailers (Safeway, CVS, Walgreens, Target) and for the independents
already listed (Mollie Stone's store list moved — find the current one), pull address lists from
the locators via the headless path, store them per-entry under `bay_area.physical_locations`, and
add a "near me" county filter on the site.

**Done when:** every available entry either lists ≥ 1 verified Bay Area street address from the
issuer or links a locator the site documents as tried-and-404.

## Priority 5 — expand the receipt-scan & rebate categories

Verified today: Checkout 51, Ibotta, P&G×Costco mail-in, Pop-Tarts Crazy Good Rewards, P&G Back to School rebates (3 tiers), Kellanova Barcode Buck$ $1-off-two. The pattern (official brand microsite, receipt upload, points on groceries) also exists
across Kellanova promotions, Nestlé and General Mills (Box Tops for Education — whose historic
`boxtops.com` domain now serves a rock band, recorded as `excl-boxtops-domain-drift`).

**Do:** fetch each program's terms page; record earning ladders verbatim; flag every account wall;
reject anything that pays out only on an online store (precedent: `excl-rkt-squishmallows-online-only-reward`).
Pass 4 did the Kellanova receipt-scan leg; pass 5 added the Kellanova Barcode Buck$ digital coupon and the P&G Back to School rebate trio: the Pop-Tarts entry now quotes its published 1-point-per-$1 ladder
verbatim from the official terms page, and the brand's legacy Scratch-Off terms (self-dated dead:
"expire on 12/31/24", play window closed 2026-09-02) were rejected as
`excl-kellanova-legacy-scratch-off-games`. Nestlé and General Mills legs still open.

**Done when:** each program entry quotes its own terms (not the app-store blurb) and the
`receipt-scan-rewards` category carries ≥ 5 entries or a limitations note saying fewer exist.

## Priority 6 — authenticated social review workflow (the original brief's Facebook/Instagram ask)

**Why:** social platforms are where fake "coupons" spread fastest, so they can be a source **only**
through a stricter path than this dataset already enforces.

**Do:** define `data/social-leads/*.json` with {post URL, brand handle, screenshot hash, the official
page that confirms the same offer, reviewer initials}; extend the tests to require that every social
lead carries an official confirmation citation before it can graduate to `data/entries/`. The dataset
schema already supports multiple sources per entry.

**Done when:** the workflow runs on new entries and the README documents that social posts are
leads, never sources.

## Priority 7 — birthday & sign-up freebie expansion (products only)

Verified so far: Starbucks (terms), McDonald's first-app McNuggets, Jimmy John's free sandwich +
birthday, Baskin-Robbins free scoop, Chipotle sign-up chips & guac. Still third-party-only:
Krispy Kreme, Jamba, Panera, Chick-fil-A, Yogurtland, Dunkin' DD Day. Verify each from its own
rewards-terms page, or record why it stays out.

## Priority 8 — public verification report + auto-issues

`.github/workflows/verify.yml` already re-checks every citation weekly, prints a summary and files
a `link-rot` issue; pass 4 added the `recheck-due` report (dataset records due within 7 days,
summary + one open issue). Remaining: wire its `reports/link-check.json` into the site header
("N of 56 citation URLs resolving as of <date>") — a CI-side change, since the sandbox has no
egress.

## Priority 9 — store-circular watch for BOGO

BOGO inventory is now 13 multi-buy manufacturer offers (Olay, Cascade, Kellanova $1-off-two, Mollie Stone's sandwich clubs) because store weekly ads are app-gated.
Raley's family (Bel Air, Nob Hill), Save Mart, Food 4 Less ("Dynamic Deals"), Costco (Instant
Savings) and Lucky publish BOGO-style in-store deals that cycle weekly. Same headless tooling,
weekly cadence, and honest `source-outdated` flags when the PDF is stale.

## Priority 10 — schema hardening for what the passes keep teaching us

- ✅ Done (pass 4): the Kellanova headline "8 coupons today, up to $7.00" is pinned by
  `TestIssuersCompletenessHeadline` — shard count, sum and per-entry evidence must all equal it.
- ✅ Done (pass 4): `verification.recheck_due` (expiry − 3 days) on all 38 dated records, policy
  documented in `data/meta.json`, enforced by `TestRecheckSchedule`, reported (and issue-filed
  weekly) by `.github/workflows/verify.yml`.
- ✅ Done (pass 5): P&G full harvest — 112 rows = "Search 112 Digital Coupons" headline pinned by `TestPgHarvestCompleteness`; seven expiry contradictions flagged; retailer acceptance list corrected from issuer's own FAQ (eight retailers, only CVS Bay Area-confirmed); front-end `daysUntil` bug fixed (yesterday was rounding to 0).
- ✅ Done (pass 5): new flag codes introduced for what passes 5 taught us: `retailer-list-published`, `retailer-acceptance-narrower-than-assumed`, `coupon-grid-not-re-readable`, `one-reward-per-household`, `terms-internal-count-mismatch`, `retailer-participation-unverified`, `recurring-one-day-sale`, `item-level-offers-in-images`, etc.
- ✅ Done (pass 5): Clorox hub re-checked a third time (still 404) and its Gift of Clean verified as sold-out SERVICE — rejected, not silently dropped.
- A `rescoped` note type so archived taxonomies stay documented without staying in the build.
- ✅ Done (pass 6): four new researched categories (home improvement/hardware/auto, sporting goods
  & outdoor, pet supplies, office/craft/hobby) with 39 verified offers; disclosure of paid
  membership enforced by `TestPass6Expansion`.

## Priority 11 — pass-6 follow-ups and next-session targets

**Re-harvest watch (dated material verified in pass 6):**
1. **Harbor Freight coupon batch (expiry 9/27/2026):** the hub cycles roughly monthly — harvest the
   October batch at go.harborfreight.com/coupons/ the same way (index + one detail page cross-check),
   replacing the three transcribed coupons and their recheck dates.
2. **Kohl's Cash earn banner (9/21–9/27/2026 window):** weekly cadence; re-read the banner's dated
   details URL and either update or let the card expire (site auto-retires it 2026-09-28).
3. **IKEA Family offer cycle (thru 10/12/2026):** re-read /us/en/offers/family-offers/ after 10/12
   for the next six-group cycle; the student 15% box ends 9/30/26 — check whether it renews.
4. **Whole Foods Days of Deals (valid through 10/6/2026):** re-read the /amazon page for the
   successor window; the extra-10% Prime perk itself is standing.
5. **REI new-member $30 bonus card (thru 11/12/2026):** watch for extension around Black Friday.

**Retrieval upgrades for pass-6 snippet-level records:** fetch the canonical program pages directly
(headless) for Ace Rewards (canonical page behind /user/login), Petco Perks, PetSmart Treats,
Michaels Rewards, Taco Bell Rewards terms, Fetch terms, Grocery Outlet /faqs (CAPTCHA body), so the
35 `retrieval-via-search-snippet` disclosures can shrink. Lucky's for U remains unverified (own 404);
Home Depot, Tractor Supply, Sephora, Ulta, Best Buy, JCPenney, Bed Bath/BuyBuy, DSW and Bay Area
mall-based chains are untested territory for the same official-first sweep. CVS remains the
headless priority from Priority 3.

## Maintenance cadence

| What | When | Tool |
| --- | --- | --- |
| Citation link check + recheck-due report | Weekly (CI) | `scripts/verify_links.py` via `verify.yml` |
| P&G + Kellanova + Coupons.com re-harvest | Monthly (or when flags say `expires-imminently`) | generator + CI |
| Restaurant/sign-up program terms | Quarterly | manual pass, same rules |
| Retail loyalty rate cards (Ace, Lowe's, AutoZone, O'Reilly, Petco, PetSmart, Michaels, Staples, REI, Kohl's) | Quarterly | manual pass, same rules |
| Dated campaign blocks (Harbor Freight batch, Kohl's Cash banner, IKEA cycles, WFM Days of Deals) | On their printed end dates (tracked by `recheck_due`) | `verify.yml` recheck report + manual re-read |
| Taxonomy review | When a category changes (e.g. this re-scope) | `data/meta.json` + tests |

## Definition of done for the project overall

A Bay Area shopper can, for any entry: read the verbatim offer text, see its printed expiry or an
explicit "none published", see a physical redemption path (venue address or working locator), open
the exact official page that was quoted, and see every known irregularity flagged on the card.
Everything not meeting that bar stays out — in `10-excluded-unverified.json` if it was checked and
refused, in `docs/ROADMAP.md` if it is simply not done yet.

# Verification log

**Verification date: 2026-09-22** (all sources accessed on this date; `accessed` is recorded per
citation in the data).
**Result after pass 4 (2026-09-22, same day): 101 verified offers · 17 documented rejections · 113 citations ·
41 domains · 208 flags (A: 85 · B: 14 · C: 2).**
(Pass 3 had reached 101 offers · 15 rejections · 112 citations · 41 domains · 207 total flags (A: 85 · B: 14 · C: 2).)
(The pass-1/2 result was 128 offers · 9 rejections · 141 citations across 30 domains, and 224 total recorded irregularities, including 49 venue-admission entries that the project owner subsequently moved out of scope; they and their evidence are preserved in `archive/rescoped-2026-09-22/`.)

This log records what was actually retrieved, what came back, what was rejected and why. It
exists so a reviewer can audit the work without repeating it, and so that a future pass can tell
"a page that has changed" from "a page that was never read".

---

## 1. Method used for this pass

1. Candidate offers were collected from the issuers' own domains (brand coupon hubs, program
   rules pages, museum visit/admission pages, municipal program listings) and, for lead-finding
   only, from search results and community threads.
2. Each official page was retrieved and the offer text, value, expiry, conditions, exclusions and
   venue details were transcribed verbatim into `data/entries/*.json`.
3. Every citation stores the URL, page title, publisher, retrieval method, access date and the
   evidence passage read.
4. Dates were compared against 2026-09-22. Expired offers, closed purchase windows and benefits
   the issuer describes as not live yet were recorded with their real status and flagged.
5. Contradictions between official pages were quoted on both sides and flagged `critical`; none
   was resolved by choosing a favourite.
6. Claims traceable only to aggregators, promo-code sites, listicles or community posts were
   moved to `data/entries/10-excluded-unverified.json` with the reason, the URLs checked, the
   risk and the evidence that would change the verdict.

Retrieval was anonymous HTTP (no accounts, no cookies, no app sessions). Where that proved
insufficient, the entry says so — see §4 and the `retrieval-via-search-snippet` flags.

## 2. Retrieval inventory — official domains

| Domain | Retrievals | Method | Outcome |
| --- | --- | --- | --- |
| `pgbrandsaver.com` | 36 | fetch_page | Full coupon list read ("Search 112 Digital Coupons"); 36 offers transcribed with printed expiries of 26–27 Sep 2026. Three Crest coupons appear twice on the same page with two different expiries → `critical` |
| `www.sfhsa.org` | 27 | fetch_page | City & County of San Francisco Museums For All listing read in full; 26 venues transcribed with published admission lines and walk-up/advance-ticket wording |
| `rainbow.coop` | 10 | fetch_page | `/contact/` read: Every Day Discounts, Honored Every Day programs, Volume Discounts, cheese bands, reusable-container credit, FSA/HSA change (effective 2/23/26), hours and phone |
| `www.sfmoma.org` | 10 | fetch_page | `/deals-discounts/`, `/free-days/`, `/visit/` read: 18 & under free, Free Family Day 2026-10-25, Museums For All, Blue Star, SFUSD staff, 45,000 sq ft always-free spaces |
| `www.exploratorium.edu` | 11 | fetch_page (9), web_search (2) | `/visit/reduced-rates` read in full (7 programs); `/visit` price ladder read via search snippet |
| `www.famsf.org` | 8 | fetch_page | `/visit/free-reduced-admission` read: Free Saturdays (9 counties), free first Tuesdays, Museums For All + $48 membership, $3 transit discount, $99 Access membership. Transit passage truncated mid-sentence → flagged |
| `www.starbucks.com` | 6 | fetch_page | `/terms/rewards/` (effective 2026-03-10) read: Free Mod Mondays, Birthday Reward windows, Reusable Cup Benefit, Digital Reload Bonus Stars, Double/Triple Star Days, program terms |
| `www.coupons.com` | 5 | fetch_page | Homepage printable index read; 5 printables transcribed. Deep printable URLs 404 → logged |
| `www.mcdonalds.com` | 3 | fetch_page | Official U.S. rewards page read: 6-tier ladder (1500/2000/3500/4000/5000/7000), free 10-pc McNuggets on first app purchase $1+, 1500 bonus points with linked card |
| `www.cvs.com` | 3 | web_search | Direct fetch of `/extracare` returned an anti-bot interstitial. Program Rules and two help pages read via search snippets of the official domain; two different reward thresholds found → `critical` |
| `www.walgreens.com` | 2 | fetch_page | myWalgreens page read: WELL20 20% weekly deal, $10 beauty reward. No published expiry; asterisk terms not machine-readable → flagged |
| `www.andronicos.com` | 2 | web_search | for U terms read via search snippet of the official domain |
| `www.safeway.com` | 1 | fetch_page | `/foru-guest.html` read (program terms, clipping, member prices). `/foru/coupons.html` 404 → logged |
| `www.albertsons.com` | 1 | web_search | for U banner list read via search snippet; Lucky absent from the list → flagged |
| `www.costco.com` | 1 | web_search | Member-only savings program wording read via search snippet; both offer URLs 404 on direct fetch → `critical` (no item-level offers asserted) |
| `www.getpgoffer.com` | 1 | fetch_page | Official P&G promotion microsite read: Buy More Save More Costco rebate, purchase window 8/24–9/20/26 (closed), submissions to 10/31/26 |
| `molliestones.com` | 1 | fetch_page | Rewards terms read: 3% back as Rewards Rebate. Terms contain a stale 2025 voucher expiry → flagged. `/stores/` 404 |
| `discoverandgo.org` | 1 | fetch_page | Program read; 30 participating Bay Area library systems transcribed from the program's own selector |
| `dennys.com` | 1 | fetch_page | `/rewards` read: BoothBucks (10 per $1, 600 → Booth Reward from 40+ items). **No birthday freebie on the page** → the circulating claim was rejected |
| `www.goodrx.com` | 1 | fetch_page | Prescription pricing model and example prices read with their URLs; "as low as" language preserved |
| `ibotta.com` | 1 | fetch_page | Corporate site read: cash-back model, retail/manufacturer offers, redemption mechanics |
| `www.raleys.com` | 1 | fetch_page | Returns a JavaScript shell ("Raley's Home Page") — no offer text in the HTML |
| `contenthandler-raleys.fieldera.com` | 1 | web_search | Official circular distribution host; the locatable circular is `022625_RBN.pdf` (26 Feb 2025, ~19 months old) → `critical`, example prices not presented as current |
| `corporate.target.com` | 1 | web_search | Official newsroom: Target Circle Deal Days 25–27 Mar 2026 (historical) → flagged as an example, not a live offer |
| `about.bankofamerica.com` | 0 | — | **Not retrieved.** The Museums on Us mechanics are cited from FAMSF's own participating-venue page instead; the entry carries `sponsor-page-not-retrieved` so the gap is visible on the card |
| `github.com` | 1 | official_document | Self-citation used by the link-rot maintenance entry only |

## 3. Retrieval inventory — third-party domains (rejection evidence and policy notes only)

| Domain | Used for |
| --- | --- |
| `thekrazycouponlady.com` | 2026 Sunday-insert landscape and the month-by-month insert schedule; SmartSource discontinuation (June 2025); P&G insert return in 2025. Recorded as a level-C policy note, never as an offer |
| `moneypantry.com` | Corroboration that SmartSource printables are gone and that FreeCoupons.com, CoolSavings, PPGazette and Mambo Sprouts are dead or redirected |
| `www.chowhound.com`, `www.mashed.com` | Two independent reports quoting Trader Joe's own statement and a PR email: no Trader Joe's coupons, manufacturer coupons accepted for other brands. Level C because `traderjoes.com` was not retrieved in this pass |
| `www.reddit.com` | Lead generation only: the `getpgoffer.com` rebate (verified and included) and Costco Instant Savings cycle dates (not verifiable on Costco → excluded) |
| promo-code aggregators (simplycodes, couponcabin, valuecom, coupons4u and similar) | Read only to document what is circulating for Round Table Pizza and 99 Ranch Market; every code found there was rejected |

## 4. Dead ends — what could not be read

All of these are recorded in the entry `policy-link-rot-observed-2026-09-22`, which the site
renders in full, so that nobody treats them as working citations.

**404 / removed on 2026-09-22:**

| URL | What came back | Replacement used |
| --- | --- | --- |
| `safeway.com/foru/coupons.html` | "Oops! Looks like this page is out of season." | `safeway.com/foru-guest.html` |
| `coupons.com/printable-grocery-coupons`, `/printables` | "Oops! Something went wrong." | `coupons.com/` → "View all Printable Coupons" |
| `costco.com/coupons.html`, `/online-offers.html` (± `EXTID` param) | "Page Not Found!" | Costco app → Warehouse tab, or the in-warehouse book |
| `calacademy.org/neighborhood-free-sundays` | "Someone pulled the plug on this page!" | none found — the Academy has **no** verified entry (Priority 1 in ROADMAP) |
| `molliestones.com/stores/` | "Page not found" | store list still unlocated |
| `luckysupermarkets.com/foru-guest.html` and `/wp/foru-guest.html` | Lucky's own 404 shell | unknown — Lucky unverified |
| `papajohns.com/order/coupons` | "LOOKS LIKE SOMEONE TOOK THE LAST SLICE" | `papajohns.com` → Deals (client-rendered) |
| `kfc.com/deals` | "There's no fried chicken on this page…" | `kfc.com` → Deals (requires a store selection) |
| `dominos.com/en/pages/order/coupons/` | Domino's "Not found" | `dominos.com` → Deals |

**Retrieved but not machine-readable:**

- `raleys.com` — JavaScript shell only; HTML body contains just the page title.
- `pizzahut.com/deals` — HTTP 200 but only empty-cart and cookie-consent markup; offers are
  client-rendered.
- `cvs.com/extracare` → `/extracare/home` — anti-bot interstitial ("One moment to bring them").

**Merchants with no official offers page found at all:** Round Table Pizza, Black Bear Diner,
Sizzler. Their codes exist only on aggregators → rejected.

**Not retrieved (deliberately):** `citypass.com` — the vendor's own price was therefore not
asserted; the three museums' own pages supply the savings claims, and their disagreement is
flagged.

## 5. Critical irregularities — 12 flags across 10 distinct issues

Reproduced from the data so this log stands alone. Each is also on the site's **Irregularities**
view and on the affected card.

1. **`pg-crest-5`, `pg-crest-4`, `pg-crest-2` — `source-page-inconsistency` (3 flags).** The same
   offer appears twice on the official P&G page with two different expiry dates: 2026-09-26 in the
   "Featured Digital Coupons" block and 2026-09-27 in the full "Search 112 Digital Coupons" list.
   The earlier date is treated as the safe assumption; the contradiction is reported, not averaged.
2. **`pg-buy-more-save-more-costco` — `purchase-window-closed`.** The qualifying purchase window
   (2026-08-24 → 2026-09-20) closed *before* the verification date. Only shoppers who already
   bought qualifying products can still submit (receipts online or postmarked by 2026-10-31). The
   site's `Window closed` status keeps it out of the default list so it cannot be mistaken for an
   available rebate.
3. **`raleys-something-extra-member-deals` — `source-outdated`.** The only locatable official
   circular is dated 26 Feb 2025 (~19 months old). Its example prices are recorded as evidence of
   program mechanics and are explicitly *not* presented as current offers.
4. **`costco-member-only-savings` — `item-level-offers-unverified`.** No Costco item, price or
   discount is asserted as current. Offers rotate on a ~4-week cycle and both public offer URLs
   404'd on 2026-09-22; only the member channels (app → Warehouse tab, in-warehouse book) expose
   them.
5. **`cvs-extracare-pharmacy-health-rewards` — `official-sources-conflict`.** Two official CVS
   pages state different thresholds for the same program: Program Rules says 10 credits → $5; the
   retail help page says 4 credits → $2. Both agree on the $50 annual cap and the 31 December
   reset. Both are quoted verbatim; neither is chosen.
6. **`rainbow-grocery-community-discount-pilot` — `announced-but-not-live`.** The retailer's own
   page states "This promotion is not live yet." Recorded with `bay_area.available = false` and
   rendered as `Not redeemable yet`, visible only so reviewers can see it was checked.
7. **`policy-trader-joes-no-coupons` — `scam-vector`.** Because Trader Joe's issues no coupons, any
   site, Facebook post or Instagram story offering Trader Joe's coupons, circulars or gift cards is
   not official, and the retailer disowns such organisations.
8. **`policy-sunday-insert-landscape-2026` — `stale-source-directories`.** "Best coupon site"
    directories still list SmartSource.com, FreeCoupons.com, CoolSavings, PPGazette and Mambo
    Sprouts; several are out of business or redirected. Any list built from those directories
    without checking each domain will contain dead or fraudulent sources.
9. **`policy-social-media-sourcing` — `scam-density`.** Social platforms are the dominant
    distribution channel for fabricated coupons and gift-card giveaways, which is why the project
    rule is "leads yes, citations no".
10. **`policy-colgate-coupons-suspended` — `source-page-inconsistency`.** Two Colgate-operated
    pages disagree about whether online coupons exist; the main site (fetched in full twice, pass 3
    and pass 4) says unavailable, the microsite that advertised printables has failed every direct
    retrieval across both passes. Recorded as a contradiction, not resolved.

*Numbering note:* items 7–8 of the pre-re-scope list (the Contemporary Jewish Museum
`venue-temporarily-closed` and the FAMSF/de Young Tuesday contradiction) retired with their venue
entries to `archive/rescoped-2026-09-22/` on 2026-09-22; this section was left describing them
until pass 4's documentation audit caught the drift (13→12 critical flags, 11→10 issues).

### 5b. Warning-level irregularities a reviewer should see

Not critical, but each one changes how an offer should be used. All are on the cards themselves.

- **McDonald's rewards tiers** — two third-party ladders circulate (2,000/4,000/6,000/10,000/14,000
  and 1,500/3,000/…), neither matching the official 1500/2000/3500/4000/5000/7000 tiers published
  on `mcdonalds.com`. The official ladder is included; the third-party versions are rejected.
- **Museums For All per-venue variation** — each of the 26 San Francisco venues sets its own
  admission amount and its own walk-up/advance-ticket rule, so the City's published line is kept
  verbatim per venue instead of being generalised (`per-venue-terms-vary`).
- **FAMSF eligibility wording** — FAMSF writes "Medi-Cal **and** food assistance (SNAP benefits)"
  while the City's listing writes "EBT **or** Medi-Cal" (`eligibility-wording-differs`). Both are
  quoted; the stricter reading is not assumed.
- **FAMSF transit discount** — the retrieved passage ends mid-sentence ("…including BART, Muni,
  Caltrain, and more"), so the full terms were not captured (`source-text-truncated`).
- **SFMOMA Blue Star Museums** — the season (third Saturday in May → first Monday in September)
  had already ended by 2026-09-22, and the current rule is free general admission for the ID
  holder plus **one** guest, not five (`seasonal-benefit-reduced`, `date-specific`).
- **SFMOMA Free Family Day** — a dated one-off event (2026-10-25) with `expires` set so the
  listing retires itself; the next Free Community Day is published as TBD.
- **Starbucks Birthday Reward** — Gold (7-day) and Reserve (30-day) windows captured verbatim; the
  Green-level baseline sentence and the list of what the reward covers fell outside the retrieved
  portion and were **not** reconstructed (`partial-capture`).
- **Walgreens** — WELL20 has no published expiry (`expiry-not-published`) and the beauty reward's
  asterisked terms were not machine-readable (`terms-not-readable`).
- **Mollie Stone's** — the rewards terms still carry a 2025 voucher expiry
  (`source-page-stale-date`) and `molliestones.com/stores/` 404s (`store-list-url-broken`).
- **Rainbow Grocery** — the "NOBAWC" acronym is used without definition
  (`eligibility-term-undefined`), Helping Hands criteria are not published
  (`eligibility-criteria-unpublished`), and the retrieved contact page yielded city/ZIP/phone but
  no street address (`address-incomplete`).
- **CityPASS** — three official museum pages quote three different savings figures (46%, "up to
  46%", "up to 45%") (`conflicting-savings-claims`), the outbound links carry affiliate tracking
  parameters (`affiliate-links`), and it is a paid product (`paid-product`).
- **Target Circle Deal Days** — the dates found (25–27 March 2026) are historical and are recorded
  as an example of the program's mechanics, not as a live offer (`example-offer-expired`).
- **Discover & Go** — passes must be reserved before the visit (`reservation-required`) and the
  program's own library selector includes systems outside the nine counties
  (`library-list-includes-non-bay-area`).
- **Retrieval transparency** — 17 entries were sourced from search-engine snippets of official
  domains rather than direct fetches and each carries `retrieval-via-search-snippet` (one added in
  pass 4: the Pop-Tarts rewards terms citation).

## 6. Rejections (17)

Full records, with URLs checked and evidence, live in `data/entries/10-excluded-unverified.json`
and on the site's **Rejected & scam watch** view.

| Record | Merchant | Verdict | Reason in one line |
| --- | --- | --- | --- |
| `excl-round-table-pizza-aggregator-codes` | Round Table Pizza | REJECTED | Codes appear only on promo-code aggregators that contradict each other (and themselves), including one scoped to Reno & Sparks, NV |
| `excl-99-ranch-simplycodes` | 99 Ranch Market | REJECTED | Aggregator-only codes; the source page states "there are no active promo codes … right now" beside the codes it lists |
| `excl-coupons-com-affiliate-promo-codes` | 23 merchants (VistaPrint, Uber Eats, Samsung, FedEx, Macy's, Walmart, …) | REJECTED for this dataset | Affiliate-published promo codes, not merchant-published; the page itself states "We might earn commissions on purchases." Also outside the physical-Bay-Area-redemption scope |
| `excl-mcdonalds-third-party-reward-tiers` | McDonald's | REJECTED | Contradicted by the issuer's own rewards page, fetched the same day |
| `excl-dennys-free-birthday-grand-slam` | Denny's | REJECTED | Absent from `dennys.com/rewards`; the program is now BoothBucks. Belongs to the retired eClub era |
| `excl-california-academy-of-sciences-free-days` | California Academy of Sciences | UNVERIFIED → out of scope | Official program page 404s; the press fact sheet is stale; third parties conflict. Superseded the same day by the product-only re-scope — venue admission is no longer tracked at all |
| `excl-costco-instant-savings-book-dates` | Costco | PLAUSIBLE BUT UNOFFICIAL | Cycle dates come from community scans, not Costco. One window independently matches P&G's official rebate window, but the dates are unauditable |
| `excl-trader-joes-online-coupons` | Trader Joe's | REJECTED | Disowned by the retailer; known phishing vector. Risk rated HIGH |
| `excl-exploratorium-free-wednesday-evenings` | Exploratorium | REJECTED | Neither the visit page nor the free/reduced admission page mentions any free evening program; the museum is closed Mondays and Thursday evenings are a paid "After Dark" session. Also out of scope after the re-scope |
| `excl-generalmills-aggregator-promo-codes` | General Mills | REJECTED (pass 3) | SimplyCodes/DealDrop/Knoji "20–40% codes" with no issuer-side counterpart; official-domain search finds no coupon hub, only a Box Tops rebate that ended 2025-11-30 |
| `excl-raleys-smartandfinal-aggregator-codes` | Raley's, Smart & Final | REJECTED (pass 3) | Knoji/ValueCom/DontPayFull "store-wide 15–85% codes"; both chains' official pages document card/app-based programs with no checkout codes |
| `excl-boxtops-domain-drift` | Box Tops for Education | REJECTED (pass 3) | boxtops.com now serves the band "The Box Tops" 2026/2027 tour site — fetched live 2026-09-22; citing it as the GM program's authority is citing a squatted domain |
| `excl-realsavings-domain-drift` | Campbell's Real Savings | REJECTED (pass 3) | realsavings.com resolves to a parked-ad shell (yfdabv11.com / rapidresultsearch.com block page) — live fetch captured the redirect |
| `excl-rkt-squishmallows-online-only-reward` | Rice Krispies Treats® | REJECTED for scope (pass 3) | Verified on Kellanova's own promotions page, but the $5 reward redeems only on Squishmallows.com — online-only, and online-only redemption is out of scope by policy |
| `excl-kraftheinz-stale-2022-campaign-page` | Kraft Heinz | REJECTED (pass 3) | kraftheinzsaveearnwin.com is official but prints its own end date "Ends 5/9/22" — a live-looking dead campaign; no current Kraft/Heinz consumer coupon hub found |
| `excl-colgate-aggregator-promo-codes` | Colgate (shop.colgate.com codes) | REJECTED (pass 4) | Five code farms (orangeoffer, DontPayFull, TenereTeam, coupons.com code pages, plus an India-market terms page as the only real "Smiles" offer) all apply recycled codes to an online store while Colgate's own U.S. coupon page — fetched twice — says coupons are unavailable |
| `excl-kellanova-legacy-scratch-off-games` | Kellanova (Cheez-It/RKT/Pop-Tarts rewards games) | REJECTED (pass 4) | Terms pages still served on the official domain carry their own disqualification: Barcode Buck$ "expire on 12/31/24", Pop-Tarts game plays "must be completed by … 9/2/26", and that game's prize redeems only at shop.poptarts.com (online-only) |

## 7. Pass log

### Pass 1 — implement and verify (complete)

Research, data construction, site, tests, CI and documentation, as described above. Deliverables:
11 shards (128 offers + 9 rejections), `data/meta.json` taxonomy and policy, generator for the
two bulk shards, build script, static site with six views, 167-URL link checker, 36 data-integrity
tests, 85 render assertions, two GitHub Actions workflows, five documents and this log.

### Pass 2 — bug, requirement and edge-case review (complete)

Reviewed the Pass-1 output line by line against the brief and against the data itself. Ten
defects found and fixed:

1. **The value schema was not uniform.** 92 entries stored `{amount, currency, kind}` and 11
   stored `{amount, unit, kind}`, so the site could not label or sort values without guessing.
   All 103 value objects were normalised to `{amount, unit, currency, kind}`, the schema was
   documented in `data/meta.json → value_schema`, the generator was taught to emit it, and four
   tests now enforce it. Edge case found while writing those tests: Starbucks Free Mod Mondays is
   a `free_item` carrying a **$2 cap**, so the naive rule "free means zero" was refined to "a
   non-zero `free_item` amount must appear verbatim in `offer_text` as the issuer's own cap".
2. **14 entries carried a single verification check.** Each was expanded to two or three specific
   and true checks — what was compared, what was cross-referenced, and what was deliberately
   *not* asserted — and the suite now requires at least two.
3. **The Costco entry asserted a policy nobody had verified.** A flag claimed "Costco does not
   accept manufacturer coupons at all", which came from model knowledge rather than a fetched
   source. Removed; the entry now verifies program mechanics only and says explicitly that the
   third-party-coupon question was not verified.
4. **The Bank of America Museums on Us entry implied an unfetched source.** Its `publisher` named
   `about.bankofamerica.com`, which was never retrieved. Publisher, checks and a new
   `sponsor-page-not-retrieved` warning now state that the mechanics come from FAMSF's
   participating-venue page and that other venues may apply different rules.
5. **Seven entries sourced from search snippets did not disclose it.** Added the
   `retrieval-via-search-snippet` warning to each, plus a test requiring that disclosure whenever
   `web_search` is the only retrieval method — so no entry can imply a direct fetch it did not do.
6. **`pages.yml` would have failed on every push.** Pages on this repository is configured
   "Deploy from a branch" (`main`, `/`) and the integration token cannot change it (403 on
   POST/PUT `/pages`). The workflow now detects `build_type` at run time: under Actions mode it
   uploads and deploys `_site`; under branch mode it explains that GitHub serves the committed
   root files. A permanently red workflow for a site that publishes correctly was the failure
   mode avoided here.
7. **Filter chips duplicated on rebuild.** `buildFilters()` appended without clearing its
   containers, so every filter click doubled the chip list. Fixed.
8. **An address was about to be completed from memory.** Rainbow Grocery's retrieved contact page
   gave city, ZIP and phone only. Rather than supplying the street address, the gap is flagged
   `address-incomplete`.
9. **Render edge cases were untested.** Added `tests/dom_shim.js` and `tests/test_site_render.js`,
   which run the real front-end against the real dataset with the clock **pinned to 2026-10-05**
   (after the verification date) so expiry logic is exercised on real entries: 85 assertions
   covering default filters, `Expired` / `Window closed` / `Not redeemable yet` labelling, chip
   toggling, flagged-only and no-spend-only filters, search hits and misses, the empty state, all
   five sort orders, all six views, flag/exclusion/citation counts checked against the data, and
   deep links lifting the filters that would hide their target. This is what found defects 7 and
   the false positive where the legitimate flag code `eligibility-term-undefined` tripped an
   "undefined value" assertion.
10. **Reproducibility confirmed.** `scripts/generate_bulk_entries.py` is byte-for-byte
    deterministic; CI re-runs it and fails if the committed shards drift.

### Pass 3 — full re-check against the original request (complete)

Requirement-by-requirement audit, with the artifact that proves each line.

| # | Original requirement | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Build a coupon site in this repository | ✅ | `index.html`, `assets/`, live at https://buffedlizard55-lab.github.io/Coupons/ |
| 2 | From official verified public sources | ✅ | 141 citations over 24 official issuer domains; the suite fails the build if an aggregator or social domain sources an offer |
| 3 | …such as Krazy Coupon Lady, Reddit, social-media searches | ✅ with a documented boundary | KCL used only as a level-C policy note (2026 insert landscape); Reddit used for leads only — one lead promoted after official verification (`getpgoffer.com`), one rejected (Costco cycle dates); Facebook, Instagram and TikTok are not retrievable anonymously, so none is cited — see `policy-social-media-sourcing` |
| 4 | Only verified official coupons; no scams or malware | ✅ | 9 documented rejections including the Trader Joe's phishing vector; a dedicated scam-watch view; zero promo-code domains cited for an available offer |
| 5 | Verify the coupons are true and not expired | ✅ | every published date compared against 2026-09-22; the site recomputes status from the visitor's clock. Audit result: **0** entries with `expires` in the past, **1** closed purchase window (flagged, hidden by default), **1** benefit the issuer says is not live (flagged, hidden by default) |
| 6 | Work line by line, no hallucinations | ✅ | 128 entries × ≥2 specific checks; `offer_text_is_verbatim` on every entry; `no_hallucination_policy` in `data/meta.json`; three Pass-2 removals of unverified assertions (Costco policy, Bank of America source, Rainbow address) |
| 7 | Flag irregularities | ✅ | 224 total flags at that time (13 critical / 136 warning / 75 info) across 105 distinct codes, all rendered on cards and in the Irregularities view — superseded by pass 3's 207 total flags (12 critical / 142 warning / 53 info) |
| 8 | Organise into researched categories (no-spend, rebate, BOGO…) | ✅ | 13 categories and 15 deal types derived from the research rather than a generic taxonomy |
| 9 | Expand the categories through own research | ✅ | Discover & Go library passes, Museums For All, Blue Star, BofA Museums on Us, an FSA/HSA payment-method change, a transit-triggered museum discount, a reusable-container credit, ASTC Passport reciprocity — none of these appear in standard coupon-site taxonomies |
| 10 | Usable in the SF Bay Area with physical redemption locations | ✅ | every entry has a `bay_area` determination; audit found **0** entries without a venue, store list, official locator or explanatory note; the nine-county definition is FAMSF's published list |
| 11 | Provide links for manual review | ✅ | Sources view lists all 141 citations with the evidence passage read; `docs/SOURCES.md` is generated from the data; `scripts/verify_links.py` re-checks all 167 URLs |
| 12 | No manual input from the user | ✅ | research, transcription, coding, testing, publishing and merging were all performed by the agent; no clarification was requested at any point |
| 13 | GitHub Page with a clean, simple, organised, easy-to-read UI | ✅ | six views, filters, search, five sorts, status badges, collapsible evidence, dark mode, `prefers-reduced-motion`, print styles, skip link, `aria-live` result count |
| 14 | Official verified source links on the page | ✅ | every card ends with its citations; a render test asserts every visible card links to at least one official source |
| 15 | Create a pull request and merge it to main | ✅ | PR #1 merged as `0da9132`; the Pass-3 corrections ship in PR #2 |
| 16 | Suggestions for remaining work and limitations | ✅ | `docs/LIMITATIONS.md` (12 sections), `docs/ROADMAP.md` (10 priorities, backlog, maintenance cadence, definition of done) and the site's Limits & next work view |
| 17 | Multi-pass execution; do not stop after Pass 1 | ✅ | this log |

**Pass 3 defects found and fixed**

- **Documentation drift.** README, METHODOLOGY, LIMITATIONS, ROADMAP and this log all still said
  the pre-Pass-2 totals (223 overall, 135 at warning severity) after Pass 2 added flags.
  Corrected to **224 total flags (13 critical / 136 warning / 75 info)** in all five
  documents, and a new `TestDocsMatchData` class now fails the build if any document's flag
  totals, README headline counts, README category table, METHODOLOGY level table disagree with
  the data — or if a document references a repository path that does not exist, or omits one of
  the nine rejections. `docs/ROADMAP.md` is exempt from the path check by design, because it
  names files that do not exist yet.
- **Published-site verification.** The live Pages URL was fetched after the merge and confirmed
  to serve `index.html`, `assets/css/styles.css`, `assets/js/app.js`, `assets/data/coupons.js`
  and `data/coupons.json` (all HTTP 200), with statuses computed correctly against the current
  date (e.g. "Expires soon · Expires in 6 days (Sep 26, 2026)").

**Gaps carried forward deliberately** (unchanged by Pass 3, all in `docs/ROADMAP.md`): the
California Academy of Sciences free-day question, Lucky and the ethnic grocers, the six merchants
whose pages are unreadable without a headless browser, social-only offers, and re-harvesting the
P&G block whose coupons expired on 26–27 September 2026.

### Pass 3 — product-only re-scope + expansion (complete, 2026-09-22)

**Owner instruction:** "When I say coupons I mean products to purchase, not events and museums,
etc." Actions taken, line by line:

1. **Re-scope.** The two museum/admission shards (26 SF Museums For All venues; 23 Bay Area
   access programs) were moved out of the build into `archive/rescoped-2026-09-22/` with a
   README; the `community-access` category, the two admission deal types and the admission value
   kinds were retired from `data/meta.json`; the museum half of
   `scripts/generate_bulk_entries.py` was removed and the P&G half re-verified as byte-identical.
   The `no-spend-free` category was redefined as "No-spend & standing perks" (product freebies
   and free-to-obtain perks), and a `receipt-scan-rewards` category was added.
2. **P&G block spot re-verification.** `pgbrandsaver.com/coupons/` was re-fetched live on the
   verification afternoon: still "Updated September 2026", still "Search 112 Digital Coupons";
   26 offer lines across the first two rendered chunks (featured: Crest $5/$4/$2, Tampax/Always
   $1, Olay $5/$4/$2 TWO, five Bounce; list: Cascade $5 TWO/$4, Clearblue $2, the duplicate Crest
   prints at $5/$4/$2, Crest Mouthwash $1, Dawn Powerwash $2, five Downy cards, Bounce 330 $3)
   match the transcription verbatim, including the 9/26 and 9/27 expiry sets and the
   duplicated-Crest expiry contradiction (9/26 featured vs 9/27 in the search list — exactly the
   contradiction the `source-page-inconsistency` flags record). Programmatic check: shard expiry
   field equals the page line on all 26 compared offers. No drift found; the pre-existing flags
   remain accurate. The remaining 10 shard lines come from the same same-day full transcription
   (page self-reports a monthly refresh); a full 36/36 re-diff is scheduled in ROADMAP item 1.
3. **New verified offers (22):** 8 Kellanova printables read directly from
   `kellanovaus.com/us/en/coupons.html` (values sum to the page's own "up to $7.00 in savings"
   headline — completeness cross-check recorded per entry); Pop-Tarts Crazy Good Rewards;
   Checkout 51; Dunkin' $6 Meal Deal + Mobile Mondays (both fetched from the live homepage —
   the Mobile Mondays end date is a labelled inference, flagged); Chipotle Rewards "on Repeat"
   (2026-04-13 official press release); Jimmy John's Rewards enrolment + birthday terms (official
   terms page); Baskin-Robbins free-scoop sign-up; Subway MyWay→MVP transition (level B — the
   only bonus-points claim found sat on a `swuat.test.subway.com` TEST subdomain and was NOT used);
   Raley's Something Extra Dollars (official page read via search retrieval); Save Mart Rewards
   (official FAQ copy on savemart.com); Smart & Final Smart Advantage digital coupons (official
   FAQ, CA/AZ/NV restriction quoted); CVS ExtraCare Plus 20%-off-CVS-Health-brands (overview page,
   cross-checked against the coupon-policy page); 7-Eleven 7REWARDS (official join page + FAQ);
   plus the 2 Dunkin' entries counted above. Every one stores its URL, title, publisher, method,
   date and verbatim passage; every search-snippet-only entry carries
   `retrieval-via-search-snippet`.
4. **New negative findings (6 rejections, table above)** — the General Mills and Raley's/Smart &
   Final fabricated-code rings, two domain-drift hazards (boxtops.com, realsavings.com), one
   verified-but-online-only Kellanova offer, and the still-live-but-dead-in-2022 Kraft Heinz
   campaign page.
5. **Policy notes added (1):** `policy-colgate-coupons-suspended` — Colgate's own two pages
   disagree about whether online coupons exist; the live page was fetched (statement quoted), the
   contradicting microsite failed fetch twice, so the record flags `source-page-inconsistency`
   critical rather than picking a side. Clorox's 404'd Coupons page (contradicting its own
   product FAQs) went into the link-rot log, now 18 entries.
6. **Retrieval failures recorded, not hidden.** During this pass the fetcher intermittently
   failed (including two attempts on `smiles.colgate.com`); affected entries disclose it via the
   snippet flag; the roadmap (Priority 2/3) carries re-verification. No offer was dated
   `verified` without a successful read of official content.
7. **Tests and docs moved with the data:** render-test clock assertions updated (Kellanova =
   Ongoing at pinned date; Dunkin' Mobile Mondays = Expired; flagged-only asserted as exact
   count now that every visible card carries a flag); README / METHODOLOGY / LIMITATIONS /
   ROADMAP rewritten to the new totals and enforced against drift by `TestDocsMatchData`.

**Counts after this pass:** 101 offers (79 retained product entries + 22 new) · 15 rejections ·
112 citations · 41 domains · 207 total flags (12 critical / 142 warning / 53 info). Verified 2026-09-22.

8. **Post-merge CI audit found two real defects in the citation gate, fixed the same day**
   (PRs #4 and #5). The link re-check step carried `continue-on-error: true`, so the
   workflow's `strict` dispatch input could never fail a run, and its exit code was also
   swallowed by the un-`pipefail`ed `| tee` pipeline. Underneath both, `tee
   reports/link-check.log` failed at pipeline start because `reports/` is gitignored and
   absent from a fresh checkout — `verify_links.py` was SIGPIPE'd before checking a single
   URL, on every CI run, while the job stayed green. After `set -o pipefail` +
   `mkdir -p reports`, the post-merge run on main completed a full pass over the cited URLs
   in 1m4s with exit 0 and uploaded a genuine report artifact (10.5 KB). Provenance: link
   figures quoted earlier in this log came from local runs of the script, not CI artifacts,
   because before 2026-09-22 CI produced none. The weekly scheduled job now files a
   `link-rot` issue on genuine new failures as designed.

### Pass 4 — manufacturer re-harvest, Colgate follow-up, schema hardening (complete, 2026-09-22)

Owner instruction for this pass: keep expanding the project, working line by line with no
hallucinations, and land the improvements via a PR. Retrieval ran through the same anonymous
`fetch_page`/`web_search` tooling; the fetch proxy degraded mid-pass (repeated signature errors on
chunk continuations), which bounded what could honestly be read — and the honest record is what
shipped.

1. **P&G brandSAVER re-harvest (partial, honestly bounded).** `pgbrandsaver.com/coupons/` was
   re-fetched live. The page still self-reports "Updated September2026" and "Search 112 Digital
   Coupons". Everything this pass could read — the seven Featured rows and the first eighteen full
   rows of the search list, 25 offer lines covering 22 distinct transcribed coupons — matched the
   committed transcription line by line, including both expiry sets (9/26 Featured vs 9/27 list)
   and the three duplicated Crest rows that carry the `source-page-inconsistency` critical flags.
   One observed wrinkle: the list-view rendering of the Bounce 180 ct row prints
   "180 ct(excludes travel size)" with the space absent, in the same flattening that glues
   "$3.00OFF ONE" together — a DOM/markdown artefact of the card layout, recorded here, not
   "corrected" into the data. Chunks 2–9 — the remainder of the 36-row transcription's tail and
   the ~76 unlisted coupons — could not be fetched before the proxy failures; **no rows were
   invented to fill the gap** and the shard is unchanged apart from the new `recheck_due` field.
   The full 112-row harvest stays open (ROADMAP priority 1).
2. **Kellanova page re-fetched in full; completeness automated.** `kellanovaus.com/us/en/coupons.html`
   returned whole in one retrieval. All 8 transcribed cards re-read line by line against the
   page — SAVE $1.00/$1.25/$1.00/75¢/50¢/50¢/$1.00/$1.00 with their brand and qualifying-items
   lines — and the page headline still reads "We have 8 coupons today, up to $7.00 in savings":
   count 8 ✓, sum $7.00 ✓, zero drift. The page also still carries the "Mars Completes Acquisition
   of Kellanova" banner (domain-continuity evidence) and the print-limit copy behind the existing
   requirements. Per ROADMAP priority 10 #1, that hand-checked headline relationship is now a test
   (`TestIssuersCompletenessHeadline`) that fails the build if the shard and the quoted headline
   ever disagree. The eight KV cards were also **re-tagged** `offer_text_is_verbatim: false` with a
   new `verbatim_source_text` holding the three raw page lines in order — matching what
   METHODOLOGY §4 already describes for them (heading + brand + "on any ONE/TWO" lines joined with
   em dashes); the site now shows the assembled-quote note on those cards.
3. **Colgate contradiction: main page confirmed, microsite still unreachable.** `colgate.com/en-us/special-offers`
   was fetched again and printed the identical full statement ("Coupons Temporarily Unavailable…
   Please check back soon for updated offers"), read in one chunk with nothing truncated.
   `smiles.colgate.com/page/content/special-offers` and the domain root both failed direct fetch
   (attempts 3 and 4 of the project's four), and a targeted pass-4 search for the microsite returned
   **no organic result from that domain at all** — the only pages surfacing "Colgate coupon codes"
   were aggregator code farms. The contradiction therefore stands (the main site says *temporarily*,
   promising a future return, so the flag is kept), and the circulating code ring is now documented
   as `excl-colgate-aggregator-promo-codes` with the India-only Smiles Club Amazon terms as the
   nearest official analogue (online-only, non-US → out of scope twice over).
4. **Kellanova promotion-hub sweep produced two verified additions and one rejection.** The Pop-Tarts
   Crazy Good Rewards program entry gained its **published earning ladder** verbatim from the
   issuer's own Program Terms page ("You will receive 1 point for every $1 spent on participating
   Pop-Tarts™ products. You can then redeem these Points for Rewards through the Reward Catalog"),
   cited via search retrieval of the official domain and disclosed with the `retrieval-via-search-snippet`
   flag; the reward catalogue and product list stay behind login, so the entry remains level B. The
   legacy Scratch-Off game terms pages still served on `kellanovaus.com` were rejected
   (`excl-kellanova-legacy-scratch-off-games`): Cheez-It/RKT rewards "expire on 12/31/24" and the
   Pop-Tarts game closed 2026-09-02 with an online-only prize — the Kraft-Heinz-style
   "live-looking-dead" failure mode, caught on the issuer's own domain.
5. **Schema hardening (ROADMAP priority 10 #2).** Every one of the 38 dated records now carries
   `verification.recheck_due` = printed expiry − 3 days (policy documented in
   `data/meta.json → dataset.recheck_policy`; generated mechanically for the P&G shard, so CI
   reproducibility is preserved). Undated records deliberately carry none. The site renders the
   date on the card as a project-side re-check note, and `verify.yml` prints a run-summary table
   of records due within 7 days and files a single `recheck-due` issue on the weekly schedule run.
6. **Documentation audit fixes (drift found by this pass, not by tests).** §5 still described the
   pre-re-scope critical set (13 flags/11 issues, including two museum venue flags that moved with
   their entries to the archive) — corrected to the 12 flags/10 issues the data actually holds,
   with an explicit numbering note; §5b's snippet-disclosure count was stale at 7 (data: 17); §6's
   heading still said "(9)" while the table listed 15 — now 17 with this pass's two new records.
   The three-figure total checks in `TestDocsMatchData` had no way to catch sub-100 mentions like
   these; the human line-by-line pass did.
7. **Counts after this pass:** 101 offers (unchanged — this pass added evidence depth, not offer
   rows) · **17 rejections** · **113 citations** · 41 domains · **208 flags** (12 critical,
   142 warning, 54 info) · 80 unique cited URLs · 50 tests. Verified 2026-09-22 (passes 1–4).

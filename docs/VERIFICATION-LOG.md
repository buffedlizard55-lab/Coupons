# Verification log

**Verification date: 2026-09-22** (all sources accessed on this date; `accessed` is recorded per
citation in the data).
**Result: 128 verified offers · 9 documented rejections · 141 citations · 30 domains · 223 flags.**

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

## 5. Critical irregularities — 13 flags across 11 distinct issues

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
7. **`sf-museums-for-all-the-contemporary-jewish-museum` — `venue-temporarily-closed`.** The
   City's listing is headed "The Contemporary Jewish Museum (Temporarily Closed)". The admission
   benefit is published; the venue is not open. Do not travel without confirming on thecj.org.
8. **`famsf-free-first-tuesdays` — `de-young-closed-tuesdays-2026`.** FAMSF publishes free general
   admission on the first Tuesday of every month, while the City's Museums For All listing gives
   de Young hours as Thursday–Sunday (closed Tue–Wed). The Legion of Honor *is* open Tuesdays per
   the same listing. Both official statements are quoted; a first-Tuesday visit to the de Young may
   be impossible.
9. **`policy-trader-joes-no-coupons` — `scam-vector`.** Because Trader Joe's issues no coupons, any
   site, Facebook post or Instagram story offering Trader Joe's coupons, circulars or gift cards is
   not official, and the retailer disowns such organisations.
10. **`policy-sunday-insert-landscape-2026` — `stale-source-directories`.** "Best coupon site"
    directories still list SmartSource.com, FreeCoupons.com, CoolSavings, PPGazette and Mambo
    Sprouts; several are out of business or redirected. Any list built from those directories
    without checking each domain will contain dead or fraudulent sources.
11. **`policy-social-media-sourcing` — `scam-density`.** Social platforms are the dominant
    distribution channel for fabricated coupons and gift-card giveaways, which is why the project
    rule is "leads yes, citations no".

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
- **Retrieval transparency** — 7 entries were sourced from search-engine snippets of official
  domains rather than direct fetches and each carries `retrieval-via-search-snippet`.

## 6. Rejections (9)

Full records, with URLs checked and evidence, live in `data/entries/10-excluded-unverified.json`
and on the site's **Rejected & scam watch** view.

| Record | Merchant | Verdict | Reason in one line |
| --- | --- | --- | --- |
| `excl-round-table-pizza-aggregator-codes` | Round Table Pizza | REJECTED | Codes appear only on promo-code aggregators that contradict each other (and themselves), including one scoped to Reno & Sparks, NV |
| `excl-99-ranch-simplycodes` | 99 Ranch Market | REJECTED | Aggregator-only codes; the source page states "there are no active promo codes … right now" beside the codes it lists |
| `excl-coupons-com-affiliate-promo-codes` | 23 merchants (VistaPrint, Uber Eats, Samsung, FedEx, Macy's, Walmart, …) | REJECTED for this dataset | Affiliate-published promo codes, not merchant-published; the page itself states "We might earn commissions on purchases." Also outside the physical-Bay-Area-redemption scope |
| `excl-mcdonalds-third-party-reward-tiers` | McDonald's | REJECTED | Contradicted by the issuer's own rewards page, fetched the same day |
| `excl-dennys-free-birthday-grand-slam` | Denny's | REJECTED | Absent from `dennys.com/rewards`; the program is now BoothBucks. Belongs to the retired eClub era |
| `excl-california-academy-of-sciences-free-days` | California Academy of Sciences | UNVERIFIED | Official program page 404s; the press fact sheet is stale; third parties conflict. Highest-priority verification gap |
| `excl-costco-instant-savings-book-dates` | Costco | PLAUSIBLE BUT UNOFFICIAL | Cycle dates come from community scans, not Costco. One window independently matches P&G's official rebate window, but the dates are unauditable |
| `excl-trader-joes-online-coupons` | Trader Joe's | REJECTED | Disowned by the retailer; known phishing vector. Risk rated HIGH |
| `excl-exploratorium-free-wednesday-evenings` | Exploratorium | REJECTED | Neither the visit page nor the free/reduced admission page mentions any free evening program; the museum is closed Mondays and Thursday evenings are a paid "After Dark" session |

## 7. Pass log

### Pass 1 — implement and verify (complete)

Research, data construction, site, tests, CI and documentation, as described above. Deliverables:
11 shards (128 offers + 9 rejections), `data/meta.json` taxonomy and policy, generator for the
two bulk shards, build script, static site with six views, 167-URL link checker, 36 data-integrity
tests, 85 render assertions, two GitHub Actions workflows, five documents and this log.

### Pass 2 — bug, requirement and edge-case review (see below)

### Pass 3 — full re-check against the original request (see below)

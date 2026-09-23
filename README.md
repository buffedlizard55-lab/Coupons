# Bay Area Verified Coupons — product coupons only

A coupon, rebate and BOGO dataset for the **San Francisco Bay Area**, focused on **products you
buy in a store** — food, household, personal care, cleaning, OTC health, prepared food and
drinks. Event tickets and museum admission were explicitly removed from scope on 2026-09-22
(`archive/rescoped-2026-09-22/` explains why and keeps the evidence).

Every single offer was read line by line from **the website of the party that has to honour it** —
the manufacturer, the grocer, the pharmacy chain or the restaurant brand — and never from an
aggregator, a cashback portal, a promo-code site, a listicle or a social-media post.

**Live site:** https://buffedlizard55-lab.github.io/Coupons/

| | |
| --- | --- |
| Verified offers | **227** |
| Rejected / scam-watch claims documented | **20** |
| Citations | **265** across **72** domains |
| Verification levels | A: 190 · B: 34 · C: 3 |
| Irregularities flagged | **612** (20 critical, 497 warning, 96 info) |
| All sources checked on | **2026-09-22** |

---

## Why this exists

Most coupon sites are affiliate businesses. They republish codes from anywhere, keep expired
offers live because expired offers still earn clicks, and mix genuine manufacturer coupons with
promo codes that were never issued by anybody. The result is that a shopper cannot tell a real
$1.00-off Crest coupon from a fabricated "85% off Smart & Final" code page — among its 20
documented rejections this repository records **six fabricated-code rings** (Round Table Pizza,
99 Ranch Market, General Mills, Raley's/Smart & Final, Colgate, Sprouts), a family of stale
Kellanova prize-game terms still served on the official domain, coupon codes for **JOANN**, a
chain that liquidated every store in May 2025 and cannot honour anything, a Trader Joe's phishing
vector, and two manufacturer domains (boxtops.com, realsavings.com) that have drifted to a rock
band's tour site and a parked-ad shell.

This project takes the opposite position:

1. **Official sources only.** If the issuer does not publish it, it is not here.
2. **Products, not admissions.** Coupons for things you buy at a register — never events,
   venues or "free museum day" lists that always age out first.
3. **Nothing is invented.** No price, expiry, store list or eligibility rule is filled in from
   memory or from a "reasonable assumption". When the issuer publishes no expiry, the record
   says *ongoing — no end date published* instead of guessing one.
4. **Irregularities are surfaced, not smoothed over.** Contradictions between two official
   pages (Colgate's two coupon pages disagree), closed purchase windows, expired offers,
   benefits the issuer says are not live yet, and sources that were only partially retrievable
   are all flagged on the card itself.
5. **Rejections are published too.** Twenty claims that circulate widely online are documented
   with the reason they were rejected and the evidence that would change the verdict.
6. **Every line is checkable by hand.** Each citation stores the URL, the publisher, the page
   title, the retrieval method, the date it was read, and the verbatim passage that was read.

## What is in it

Categories are the ones the research actually produced, not a generic coupon-site taxonomy:

| Category | Offers | Notes |
| --- | --- | --- |
| Manufacturer digital coupons | 113 | P&G brandSAVER 112 coupons (full harvest: Crest, Tide, Olay, Always, Bounce, Cascade, Downy, Gain, Gillette, Old Spice, Oral-B, Swiffer… $0.75–$10.00, via Coupon24 at CVS) + Kellanova $1-off-two Barcode Buck$ |
| No-spend & standing perks | 23 | App sign-up freebies and free-to-obtain product perks (free McNuggets, free scoop, Mollie's weekly free item, IKEA Family free coffee/tea and $20 first-shop QR offer, Big 5 E-Team 10%, Grocery Outlet WOW $3-off-$25, Kohl's Senior-Wednesday/Military-Monday 15%) |
| Restaurant & quick-service loyalty | 22 | McDonald's, Starbucks, Dunkin', Chipotle, Jimmy John's, Baskin-Robbins, Subway, Taco Bell, Domino's, Pizza Hut, Peet's Peetnik Rewards — official rewards terms |
| Bay Area independent grocers & co-ops | 14 | Rainbow Grocery (10% seniors, volume, case, cheese), Mollie Stone's Rewards (1–3% rebate), 4 Items on the 4th (40% off), Sandwich/Salad/Soup clubs, weekly free item |
| Printable manufacturer coupons | 13 | Coupons.com printables + 8 Kellanova printables read directly from Kellanova's own coupon page |
| BOGO & multi-buy | 13 | "OFF TWO"/"any TWO" volume offers from P&G (Olay, Cascade), Kellanova and the new Kellanova $1-off-two |
| Grocery store coupon programs | 11 | Safeway / Andronico's for U, Raley's, Save Mart, Smart & Final, Albertsons, Whole Foods Prime (extra 10%, Tue/Fri Days of Deals), Sprouts digital coupons, Grocery Outlet WOW |
| Policy notes & scam watch | 10 | Trader Joe's, 2026 insert landscape, link-rot log, social-media sourcing, Colgate suspension, P&G retailer acceptance, Dollar Tree coupon-acceptance rules, Grocery Outlet coupon policy, Hobby Lobby coupon sunset |
| Big-box & mass retail loyalty | 10 | Target Circle, 7-Eleven, IKEA Family (member prices, dated 10/12 offers, student 15%), Kohl's Rewards 5% + Kohl's Cash earn event |
| Home improvement, hardware & auto | 9 | Harbor Freight coupon hub (3 dated in-store coupons + paid Inside Track Club), Ace Rewards, Lowe's MyLowe's, AutoZone $20/5-credits, O'Reilly O'Rewards |
| Rebates & cash back | 8 | P&G Back to School rebates ($25/$15/$5 — 3 tiers), P&G × Costco mail-in rebate, Ibotta, Checkout 51, Mollie Stone's $20 signup bonus |
| Drugstore & pharmacy | 7 | Walgreens, CVS ExtraCare & ExtraCare Plus 20%-off, GoodRx prescription pricing |
| Sporting goods & outdoor | 3 | REI Co-op ($30 lifetime, annual ~10% back, $30 new-member bonus card through 11/12/26), Big 5 E-Team |
| Pet supplies | 3 | Petco Perks Core (167 pts = $5) and paid Premier 15%-off tiers, PetSmart Treats (10 pts/$1, $2 per 1,000 pts) |
| Office, craft & hobby | 3 | Staples Easy Rewards (renamed program, 200 pts = $1), Michaels 3%/6% back, Hobby Lobby standing 40%-off-marked-price departments |
| Receipt-scan rewards | 2 | Pop-Tarts Crazy Good Rewards (Kellanova), Fetch |
| Warehouse club instant savings | 1 | Costco (program mechanics only) |

Deal types recorded: `$ off`, `% off`, `BOGO / multi-buy`, `free item`, `cash back`,
`rebate / gift card`, `points reward`, `member price`, `discounted price`, `rewards credit`,
`volume / case discount`, `promo code`, `policy note` — exactly the thirteen the dataset uses;
the two admission deal types from the pre-re-scope taxonomy were retired with it.

Physical redemption is a hard requirement. Rainbow Grocery's address, hours and phone are
transcribed verbatim; where offers are chain-wide and the issuer's locator is JavaScript-driven,
the card links to the official locator rather than inventing an address list. Online-only
redemption was itself grounds for rejection this pass (see `excl-rkt-squishmallows-online-only-reward`).

## Using the site

- **Browse offers** — filter by category, deal type, verification level and status; search
  across brands, offer text, addresses and source domains. Expired and not-yet-redeemable
  offers are hidden by default and can be switched back on.
- **Irregularities** — all 613 flags grouped by severity, each linking back to the offer.
- **Rejected & scam watch** — the twenty claims that were refused, with the reasoning.
- **Sources** — every citation, with the evidence passage that was read from it.
- **How this was verified** — verification levels, retrieval methods, flag severities, the
  nine-county Bay Area definition, and how to reproduce the build.
- **Limits & next work** — what this dataset does *not* cover and what to do next.

Statuses are computed in the browser against the visitor's current date, so an offer that was
"Active" on the verification date retires itself automatically: `Active` → `Expires soon`
(≤ 7 days) → `Expired`, plus `Window closed` for rebates whose purchase period has passed and
`Not redeemable yet` for benefits the issuer has announced but not launched.

Every dated record also carries a project-side `recheck_due` date — the printed expiry minus a 3-day
safety margin, documented in `data/meta.json` — which the weekly CI job uses to file
"due for re-verification" issues *before* an offer goes stale. It is scheduling metadata, never
an issuer deadline.

## Repository layout

```
index.html                     the site
assets/css/styles.css          styling (no frameworks, no CDN, no build step)
assets/js/app.js               front-end: filtering, sorting, status, routing
assets/data/coupons.js         generated dataset consumed by the front-end
data/meta.json                 taxonomy, verification policy, value schema, flag severities
data/entries/01..17-*.json     the curated shards — every offer string lives here
data/coupons.json              generated merged dataset (for reuse by other tools)
archive/rescoped-2026-09-22/   the museum/admission shards removed when scope became products-only
scripts/generate_bulk_entries.py  regenerates the P&G shard from its transcription
scripts/generate_pass6_entries.py regenerates the pass-6 expansion shard from its transcription
scripts/build_site.py          validates shards, emits the dataset, the site payload and _site/
scripts/verify_links.py        re-fetches every citation and reports what still resolves (CI-only)
tests/test_data.py             integrity tests (schema, sourcing rules, Bay Area, values, docs)
tests/test_site_render.js      render assertions against the real dataset in a DOM shim
tests/dom_shim.js              minimal DOM so the front-end can be tested without a browser
docs/METHODOLOGY.md            how each line was verified
docs/SOURCES.md                generated: every citation, grouped, with evidence
docs/LIMITATIONS.md            what is not covered and why
docs/ROADMAP.md                next work, in priority order
docs/VERIFICATION-LOG.md       what was checked, when, and what failed
.github/workflows/             Pages build + weekly citation re-check
```

## Reproducing and extending it

```bash
python3 scripts/build_site.py            # validate shards, regenerate data + site payload + docs/SOURCES.md
python3 -m unittest discover -s tests    # 56 tests: data integrity + site render
python3 scripts/verify_links.py          # re-check citations over HTTP (needs egress; runs weekly in CI)
python3 -m http.server 8000              # view the site locally at http://localhost:8000
```

The rules for adding an entry are enforced by the tests, not by convention:

- an entry without a `sources[]` citation fails the build;
- a citation without a verbatim `evidence` passage, a publisher, an access date and a retrieval
  method fails the build;
- an aggregator, promo-code, listicle or social domain cited as the source of an *available*
  offer fails the build;
- a level-A claim with no official-domain source fails the build;
- an offer marked unavailable in the Bay Area without an explanatory flag fails the build;
- a value that does not follow the canonical `{amount, unit, currency, kind}` schema fails the
  build;
- a `free_item` carrying a non-zero dollar figure must show the issuer's own cap verbatim in the
  offer text;
- editing a shard without rebuilding the generated files fails the build;
- a dated offer whose `verification.recheck_due` is missing or off-policy, or an undated one that carries one, fails the build;
- a Kellanova-style issuer completeness headline that no longer equals the shard's count and sum fails the build;
- README/docs totals that drift from the data (flag counts, level counts, category table,
  "every rejection is in the log") fail the build.

## Publishing

GitHub Pages for this repository is configured as **Deploy from a branch → `main` → `/ (root)`**,
so the site publishes from the committed root files (`index.html`, `assets/`, `data/`,
`.nojekyll`) as soon as a change lands on `main`. `.nojekyll` is committed deliberately so GitHub
serves the files as-is instead of running them through Jekyll.

`.github/workflows/pages.yml` validates the dataset, runs all 56 tests, proves the P&G shard is
reproducible and builds the site on every push and pull request. It also detects the repository's
Pages mode: if Pages is ever switched to **GitHub Actions**, the same workflow uploads `_site/` as
the Pages artifact and deploys it, with no further changes needed. `.github/workflows/verify.yml`
re-checks every citation weekly and posts the result as a workflow log/issue-ready report.

## Honesty about coverage

This is not every coupon that exists. It is every product offer that could be **verified against
an official source during the research passes of 2026-09-22**, plus an explicit record of what was
rejected and why. Two known freshness facts: the 112 P&G brandSAVER coupons carried printed expiries of 26–28 September 2026 (the site marks them expired from those dates automatically, and pass 5 re-read all 10 chunks of https://pgbrandsaver.com/coupons/ live — 112 rows, exactly the page's advertised "Search 112 Digital Coupons" headline, with zero drift on the 36 previously transcribed and seven newly documented expiry contradictions), and the Kellanova printables show no expiry on the page, so the printed coupon is the authority. A pass-5 regression was also recorded: kellanovaus.com/us/en/coupons.html now intermittently serves its coupon grid unpopulated to plain fetch (tokens for count and savings left unresolved, print control reading "PRINT COUPONS0"), so its 8 coupons could not be re-confirmed in that fetch cycle — flagged rather than treated as retracted.
Personalised offers (Safeway for U, Target Circle, Costco Instant Savings, restaurant apps) are
verified at program level only, because their offers are per-account and cannot be read
anonymously. Facebook and Instagram could not be searched at all: both require authentication, so
no social post was read or cited; social platforms were used only to generate leads that were then
verified on an official domain or rejected.

`docs/LIMITATIONS.md` states all of this in full; `docs/ROADMAP.md` lists the next steps,
starting with the monthly manufacturer re-harvest (now that the P&G 112-row harvest is complete, the headline is pinned by a test) and watching for Colgate's promised "updated offers" (its main page was re-fetched three times on 2026-09-22 and still says coupons are unavailable), plus a new Clorox rejection: the Gift of Clean is sold out and is a service, not a product, while clorox.com/coupons/ still 404s.

## Licence and disclaimer

Site code and scripts: MIT (`LICENSE`). Curated data and documentation: CC BY 4.0
(`LICENSE-DATA`) — attribution must carry the verification date forward.

Independent research project. Not affiliated with, endorsed by or sponsored by any retailer,
manufacturer, restaurant, pharmacy or brand owner named here. All trademarks belong to their
owners. Offer text is quoted for identification, review and consumer-protection purposes. Offers
change without notice; always confirm with the issuer before travelling.

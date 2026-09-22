# Bay Area Verified Coupons

A coupon, rebate and free-admission dataset for the **San Francisco Bay Area**, in which every
single offer was read line by line from **the website of the party that has to honour it** —
the manufacturer, the grocer, the museum, the restaurant chain or the city agency — and never
from an aggregator, a cashback portal, a promo-code site, a listicle or a social-media post.

**Live site:** https://buffedlizard55-lab.github.io/Coupons/

| | |
| --- | --- |
| Verified offers | **128** |
| Rejected / scam-watch claims documented | **9** |
| Citations | **141** across **30** domains |
| Verification levels | A: 115 · B: 11 · C: 2 |
| Irregularities flagged | **223** (13 critical, 135 warning, 75 info) |
| All sources checked on | **2026-09-22** |

---

## Why this exists

Most coupon sites are affiliate businesses. They republish codes from anywhere, keep expired
offers live because expired offers still earn clicks, and mix genuine manufacturer coupons with
promo codes that were never issued by anybody. The result is that a shopper cannot tell a real
$1.00-off Crest coupon from a fabricated "Costco $100 gift card" post.

This project takes the opposite position:

1. **Official sources only.** If the issuer does not publish it, it is not here.
2. **Nothing is invented.** No price, expiry, store list or eligibility rule is filled in from
   memory or from a "reasonable assumption". When the issuer publishes no expiry, the record
   says *ongoing — no end date published* instead of guessing one.
3. **Irregularities are surfaced, not smoothed over.** Contradictions between two official
   pages, closed purchase windows, expired offers, benefits the issuer says are not live yet,
   and sources that were only partially retrievable are all flagged on the card itself.
4. **Rejections are published too.** Nine claims that circulate widely online are documented
   with the reason they were rejected and the evidence that would change the verdict.
5. **Every line is checkable by hand.** Each citation stores the URL, the publisher, the page
   title, the retrieval method, the date it was read, and the verbatim passage that was read.

## What is in it

Categories are the ones the research actually produced, not a generic coupon-site taxonomy:

| Category | Offers | Notes |
| --- | --- | --- |
| No-spend & free admission | 51 | Free with no purchase: museum admission, age-based free entry, always-free public spaces |
| Community access programs | 45 | Museums For All, Free Saturdays, Discover & Go library passes, Blue Star |
| Manufacturer digital coupons | 36 | P&G brandSAVER, clipped to a store loyalty card |
| Bay Area independent grocers & co-ops | 11 | Rainbow Grocery, Mollie Stone's |
| Restaurant & quick-service loyalty | 10 | McDonald's, Starbucks, Denny's — official rewards terms |
| BOGO & multi-buy | 6 | Volume and multi-item offers |
| Drugstore & pharmacy | 6 | Walgreens, CVS ExtraCare, GoodRx prescription pricing |
| Printable manufacturer coupons | 5 | Coupons.com printables |
| Policy notes & scam watch | 5 | Trader Joe's coupon policy, 2026 insert landscape, link-rot log, social-media sourcing |
| Grocery store coupon programs | 4 | Safeway / Andronico's for U, Raley's, Albertsons banners |
| Rebates & cash back | 3 | P&G × Costco mail-in rebate, Ibotta |
| Warehouse club instant savings | 1 | Costco (program mechanics only) |
| Big-box & mass retail loyalty | 1 | Target Circle |

Deal types recorded: `$ off`, `free admission`, `% off`, `member price`, `rewards credit`,
`reduced admission`, `points`, `BOGO`, `free item`, `volume discount`, `rebate`, `cash back`,
`promo code`, `policy`.

Physical redemption is a hard requirement. Where the issuer publishes an address, opening hours
or a phone number, that is transcribed onto the card (Exploratorium at Pier 15, de Young at
50 Hagiwara Tea Garden Drive, Legion of Honor at 100 34th Avenue, SFMOMA at 151 Third Street,
Rainbow Grocery in San Francisco, and so on). Where offers are chain-wide and the issuer's
locator is JavaScript-driven, the card links to the official locator rather than inventing an
address list.

## Using the site

- **Browse offers** — filter by category, deal type, verification level and status; search
  across brands, offer text, addresses and source domains. Expired and not-yet-redeemable
  offers are hidden by default and can be switched back on.
- **Irregularities** — all 223 flags grouped by severity, each linking back to the offer.
- **Rejected & scam watch** — the nine claims that were refused, with the reasoning.
- **Sources** — every citation, with the evidence passage that was read from it.
- **How this was verified** — verification levels, retrieval methods, flag severities, the
  nine-county Bay Area definition, and how to reproduce the build.
- **Limits & next work** — what this dataset does *not* cover and what to do next.

Statuses are computed in the browser against the visitor's current date, so an offer that was
"Active" on the verification date retires itself automatically: `Active` → `Expires soon`
(≤ 7 days) → `Expired`, plus `Window closed` for rebates whose purchase period has passed and
`Not redeemable yet` for benefits the issuer has announced but not launched.

## Repository layout

```
index.html                     the site
assets/css/styles.css          styling (no frameworks, no CDN, no build step)
assets/js/app.js               front-end: filtering, sorting, status, routing
assets/data/coupons.js         generated dataset consumed by the front-end
data/meta.json                 taxonomy, verification policy, value schema, flag severities
data/entries/01..11-*.json     the curated shards — every offer string lives here
data/coupons.json              generated merged dataset (for reuse by other tools)
scripts/generate_bulk_entries.py  regenerates the two largest shards from transcriptions
scripts/build_site.py          validates shards, emits the dataset, the site payload and _site/
scripts/verify_links.py        re-fetches every citation and reports what still resolves
tests/test_data.py             36 integrity tests (schema, sourcing rules, Bay Area, values)
tests/test_site_render.js      85 render assertions against the real dataset in a DOM shim
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
python3 scripts/build_site.py            # validate shards, regenerate data + site payload
python3 -m unittest discover -s tests    # 39 tests: data integrity + site render
python3 scripts/verify_links.py          # re-fetch all 167 cited URLs, write reports/
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
- editing a shard without rebuilding the generated files fails the build.

## Publishing

GitHub Pages for this repository is configured as **Deploy from a branch → `main` → `/ (root)`**,
so the site publishes from the committed root files (`index.html`, `assets/`, `data/`,
`.nojekyll`) as soon as a change lands on `main`. `.nojekyll` is committed deliberately so GitHub
serves the files as-is instead of running them through Jekyll.

`.github/workflows/pages.yml` validates the dataset, runs all 39 tests, proves the bulk shards are
reproducible and builds the site on every push and pull request. It also detects the repository's
Pages mode: if Pages is ever switched to **GitHub Actions**, the same workflow uploads `_site/` as
the Pages artifact and deploys it, with no further changes needed.

## Honesty about coverage

This is not every coupon that exists. It is every offer that could be **verified against an
official source during the research pass of 2026-09-22**, plus an explicit record of what was
rejected and why. The largest single block — 36 P&G brandSAVER coupons — carried printed
expiries of 26–27 September 2026, four to five days after verification; the site marks them
expired from that date, and the block needs re-harvesting to stay useful. Personalised offers
(Safeway for U, Target Circle, Costco Instant Savings, restaurant apps) are verified at program
level only, because their offers are per-account and cannot be read anonymously. Facebook and
Instagram could not be searched at all: both require authentication, so no social post was read
or cited, and social platforms were used only to generate leads that were then verified on an
official domain or rejected.

`docs/LIMITATIONS.md` states all of this in full; `docs/ROADMAP.md` lists the ten highest-value
next steps, starting with the California Academy of Sciences free-admission gap.

## Licence and disclaimer

Site code and scripts: MIT (`LICENSE`). Curated data and documentation: CC BY 4.0
(`LICENSE-DATA`) — attribution must carry the verification date forward.

Independent research project. Not affiliated with, endorsed by or sponsored by any retailer,
manufacturer, restaurant, museum, library or government agency named here. All trademarks belong
to their owners. Offer text is quoted for identification, review and consumer-protection
purposes. Offers change without notice; always confirm with the issuer before travelling.

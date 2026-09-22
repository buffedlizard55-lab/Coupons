# Limitations

An honest account of what this dataset does not do, why, and what that means for someone
standing in a Bay Area store with a phone in their hand. Verification date: **2026-09-22**
(two passes that day; the second rescoped the project to **product coupons only** — no events,
museums or venue admission).

Nothing here is a defect that can be patched by rewording. Each item is a boundary created by
the project's own rule — *if the issuer does not publish it, it is not here* — and each is
stated so a reader can decide how much weight to give a particular entry.

---

## 1. The dataset ages in days, not months

The largest single block is 36 P&G brandSAVER coupons whose printed expiries were
**26–27 September 2026** — four to five days after verification. Every one of them
carries the flag `expires-imminently`. The Kellanova printables (8 coupons, worth a combined
$7.00 as the issuer's own page headline confirms) publish **no expiry at all**, so the printed
page is the only authority and re-verification is the only defence. The site computes status
from the visitor's clock, so dated offers retire themselves without a redeploy, but the
underlying data is only useful for a few days at a time.

Consequence: **manufacturer coupon data must be re-harvested roughly monthly**, and ideally
weekly during heavy promotion periods. `docs/ROADMAP.md` item 1 covers the re-harvest.

## 2. Personalised offers cannot be verified anonymously

These programs are real, official and confirmed (level B), but their *individual offers* are
generated per account, per store or per app session, so no anonymous reader can enumerate them:

| Program | Why the offers are not listed |
| --- | --- |
| Safeway / Andronico's **for U** | Coupons are clipped per account; `/foru/coupons.html` no longer resolves, and the guest page describes the program rather than listing offers |
| **Target Circle** | Deals are personalised; Deal Days dates come from the corporate newsroom, not a live offer list |
| **Costco Instant Savings** | Item-level offers rotate on a roughly four-week cycle; every Costco offer URL tried returned "Page Not Found!" to an anonymous fetch, and only member channels (app → Warehouse tab, in-warehouse book) expose them |
| **Raley's Something Extra** | raleys.com returns a JavaScript shell to plain fetchers; program terms (points ladder, quarterly dollars) were read from the official page via search retrieval, but which member deals are live this week is account-specific — the Feb-2025 circular example in the dataset stays flagged `source-outdated` |
| **Save Mart / Smart & Final digital coupons** | Coupon galleries are account-gated; the official FAQs establish the mechanics, not the current clip list |
| **McDonald's, Starbucks, Denny's, Dunkin', Chipotle, Jimmy John's, Baskin-Robbins, Subway** | Rewards are official and their sign-up/birthday terms are quoted verbatim, but in-app rotating offers (BoothBucks multipliers, bonus-Star days, Freepotle drops) are personalised and short-window |
| **Walgreens / CVS** | ExtraCare and myWalgreens offers are account-linked; CVS's public pages were additionally behind an anti-bot interstitial (its ExtraCare Plus 20%-off benefit is on the overview page and is recorded) |
| **Ibotta / Checkout 51** | Both are receipt-scan platforms whose value is real but per-user; only the published platform mechanics are verified |

Consequence: for these merchants the dataset tells you **the program is legitimate and how it
works**, not what it is offering you today. Any site that lists specific Costco or Safeway
offers without a membership session is guessing or scraping stale data.

## 3. Some official pages are not machine-readable

Observed on 2026-09-22 and logged in the entry `policy-link-rot-observed-2026-09-22` (which the
site renders in full):

- **404 / removed:** `safeway.com/foru/coupons.html`, `coupons.com/printable-grocery-coupons`,
  `coupons.com/printables`, `costco.com/coupons.html`, `costco.com/online-offers.html`,
  `molliestones.com/stores/`, `luckysupermarkets.com/foru-guest.html`, `papajohns.com/order/coupons`,
  `kfc.com/deals`, `dominos.com/en/pages/order/coupons/`, `clorox.com/coupons/` (while Clorox
  product FAQs still tell shoppers to "check the Coupons page")
- **JavaScript shell only (no offer text in the HTML):** `raleys.com`, `pizzahut.com/deals`
- **Anti-bot interstitial:** `cvs.com/extracare`
- **Live fetch failures during pass 3 (recorded, re-check next pass):** `smiles.colgate.com/page/content/special-offers`
- **Domain drift — former official URLs now serve other people:** `boxtops.com` (a rock band's
  tour site), `realsavings.com` (a parked-ad shell)

Consequence: several large Bay Area merchants — Lucky, Pizza Hut, Domino's, Papa Johns, KFC —
have **no verified entry at all**, not even a level-B program note, because nothing could be
read. That is a coverage hole caused by retrieval, not by choice. A headless-browser
verification path (`docs/ROADMAP.md` item 3) is the fix.

## 4. Facebook and Instagram could not be searched

The original brief asked for social-media research. Both platforms require authentication, so no
post could be retrieved, read or cited; the same applies to TikTok. Social platforms were used
**only** as lead generators, and both Reddit leads produced were then verified on an official
domain or rejected:

- Reddit → `getpgoffer.com` P&G × Costco rebate → verified as an official P&G microsite → **included**
- Reddit → Costco Instant Savings cycle dates → not confirmable on any Costco page → **excluded**
  as `PLAUSIBLE BUT UNOFFICIAL`

Consequence: genuinely social-only offers — a Bay Area restaurant's Instagram-only happy hour, a
neighbourhood bakery's Facebook flash sale — are invisible to this dataset unless the same offer
also appears on the issuer's own website. Closing that gap needs an authenticated session or a
documented human-review workflow (`docs/ROADMAP.md` item 6), not a crawler.

## 5. What "product coupons only" excludes on purpose

From 2026-09-22 the dataset tracks **products you can buy in a store** and nothing else:

- Museum/attraction admission programs — removed by owner instruction; the fully verified
  museum work is preserved in `archive/rescoped-2026-09-22/` rather than deleted, and the
  taxonomy (admission deal types, community-access category) was retired with it.
- Online-only redemptions — e.g. Kellanova's verified "upload your receipt for $5 off a $20
  purchase at Squishmallows.com" is **rejected for scope** (`excl-rkt-squishmallows-online-only-reward`),
  because it cannot be redeemed in person.
- Sweepstakes and points-for-prizes contests that do not discount a product (Cheez-It's
  "vote for a chance to win Free Cheez-It for a year") — noted during the Kellanova sweep, not
  listed, since a sweepstakes entry is not a coupon.
- Event tickets, classes, dining-out "experiences" and gift cards to venues.

## 6. Store-level acceptance is not verified

A manufacturer coupon can be genuinely published and still fail at a specific register: the
product may not be stocked, the store may not participate in the clipping channel, the coupon
may require a loyalty card the shopper does not have, or a cashier may decline it. This dataset
verifies **the offer**, not each store's behaviour on a given day. Smart & Final's own
geographic restriction ("only redeemable at Smart & Final locations in California, Arizona and
Nevada") is quoted because the issuer publishes it; no further store promises are made.

Related: Rainbow Grocery's published rule that its "Honored Every Day" discounts *override* case
discounts is recorded (`interaction-overrides`), because stacking assumptions are the most common
way a verified offer disappoints in practice.

## 7. Geographic coverage is uneven

| Depth | Area |
| --- | --- |
| Deep | San Francisco — Rainbow Grocery, Mollie Stone's, Andronico's (verified venues), plus every chain program whose locator resolves there |
| Medium | Chain-level programs valid across all nine counties (P&G, Kellanova, Coupons.com, Safeway, Raley's-family, Save Mart, Smart & Final, Walgreens, CVS, Target, 7-Eleven, Costco, McDonald's, Starbucks, Dunkin', Chipotle, Jimmy John's, Baskin-Robbins, Subway, GoodRx) |
| Shallow | Oakland, Berkeley, San Jose, the Peninsula, the North Bay, the Tri-Valley — no independently verified local independents yet |

`data/meta.json → bay_area_county_notes` records the depth per county. Nothing was padded to
make the map look even.

## 8. Official sources contradict each other

Cases found and flagged rather than resolved:

1. **CVS ExtraCare Pharmacy & Health Rewards** — the formal Program Rules page says 10 credits
   earn a $5 reward; the CVS retail help page says 4 credits earn $2. Both are quoted; neither
   is chosen.
2. **Colgate** — `colgate.com/en-us/special-offers` states "Coupons Temporarily Unavailable"
   while the Colgate-operated `smiles.colgate.com` microsite advertises printable coupons; the
   microsite could not be fetched live on the verification date, so the contradiction is recorded
   and flagged `critical` rather than resolved.
3. **Clorox** — product-page FAQs instruct shoppers to "check the Coupons page", but
   `clorox.com/coupons/` returns a 404 ("Well, this is embarrassing"). Recorded in the link-rot
   note; no Clorox coupon entries are published.
4. **P&G** — three Crest coupons appear twice on the same brandSAVER page with **two different
   printed expiries**; both are kept, flagged `source-page-inconsistency` (critical).

## 9. Prices and figures are not guarantees

- **GoodRx** prescription prices are "as low as" figures that vary by pharmacy, dosage and date;
  the recorded examples are the prices published on the verification date, with their URLs, and
  the entry carries `price-varies-by-pharmacy` and `not-insurance`.
- **Costco** instant savings vary by warehouse and cycle; no item-level price is asserted.
- **Starbucks Stars** have no cash value and the issuer's terms reserve the right to change or
  discontinue benefits (`stars-no-cash-value`, `issuer-may-suspend`, `arbitration-clause`).
- **Checkout 51 / Ibotta** cash-back amounts are per-user and per-week; only platform mechanics
  are quoted.

## 10. Partial captures are disclosed, not filled in

Several entries quote pages that could not be read in full; each says so on its face:

- **Starbucks Birthday Reward** — the Gold (7-day) and Reserve (30-day) redemption windows were
  captured verbatim, but the Green-level baseline sentence and the exact list of what the reward
  covers fell outside the retrieved portion. Flagged `partial-capture`; the missing wording was
  **not** reconstructed from third-party summaries.
- **Walgreens** — the WELL20 code has no published expiry (`expiry-not-published`) and the beauty
  reward's asterisked terms were not machine-readable (`terms-not-readable`).
- **Chipotle, Jimmy John's, Baskin-Robbins, Subway, Raley's, Save Mart, Smart & Final, CVS,
  7-Eleven** (pass 3 additions) — the live fetcher failed intermittently during the session, so
  these cite official pages via **search retrieval of the official domain** and each carries the
  `retrieval-via-search-snippet` disclosure flag. A reviewer opening the cited URL sees the same
  text; nobody should mistake these for fully re-rendered captures.

## 11. Structural limits of the dataset

- **No inventory or stock data.** Whether a couponed item is on the shelf is unknowable from a
  coupon page.
- **No price comparison.** The dataset records what an issuer offers, not whether it beats the
  competitor across the street.
- **No stacking advice beyond what issuers publish.** Combination rules are quoted where the
  issuer states them; where they do not, no assumption is recorded.
- **No accounts, no clipping, no submission.** Nothing here can clip a coupon to a loyalty card
  or file a rebate; each card links to the issuer's own page for that.
- **English only.** Issuer pages in other languages were not consulted.
- **Point-in-time evidence.** Each citation records the date it was read. A page that changes
  next week does not retroactively validate or invalidate the record; the weekly link check
  detects disappearance, not silent rewording.
- **Coupon media coverage (Krazy Coupon Lady and peers) is used only to map the landscape**
  (e.g. the 2026 Sunday-insert state), never as the source of an offer — aggregator economics
  reward staleness, as §8 demonstrates.

## 12. What the flags can't tell you

A flag marks something irregular about the **record**. It cannot mark:

- an offer the issuer withdrew quietly without changing its page;
- a regional variation the issuer never published;
- a store that stopped honouring a program;
- an offer that is real but not worth the trip.

The only defence against these is re-verification, which is why
`.github/workflows/verify.yml` re-checks all 72 unique cited URLs every Monday and files a
`link-rot` issue when one outside the documented log stops resolving.

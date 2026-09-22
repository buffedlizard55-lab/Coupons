# Limitations

An honest account of what this dataset does not do, why, and what that means for someone
standing in a store in the Bay Area with a phone in their hand. Verification date: **2026-09-22**.

Nothing here is a defect that can be patched by rewording. Each item is a boundary created by
the project's own rule — *if the issuer does not publish it, it is not here* — and each is
stated so that a reader can decide how much weight to give a particular entry.

---

## 1. The dataset ages in days, not months

The largest single block is 36 P&G brandSAVER coupons whose printed expiries were
**26–27 September 2026** — four to five days after the verification date. Every one of them
carries the flag `expires-imminently` (36 of the 136 warning flags). The site computes status
from the visitor's clock, so they display as `Expired` from those dates without a redeploy, but
the underlying data is only useful for a few days at a time.

Consequence: **manufacturer coupon data must be re-harvested roughly monthly**, and ideally
weekly during heavy promotion periods. Until that happens, the block is a demonstration of the
method rather than a live list. `docs/ROADMAP.md` item 2 covers the re-harvest.

## 2. Personalised offers cannot be verified anonymously

These programs are real, official and confirmed (level B), but their *individual offers* are
generated per account, per store or per app session, so no anonymous reader can enumerate them:

| Program | Why the offers are not listed |
| --- | --- |
| Safeway / Andronico's **for U** | Coupons are clipped per account; `/foru/coupons.html` no longer resolves, and the guest page describes the program rather than listing offers |
| **Target Circle** | Deals are personalised; Deal Days dates come from the corporate newsroom, not a live offer list |
| **Costco Instant Savings** | Item-level offers rotate on a roughly four-week cycle; every Costco offer URL tried returned "Page Not Found!" to an anonymous fetch, and only member channels (app → Warehouse tab, in-warehouse book) expose them |
| **Raley's / Bel Air / Nob Hill Something Extra** | `raleys.com` returns a JavaScript shell; the only locatable circular PDF is dated 26 Feb 2025, ~19 months old, and is flagged `source-outdated` |
| **McDonald's, Starbucks, Denny's** | Rewards are official and their terms are quoted verbatim, but bonus-Star days, BoothBucks multipliers and app offers are personalised and short-window |
| **Walgreens / CVS** | ExtraCare and myWalgreens offers are account-linked; CVS's public pages were additionally behind an anti-bot interstitial |

Consequence: for these merchants the dataset tells you **the program is legitimate and how it
works**, not what it is offering you today. Any site that lists specific Costco or Safeway
offers without a membership session is guessing or scraping stale data.

## 3. Some official pages are not machine-readable

Observed on 2026-09-22 and logged in the entry `policy-link-rot-observed-2026-09-22` (which the
site renders in full):

- **404 / removed:** `safeway.com/foru/coupons.html`, `coupons.com/printable-grocery-coupons`,
  `coupons.com/printables`, `costco.com/coupons.html`, `costco.com/online-offers.html`,
  `calacademy.org/neighborhood-free-sundays`, `molliestones.com/stores/`,
  `luckysupermarkets.com/foru-guest.html`, `papajohns.com/order/coupons`, `kfc.com/deals`,
  `dominos.com/en/pages/order/coupons/`
- **JavaScript shell only (no offer text in the HTML):** `raleys.com`, `pizzahut.com/deals`
- **Anti-bot interstitial:** `cvs.com/extracare`

Consequence: several large Bay Area merchants — Lucky, Pizza Hut, Domino's, Papa Johns, KFC —
have **no verified entry at all**, not even a level-B program note, because nothing could be
read. That is a coverage hole caused by retrieval, not by choice. A headless-browser
verification path (`docs/ROADMAP.md` item 3) is the fix.

## 4. Facebook and Instagram could not be searched

The original brief asked for social-media research. Both platforms require authentication, so no
post could be retrieved, read or cited; the same applies to TikTok. Social platforms were used
**only** as lead generators, and both leads produced were then verified on an official domain or
rejected:

- Reddit → `getpgoffer.com` P&G × Costco rebate → verified as an official P&G microsite → **included**
- Reddit → Costco Instant Savings cycle dates → not confirmable on any Costco page → **excluded**
  as `PLAUSIBLE BUT UNOFFICIAL`

Consequence: genuinely social-only offers — a Bay Area restaurant's Instagram-only happy hour, a
neighbourhood bakery's Facebook flash sale — are invisible to this dataset. Closing that gap
needs an authenticated session or a documented human-review workflow
(`docs/ROADMAP.md` item 8), not a crawler.

## 5. The California Academy of Sciences gap

A major Golden Gate Park attraction has **no verified free-admission entry**, which is the most
conspicuous hole in an otherwise deep San Francisco museum set:

- `calacademy.org/neighborhood-free-sundays` returns the Academy's own 404 page ("Someone pulled
  the plug on this page!")
- the press fact sheet that mentions free days is stale
- third-party sources disagree about whether the program still runs, and on which days

The claim is recorded in `10-excluded-unverified.json` as `UNVERIFIED` with the URLs checked and
the evidence that would resolve it. It is **not** listed as an available offer, because
publishing an unconfirmed free-day would be exactly the kind of claim this project exists to
avoid. This is the first item in `docs/ROADMAP.md`.

## 6. Store-level acceptance is not verified

A manufacturer coupon can be genuinely published and still fail at a specific register: the
product may not be stocked, the store may not participate in the clipping channel, the coupon
may require a loyalty card the shopper does not have, or a cashier may decline it. This dataset
verifies **the offer**, not each store's behaviour on a given day.

Related: Rainbow Grocery's published rule that its "Honored Every Day" discounts *override* case
discounts is recorded (`interaction-overrides`), because stacking assumptions are the most common
way a verified offer disappoints in practice.

## 7. Geographic coverage is uneven

| Depth | Area |
| --- | --- |
| Deep | San Francisco — Museums For All venues (26), FAMSF, SFMOMA, Exploratorium, Discover & Go, Rainbow Grocery, Mollie Stone's, Andronico's |
| Medium | Chain-level programs valid across all nine counties (P&G, Coupons.com, Safeway, Walgreens, CVS, Target, Costco, McDonald's, Starbucks, Denny's, GoodRx) |
| Shallow | Oakland, Berkeley, San Jose, the Peninsula, the North Bay, the Tri-Valley — no independently verified local institutions |

`data/meta.json → bay_area_county_notes` records the depth per county. Nothing was padded to
make the map look even.

## 8. Official sources contradict each other

Three cases were found and are flagged `critical` or `warning` rather than resolved:

1. **CVS ExtraCare Pharmacy & Health Rewards** — the formal Program Rules page says 10 credits
   earn a $5 reward; the CVS retail help page says 4 credits earn $2. Both are quoted; neither
   is chosen.
2. **FAMSF free first Tuesdays vs. de Young opening hours** — FAMSF publishes free general
   admission on the first Tuesday of every month, while the City of San Francisco's Museums For
   All listing gives de Young hours as Thursday–Sunday only. A first-Tuesday visit to the de
   Young may therefore be impossible; the Legion of Honor (open Tuesday–Sunday) is unaffected.
3. **CityPASS savings claims** — three official museum pages quote three different figures
   (46%, "up to 46%", "up to 45%"). All three are recorded, with `conflicting-savings-claims`,
   and the affiliate tracking parameters on the outbound links are disclosed
   (`affiliate-links`).

Also flagged rather than smoothed: FAMSF's Museums For All eligibility wording ("Medi-Cal **and**
food assistance") versus the City's listing ("EBT **or** Medi-Cal"); and the FAMSF $3 transit
discount, whose source passage was truncated mid-sentence during retrieval.

## 9. Prices and figures are not guarantees

- **GoodRx** prescription prices are "as low as" figures that vary by pharmacy, dosage and date;
  the recorded examples are the prices published on the verification date, with their URLs, and
  the entry carries `price-varies-by-pharmacy` and `not-insurance`.
- **Costco** instant savings vary by warehouse and cycle; no item-level price is asserted.
- **Museum surcharges** for special exhibitions are excluded from every free-admission offer
  (`special-exhibitions-excluded`), and per-venue Museums For All terms vary
  (`per-venue-terms-vary`).
- **Starbucks Stars** have no cash value and the issuer's terms reserve the right to change or
  discontinue benefits (`stars-no-cash-value`, `issuer-may-suspend`, `arbitration-clause`).

## 10. Partial captures are disclosed, not filled in

Two entries quote terms pages that could not be read in full:

- **Starbucks Birthday Reward** — the Gold (7-day) and Reserve (30-day) redemption windows were
  captured verbatim, but the Green-level baseline sentence and the exact list of what the reward
  covers fell outside the retrieved portion. Flagged `partial-capture`; the missing wording was
  **not** reconstructed from third-party summaries.
- **Walgreens** — the WELL20 code has no published expiry (`expiry-not-published`) and the beauty
  reward's asterisked terms were not machine-readable (`terms-not-readable`).

## 11. Structural limits of the dataset

- **No inventory or stock data.** Whether a couponed item is on the shelf is unknowable from a
  coupon page.
- **No price comparison.** The dataset records what an issuer offers, not whether it beats the
  competitor across the street.
- **No stacking advice beyond what issuers publish.** Combination rules are quoted where the
  issuer states them; where they do not, no assumption is recorded.
- **No accounts, no clipping, no submission.** Nothing here can clip a coupon to a loyalty card,
  file a rebate or reserve a museum pass; each card links to the issuer's own page for that.
- **English only.** Issuer pages in other languages were not consulted.
- **Point-in-time evidence.** Each citation records the date it was read. A page that changes
  next week does not retroactively validate or invalidate the record; the weekly link check
  detects disappearance, not silent rewording.

## 12. What the flags can't tell you

A flag marks something irregular about the **record**. It cannot mark:

- an offer the issuer withdrew quietly without changing its page;
- a regional variation the issuer never published;
- a store that stopped honouring a program;
- an offer that is real but not worth the trip.

The only defence against these is re-verification, which is why
`.github/workflows/verify.yml` re-checks all 167 cited URLs every Monday and files a `link-rot`
issue when one outside the documented log stops resolving.

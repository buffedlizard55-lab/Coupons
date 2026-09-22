#!/usr/bin/env node
/* Render smoke test for the static site.

   Runs the real assets/js/app.js against the real generated dataset inside a
   minimal DOM shim (tests/dom_shim.js), so a data or template mistake shows up
   in CI instead of in a visitor's browser. No npm dependencies.

   The clock is pinned to 2026-10-05 \u2014 deliberately AFTER the dataset's
   verification date of 2026-09-22 \u2014 so the expiry logic is exercised on real
   entries: the P&G coupons (expiring 26\u201327 September) must render as Expired,
   the P&G/Costco rebate (purchase window closed 20 September) as Window closed,
   and SFMOMA's Free Family Day (25 October) as Active.

       node tests/test_site_render.js
*/
"use strict";

const fs = require("fs");
const path = require("path");
const vm = require("vm");
const shim = require("./dom_shim.js");

const ROOT = shim.repoRoot;
const TODAY_ISO = "2026-10-05";

let failures = 0;
let checks = 0;

function ok(cond, msg) {
  checks++;
  if (!cond) { failures++; console.error("  FAIL  " + msg); }
  else console.log("  ok    " + msg);
}
function eq(a, b, msg) { ok(a === b, msg + ` (got ${JSON.stringify(a)}, want ${JSON.stringify(b)})`); }
function textOf(node) { return node ? node.textContent : ""; }
function countClass(node, cls) { return shim.collect(node, "." + cls).length; }
function sleep(ms) { return new Promise((r) => setTimeout(r, ms)); }

/* Pin the clock before the app reads it. */
const RealDate = Date;
const FIXED = new RealDate(TODAY_ISO + "T12:00:00Z");
class PinnedDate extends RealDate {
  constructor(...args) { if (args.length === 0) super(FIXED.getTime()); else super(...args); }
  static now() { return FIXED.getTime(); }
}
Object.defineProperty(globalThis, "Date", { value: PinnedDate, writable: true, configurable: true });

(async function main() {

/* ---------------------------------------------------------------- boot site */

const env = shim.install(path.join(ROOT, "index.html"));
vm.runInThisContext(fs.readFileSync(path.join(ROOT, "assets/data/coupons.js"), "utf8"), { filename: "assets/data/coupons.js" });
ok(!!env.window.COUPON_DATA, "dataset global window.COUPON_DATA is present");

const DATA = env.window.COUPON_DATA;
const entries = DATA.entries;
vm.runInThisContext(fs.readFileSync(path.join(ROOT, "assets/js/app.js"), "utf8"), { filename: "assets/js/app.js" });

const byId = env.byId;
const cards = () => byId.get("cards").children;
const cardIds = () => cards().map((c) => c.id.replace(/^offer-/, ""));
const entryById = new Map(entries.map((e) => [e.id, e]));

/* Recompute the app's own status rules here so the assertions are independent. */
function expectedStatus(e) {
  if ((e.flags || []).some((f) => f.code === "announced-but-not-live")) return "notlive";
  if (e.bay_area && e.bay_area.available === false) return "notlive";
  if (e.purchase_window && e.purchase_window.end && e.purchase_window.end < TODAY_ISO) return "closed";
  if (e.expires) {
    if (e.expires < TODAY_ISO) return "expired";
    const days = Math.round((new RealDate(e.expires + "T23:59:59") - new RealDate(TODAY_ISO + "T00:00:00")) / 86400000);
    return days <= 7 ? "soon" : "active";
  }
  return "ongoing";
}
const statusOf = new Map(entries.map((e) => [e.id, expectedStatus(e)]));
const usable = entries.filter((e) => ["active", "soon", "ongoing"].includes(statusOf.get(e.id)));
const expired = entries.filter((e) => statusOf.get(e.id) === "expired");
const hidden = entries.filter((e) => ["notlive", "closed"].includes(statusOf.get(e.id)));

/* ------------------------------------------------------------- initial view */

console.log("\n[1] initial render  (clock pinned to " + TODAY_ISO + ")");
ok(cards().length > 0, `cards rendered (${cards().length})`);
eq(cards().length, usable.length, "default filters hide expired and not-redeemable offers");
ok(expired.length > 0, `the pinned date makes ${expired.length} real entries expired, so expiry logic is under test`);

const meta = textOf(byId.get("results-meta"));
ok(meta.includes(`${entries.length} verified offers shown`), "results counter reports the dataset size");
ok(meta.includes(DATA.meta.dataset.compiled_at), "results counter shows the verification date");
ok(meta.includes("2026") , "results counter shows the viewer's current date");

eq(byId.get("stat-strip").children.length, 6, "stat strip has six tiles");
ok(textOf(byId.get("stat-strip")).includes(String(entries.length)), "stat strip shows the entry count");
eq(textOf(byId.get("tab-count-excluded")), String(DATA.excluded.length), "rejected tab badge matches the excluded shard");
ok(countClass(byId.get("cat-filters"), "chip") > 5, `category chips rendered (${countClass(byId.get("cat-filters"), "chip")})`);
ok(countClass(byId.get("deal-filters"), "chip") > 3, "deal-type chips rendered");
ok(countClass(byId.get("level-filters"), "chip") >= 2, "verification-level chips rendered");
ok(countClass(byId.get("status-filters"), "chip") >= 2, "status chips rendered");
ok(textOf(byId.get("footer-meta")).includes(DATA.meta.dataset.compiled_at), "footer carries the verification date");

/* ------------------------------------------------------- every card is sound */

console.log("\n[2] card content integrity");
let missingSource = 0, badText = 0, noBadge = 0, noQuote = 0, badCard = "";
/* 'undefined' must not appear as a rendered value; hyphenated flag codes such as
   'eligibility-term-undefined' are legitimate text and are excluded. */
const artifact = /(?:^|[\s>(:,.])undefined(?:[\s<.,;)]|$)|\[object Object\]|(?:^|[\s>(:,.])NaN(?:[\s<.,;)]|$)/;
cards().forEach((card) => {
  const links = shim.collect(card, "a").filter((a) => (a.attributes.href || "").startsWith("http"));
  if (!links.length) missingSource++;
  if (artifact.test(textOf(card))) { badText++; badCard = card.id; }
  if (!countClass(card, "badge")) noBadge++;
  if (!countClass(card, "quote")) noQuote++;
});
eq(missingSource, 0, "every visible card links to at least one official source");
eq(badText, 0, "no card renders a JS artifact" + (badCard ? " (first: " + badCard + ")" : ""));
eq(noBadge, 0, "every card carries status/value/level badges");
eq(noQuote, 0, "every card quotes the offer text");

const firstCard = cards()[0];
ok(countClass(firstCard, "block") >= 2, "cards render their structured blocks (dates, requirements, Bay Area, sources)");
ok(textOf(firstCard).includes("Official source"), "cards label their citations as official sources");
ok(textOf(firstCard).includes("Show the evidence that was read"), "cards expose the evidence behind each citation");
ok(textOf(firstCard).includes("Bay Area availability"), "cards state Bay Area availability");

/* ------------------------------------------------------------------ filters */

console.log("\n[3] filters, toggles and search");
const before = cards().length;

const chip0 = byId.get("cat-filters").children[0];
const chipLabel = textOf(chip0);
chip0.dispatch("click");
ok(cards().length < before, `category chip narrows the list (${before} -> ${cards().length}) for "${chipLabel}"`);
eq(textOf(byId.get("cat-filters").children[0]) === chipLabel ? byId.get("cat-filters").children[0].getAttribute("aria-pressed") : "?",
   "true", "the rebuilt chip reports its pressed state to screen readers");
byId.get("cat-filters").children[0].dispatch("click");
eq(cards().length, before, "clicking the chip again restores the list");

byId.get("hide-expired").checked = false;
byId.get("hide-expired").dispatch("change");
eq(cards().length, before + expired.length, "unhiding expired offers adds exactly the expired entries");
ok(cards().some((c) => textOf(c).includes("Expired")), "an expired offer is labelled Expired rather than shown as available");
const expiredCard = cards().find((c) => textOf(c).includes("Expired"));
ok(expiredCard && expiredCard.classList.contains("is-expired"), "expired cards are visually de-emphasised");
byId.get("hide-expired").checked = true;
byId.get("hide-expired").dispatch("change");
eq(cards().length, before, "hiding expired offers again restores the count");

byId.get("hide-unavailable").checked = false;
byId.get("hide-unavailable").dispatch("change");
eq(cards().length, before + hidden.length, "unhiding not-redeemable offers adds exactly those entries");
ok(cards().some((c) => textOf(c).includes("Not redeemable yet") || textOf(c).includes("Window closed")),
   "not-redeemable offers say so on the card");
byId.get("hide-unavailable").checked = true;
byId.get("hide-unavailable").dispatch("change");

const noSpend = new Set(entries.filter((e) => e.categories.includes("no-spend-free")).map((e) => e.id));
byId.get("only-no-spend").checked = true;
byId.get("only-no-spend").dispatch("change");
ok(cards().length > 0 && cards().length < before, `no-spend-only filter works (${cards().length} cards)`);
ok(cardIds().every((id) => noSpend.has(id)), "no-spend filter returns only entries in the no-spend category");
byId.get("reset-filters").dispatch("click");
eq(cards().length, before, "reset filters restores the full usable list");
eq(byId.get("q").value, "", "reset filters clears the search box");

byId.get("only-flagged").checked = true;
byId.get("only-flagged").dispatch("change");
ok(cards().length > 0 && cards().length < before, `flagged-only filter works (${cards().length} cards)`);
ok(cards().every((c) => countClass(c, "flag") > 0), "flagged-only filter returns only cards carrying a flag");
byId.get("reset-filters").dispatch("click");

const q = byId.get("q");
q.value = "starbucks";
q.dispatch("input");
await sleep(250);
const starbucksHits = cards().length;
ok(starbucksHits > 0 && starbucksHits < before, `search narrows results (${starbucksHits} hits for "starbucks")`);
ok(cards().every((c) => /starbucks/i.test(textOf(c))), "every search hit mentions the query");

q.value = "rainbow.coop";
q.dispatch("input");
await sleep(250);
ok(cards().length > 0, "search matches on source domains, not just titles");

q.value = "zzzz-no-such-offer";
q.dispatch("input");
await sleep(250);
eq(cards().length, 0, "an unmatched search renders nothing");
eq(byId.get("empty-state").hidden, false, "the empty state is shown for an unmatched search");

byId.get("clear-q").dispatch("click");
await sleep(50);
eq(cards().length, before, "clearing the search restores the list");
eq(byId.get("empty-state").hidden, true, "the empty state is hidden again");

/* ------------------------------------------------------------------- sorting */

console.log("\n[4] sorting");
const sort = byId.get("sort");
sort.value = "value";
sort.dispatch("change");
ok(textOf(cards()[0]).includes("FREE"), "sorting by largest stated value puts no-spend offers first");
sort.value = "merchant";
sort.dispatch("change");
const merchants = cards().map((c) => textOf(shim.collect(c, "p")[0] || { textContent: "" }));
ok(cards().length === usable.length, "sorting does not change how many offers are shown");
sort.value = "status";
sort.dispatch("change");
eq(cards().length, usable.length, "returning to the default sort restores the list");

/* ------------------------------------------------------------------- routing */

console.log("\n[5] section routing");
function viewActive(name) {
  return byId.get("view-" + name).classList.contains("is-active") && !byId.get("view-" + name).hidden;
}
const VIEWS = ["browse", "flags", "excluded", "sources", "method", "next"];
function onlyActive(name) {
  return VIEWS.filter((v) => v !== name).every((v) => !byId.get("view-" + v).classList.contains("is-active"));
}

env.fireHashChange("#flags");
ok(viewActive("flags"), "#flags activates the irregularities view");
ok(onlyActive("flags"), "activating one view deactivates the others");
ok(byId.get("flag-list").children.length >= 3, `flags grouped by severity (${byId.get("flag-list").children.length} groups)`);
ok(textOf(byId.get("flag-list")).includes("CRITICAL"), "critical flags are listed first");
eq(countClass(byId.get("flag-summary"), "summary-card"), 4, "flag summary tiles rendered");
const flagItems = countClass(byId.get("flag-list"), "flag-item");
const flagTotal = entries.reduce((n, e) => n + (e.flags || []).length, 0);
eq(flagItems, flagTotal, `every flag in the dataset is listed (${flagTotal})`);

env.fireHashChange("#excluded");
ok(viewActive("excluded"), "#excluded activates the scam-watch view");
eq(byId.get("excluded-list").children.length, DATA.excluded.length, "every rejected claim is rendered");
ok(textOf(byId.get("excluded-list")).includes("Why it was rejected"), "rejections explain themselves");
ok(textOf(byId.get("excluded-list")).includes("What evidence would change the verdict"), "rejections say what would change the verdict");

env.fireHashChange("#sources");
ok(viewActive("sources"), "#sources activates the citation view");
const uniqueUrls = new Set(entries.flatMap((e) => (e.sources || []).map((s) => s.url)));
eq(byId.get("source-groups").children.length, uniqueUrls.size, "one row per unique citation URL");
ok(textOf(byId.get("source-groups")).includes("Show the evidence"), "each citation exposes the evidence that was read");

env.fireHashChange("#method");
ok(viewActive("method"), "#method activates the methodology view");
const methodText = textOf(byId.get("method-prose")) + byId.get("method-prose").innerHTML;
["Verification levels", "Verification methods", "Flag severities", "Categories used", "Deal types used",
 "Bay Area definition", "Reproducing the work", "Anti-hallucination rule"].forEach((h) =>
  ok(methodText.includes(h), `methodology section present: ${h}`)
);
ok(methodText.includes(DATA.meta.bay_area_counties.join(", ")), "the nine-county definition is rendered");

env.fireHashChange("#next");
ok(viewActive("next"), "#next activates the limitations view");
const nextText = byId.get("next-prose").innerHTML;
["Known limitations", "Next session", "How to contribute", "What this project is not"].forEach((h) =>
  ok(nextText.includes(h), `limitations section present: ${h}`)
);
ok(!nextText.includes("undefined"), "limitations prose has no unfilled template values");

/* ---------------------------------------------------------------- deep links */

console.log("\n[6] deep links");
const target = expired[0];
env.fireHashChange("#offer/" + target.id);
ok(viewActive("browse"), "an offer deep link returns to the browse view");
const deep = byId.get("offer-" + target.id) || cards().find((c) => c.id === "offer-" + target.id);
ok(!!deep, `deep-linked offer ${target.id} is present in the DOM`);
ok(deep && deep.classList.contains("is-focused"), "the deep-linked offer is highlighted");
ok(deep && textOf(deep).includes("Expired"), "a deep-linked expired offer still says Expired");
eq(byId.get("hide-expired").checked, false, "opening a deep link lifts the filters that would hide it");

const closedTarget = entries.filter((e) => statusOf.get(e.id) === "closed")[0];
if (closedTarget) {
  env.fireHashChange("#offer/" + closedTarget.id);
  const node = byId.get("offer-" + closedTarget.id) || cards().find((c) => c.id === "offer-" + closedTarget.id);
  ok(!!node && textOf(node).includes("Window closed"), `deep link to ${closedTarget.id} shows its closed purchase window`);
}

env.fireHashChange("#browse");
ok(viewActive("browse"), "#browse returns to the list");
ok(cards().length > 0, "the list is still populated after navigating away and back");

/* ------------------------------------------------------------------- output */

Object.defineProperty(globalThis, "Date", { value: RealDate, writable: true, configurable: true });
console.log(`\n${checks - failures}/${checks} checks passed`);
if (failures) { console.error(`${failures} FAILURES`); process.exit(1); }
console.log("site render smoke test: OK");

})().catch((err) => { console.error(err); process.exit(1); });

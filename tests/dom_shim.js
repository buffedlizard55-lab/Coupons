/* Minimal DOM shim so the site's front-end can be smoke-tested in Node without
   a browser or any npm dependency. It implements only what assets/js/app.js uses.
   Not a general-purpose DOM: it exists to catch runtime errors and to assert that
   the real dataset actually renders into cards, chips and sections. */
"use strict";

const fs = require("fs");
const path = require("path");

class ClassList {
  constructor(el) { this.el = el; this.set = new Set(); }
  add(...c) { c.forEach((x) => x && this.set.add(x)); }
  remove(...c) { c.forEach((x) => this.set.delete(x)); }
  contains(c) { return this.set.has(c); }
  toggle(c, force) {
    const want = force === undefined ? !this.set.has(c) : !!force;
    if (want) this.set.add(c); else this.set.delete(c);
    return want;
  }
  toString() { return [...this.set].join(" "); }
}

class El {
  constructor(tag) {
    this.tagName = String(tag).toUpperCase();
    this.childNodes = [];
    this.parentNode = null;
    this.attributes = {};
    this.dataset = {};
    this.style = {};
    this.classList = new ClassList(this);
    this.listeners = {};
    this.hidden = false;
    this.checked = false;
    this.value = "";
    this._text = "";
    this._html = "";
    this.id = "";
  }
  get className() { return this.classList.toString(); }
  set className(v) {
    this.classList.set = new Set(String(v).split(/\s+/).filter(Boolean));
  }
  get children() { return this.childNodes.filter((n) => n instanceof El); }
  appendChild(node) {
    if (node instanceof TextNode) node.parentNode = this;
    else if (node) node.parentNode = this;
    this.childNodes.push(node);
    return node;
  }
  setAttribute(k, v) {
    this.attributes[k] = String(v);
    if (k === "id") this.id = String(v);
    if (k === "class") this.className = String(v);
  }
  getAttribute(k) { return k in this.attributes ? this.attributes[k] : null; }
  removeAttribute(k) { delete this.attributes[k]; }
  addEventListener(type, fn) { (this.listeners[type] = this.listeners[type] || []).push(fn); }
  removeEventListener(type, fn) {
    this.listeners[type] = (this.listeners[type] || []).filter((f) => f !== fn);
  }
  dispatch(type, event) {
    (this.listeners[type] || []).forEach((fn) => fn(event || { target: this, preventDefault() {} }));
  }
  get textContent() {
    if (this._text) return this._text;
    return this.childNodes.map((n) => n.textContent).join("");
  }
  set textContent(v) {
    this._text = v === null || v === undefined ? "" : String(v);
    this.childNodes = [];
    this._html = "";
  }
  get innerHTML() { return this._html; }
  set innerHTML(v) { this._html = String(v); this._text = ""; this.childNodes = []; }
  scrollIntoView() {}
  focus() {}
  querySelectorAll(sel) { return collect(this, sel); }
  toString() { return `<${this.tagName.toLowerCase()} id="${this.id}">`; }
}

class TextNode {
  constructor(text) { this.data = String(text); this.parentNode = null; }
  get textContent() { return this.data; }
  set textContent(v) { this.data = String(v); }
}

function collect(root, selector) {
  /* supports ".class" and "tag" selectors only — that is all app.js uses */
  const out = [];
  const wantClass = selector.startsWith(".") ? selector.slice(1) : null;
  const wantTag = wantClass ? null : selector.toUpperCase();
  (function walk(node) {
    node.children.forEach((child) => {
      if (wantClass ? child.classList.contains(wantClass) : child.tagName === wantTag) out.push(child);
      walk(child);
    });
  })(root);
  return out;
}

function buildFromHtml(htmlPath) {
  /* Create a stub element for every id and every class="tab"/class="view" in the
     real index.html, so app.js finds exactly the hooks the page provides. */
  const html = fs.readFileSync(htmlPath, "utf8");
  const byId = new Map();
  const root = new El("body");

  const tagRe = /<([a-zA-Z0-9]+)([^>]*)>/g;
  let m;
  while ((m = tagRe.exec(html)) !== null) {
    const attrs = m[2];
    const idMatch = /\sid="([^"]+)"/.exec(attrs);
    if (!idMatch) continue;
    const el = new El(m[1]);
    el.id = idMatch[1];
    el.attributes.id = el.id;
    const classMatch = /\sclass="([^"]+)"/.exec(attrs);
    if (classMatch) el.className = classMatch[1];
    const dataView = /\sdata-view="([^"]+)"/.exec(attrs);
    if (dataView) el.dataset.view = dataView[1];
    const hidden = /\shidden(\s|>|\/)/.test(attrs + ">");
    el.hidden = hidden;
    byId.set(el.id, el);
    root.appendChild(el);
  }
  return { root, byId };
}

function findByIdInTree(root, id) {
  /* A browser finds dynamically created nodes too, so the shim walks the tree
     when the id was not present in the original HTML. */
  let found = null;
  (function walk(node) {
    if (found) return;
    node.children.forEach((child) => {
      if (found) return;
      if (child.id === id || child.attributes.id === id) found = child;
      else walk(child);
    });
  })(root);
  return found;
}

function install(htmlPath) {
  const { root, byId } = buildFromHtml(htmlPath);

  const document = {
    readyState: "complete",
    body: root,
    documentElement: new El("html"),
    createElement: (tag) => new El(tag),
    createTextNode: (t) => new TextNode(t),
    getElementById: (id) => byId.get(id) || findByIdInTree(root, id),
    querySelectorAll: (sel) => collect(root, sel),
    addEventListener: () => {},
  };

  const listeners = {};
  const win = {
    COUPON_DATA: undefined,
    addEventListener: (t, fn) => { (listeners[t] = listeners[t] || []).push(fn); },
    dispatch: (t, e) => (listeners[t] || []).forEach((fn) => fn(e || {})),
    scrollTo: () => {},
  };

  /* Node 22 defines some of these as getter-only globals, so defineProperty is required. */
  const define = (name, value) => Object.defineProperty(globalThis, name, { value, writable: true, configurable: true });
  const loc = { hash: "", origin: "https://example.invalid", pathname: "/" };
  define("window", win);
  define("document", document);
  define("navigator", { clipboard: { writeText: async () => {} } });
  define("location", loc);

  return {
    window: win,
    document,
    root,
    byId,
    location: loc,
    fireHashChange: (h) => { loc.hash = h; win.dispatch("hashchange"); },
  };
}

module.exports = { install, El, TextNode, collect, buildFromHtml, repoRoot: path.resolve(__dirname, "..") };

// Figure 1: step-by-step workflow of the heterogeneity app, high resolution (Playwright + Chromium, headless).
// Viewport 640 x 900 CSS px (the page's single-column layout), light theme, device scale factor 4 (at least 3x; 4 so that
// panels are >= 300 dpi at 170 mm with text >= 8 pt). compose.py lays the regions out (tight crops, labelled
// sub-panels) and checks legibility from the font sizes recorded here. The floating method-help language switch and
// the back-to-hub link are hidden (page furniture that otherwise overlaps the panels).
// Data: the BCG vaccine trials exactly as in the corpus (metadat dat.bcg, log risk ratios; analysis dat.bcg#1), pasted
// in the app's "label, estimate, SE" format; for step 5, the app's own built-in example (8 trials).
//   node docs/screenshots/capture.mjs <work-dir> http://localhost:8000/app/heterogeneity/index.html corpus/corpus.csv
//   python docs/screenshots/compose.py <work-dir> docs/screenshots
import { chromium } from "playwright";
import { readFileSync, writeFileSync, mkdirSync } from "fs";
const [D, APP, CORPUS] = process.argv.slice(2);
const OUT = `${D}/regions`; mkdirSync(OUT, { recursive: true });
const DPR = 4;
const rows = readFileSync(CORPUS, "utf8").trim().split(/\r?\n/);
const head = rows.shift().split(",").map((h) => h.replace(/"/g, ""));
const parse = (l) => { const o = [], re = /("([^"]|"")*"|[^,]*)(,|$)/g; let m; while ((m = re.exec(l)) && o.length < head.length) o.push(m[1].replace(/^"|"$/g, "").replace(/""/g, '"')); return Object.fromEntries(head.map((h, i) => [h, o[i]])); };
const bcg = rows.map(parse).filter((r) => r.analysis === "dat.bcg#1");
const BCG = bcg.map((r) => `${r.slab}, ${r.yi}, ${r.sei}`).join("\n");
const b = await chromium.launch(process.env.APP_CHROME_CHANNEL ? { channel: process.env.APP_CHROME_CHANNEL } : {});
const ctx = await b.newContext({ viewport: { width: 640, height: 900 }, colorScheme: "light", deviceScaleFactor: DPR });
const p = await ctx.newPage();
const errs = []; p.on("pageerror", (e) => errs.push(e.message));
const meta = { dpr: DPR, viewport: [640, 900], regions: {}, states: {} };
await p.goto(APP); await p.evaluate(() => { try { localStorage.clear(); } catch (e) {} }); await p.goto(APP); await p.waitForTimeout(600);
await p.addStyleTag({ content: "#hub-back,.alm-lang-switch{display:none!important}" });
const type = async (text, est) => {
  await p.evaluate(([t, e]) => { const ta = document.getElementById("f-data"); ta.value = t; ta.scrollTop = 0;
    document.getElementById("f-tau2").value = e; ta.dispatchEvent(new Event("input", { bubbles: true })); }, [text, est]);
  await p.waitForTimeout(500);
};
const state = async (name) => (meta.states[name] = await p.evaluate(() => ({ stats: document.getElementById("stats-wrap").innerText,
  notes: document.getElementById("warn-banner").innerText })));
const rect = (sel, opt = {}) => p.evaluate(([sel, opt]) => {
  const pick = (tag, t) => [...document.querySelectorAll(tag)].find((h) => h.textContent.trim().startsWith(t));
  let e = sel.startsWith("h2:") ? pick("h2", sel.slice(3)) : sel.startsWith("legend:") ? pick("legend", sel.slice(7)) : document.querySelector(sel);
  if (!e) throw new Error("missing " + sel);
  if (opt.closest) e = e.closest(opt.closest);
  const r = e.getBoundingClientRect(); return { x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height };
}, [sel, opt]);
async function region(name, r, pad = 6) {
  const c = { x: Math.max(0, Math.floor(r.x - pad)), y: Math.max(0, Math.floor(r.y - pad)), width: Math.ceil(r.w + 2 * pad), height: Math.ceil(r.h + 2 * pad) };
  await p.screenshot({ path: `${OUT}/${name}.png`, clip: c, fullPage: true });
  const fonts = await p.evaluate((c) => {
    const out = [];
    const inside = (rr) => rr.width > 0 && rr.height > 0 && rr.left + scrollX >= c.x - 1 && rr.right + scrollX <= c.x + c.width + 1 && rr.top + scrollY >= c.y - 1 && rr.bottom + scrollY <= c.y + c.height + 1;
    const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    for (let n = tw.nextNode(); n; n = tw.nextNode()) {
      const t = n.textContent.trim(); if (t.length < 2) continue;
      const el = n.parentElement; const cs = getComputedStyle(el); if (cs.visibility === "hidden" || cs.display === "none") continue;
      if (el.tagName === "TEXTAREA" || el.tagName === "SCRIPT" || el.tagName === "STYLE" || el.tagName === "OPTION") continue;
      const range = document.createRange(); range.selectNodeContents(n); const rr = range.getBoundingClientRect(); if (!inside(rr)) continue;
      let px = parseFloat(cs.fontSize);
      if (el.closest("svg") && el.getScreenCTM) { const m = el.getScreenCTM(); if (m) px = px * Math.hypot(m.a, m.b); }
      out.push([Math.round(px * 100) / 100, t.length]);
    }
    document.querySelectorAll("textarea, input[type=text], select").forEach((f) => { const rr = f.getBoundingClientRect(); if (inside(rr)) out.push([parseFloat(getComputedStyle(f).fontSize), 10]); });
    return out;
  }, c);
  meta.regions[name] = { clip: c, fonts };
}

// 1 data entry: the BCG trials (label, log risk ratio, SE)
await type(BCG, "reml");
await region("d1_data", await rect("legend:Data", { closest: "fieldset" }));
// 2 options: the tau^2 estimator (REML)
await state("step2");
await region("d2_options", await rect("legend:Options", { closest: "fieldset" }));
// 3 summary: Q, I^2 with its Q-profile CI, tau^2 by estimator and its CI, pooled estimate (z and HKSJ), prediction interval
await region("d3_stats", await rect("#stats-wrap .stats"));
// 4 Baujat plot and leave-one-out table
await region("d4_baujat", await rect("#svg-host svg"), 2);
await region("d4_loo", await rect("#loo-table table"));
// 5 DerSimonian-Laird requested with k < 10 (the app's built-in example, 8 trials): refused with a note, PM shown
await p.click("#btn-example"); await p.waitForTimeout(400);
await p.evaluate(() => { const s = document.getElementById("f-tau2"); s.value = "dl"; s.dispatchEvent(new Event("input", { bubbles: true })); });
await p.waitForTimeout(500); await state("step5");
await region("d5_note", await rect("#warn-banner"), 1);
await region("d5_stats", await rect("#stats-wrap .stats"));
// 6 export: results (Methods + Results, CSV, JSON), figures and the GRADE hand-off
await type(BCG, "reml");
await p.evaluate(() => document.activeElement && document.activeElement.blur());
await region("d6_export", await rect("#alm-export-mount"));
await region("d6_actions", await rect(".actions"));
meta.errors = errs;
writeFileSync(`${D}/regions_meta.json`, JSON.stringify(meta, null, 1));
console.log(JSON.stringify({ states: meta.states, regions: Object.keys(meta.regions), errors: errs }, null, 1));
await b.close();

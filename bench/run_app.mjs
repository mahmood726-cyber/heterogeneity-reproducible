// Run the app itself (app/heterogeneity/index.html, unchanged, in headless Chromium) on every meta-analysis of the
// corpus with every tau^2 estimator it offers, and record every number it reports at full precision.
//
//   node bench/run_app.mjs corpus/corpus.csv results/full/app.jsonl
//
// Each meta-analysis is typed into the page as the app's own "label, estimate, SE" lines and analysed by the page's
// own parser and statistics (window.__almHetCompute, the function the page renders from). The page is then rendered
// for that estimator and every number it DISPLAYS (summary cards and leave-one-out table) is checked against the
// computed value, rounded as displayed. Output: one JSON object per meta-analysis per line.
import { readFileSync, writeFileSync } from "fs";
import { createHash } from "crypto";
import { dirname, join, resolve } from "path";
import { fileURLToPath, pathToFileURL } from "url";
import { chromium } from "playwright";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const PAGE = pathToFileURL(resolve(ROOT, "app", "heterogeneity", "index.html")).href;
const KEYS = ["pm", "reml", "ml", "eb", "sj", "he", "hs", "dl"];

function parseCSV(text) {
  const rows = []; let row = [], cur = "", q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) { if (c === '"') { if (text[i + 1] === '"') { cur += '"'; i++; } else q = false; } else cur += c; }
    else if (c === '"') q = true;
    else if (c === ",") { row.push(cur); cur = ""; }
    else if (c === "\n") { row.push(cur); rows.push(row); row = []; cur = ""; }
    else if (c !== "\r") cur += c;
  }
  if (cur.length || row.length) { row.push(cur); rows.push(row); }
  const h = rows.shift();
  return rows.filter((r) => r.length > 1).map((r) => Object.fromEntries(h.map((k, i) => [k, r[i]])));
}

const [corpusFile, out] = process.argv.slice(2);
const corpus = parseCSV(readFileSync(corpusFile, "utf8"));
const ids = [...new Set(corpus.map((r) => r.analysis))];
const browser = await chromium.launch(process.env.APP_CHROME_CHANNEL ? { channel: process.env.APP_CHROME_CHANNEL } : {});
const page = await browser.newPage();
const errors = []; page.on("pageerror", (e) => errors.push(e.message));
await page.goto(PAGE); await page.evaluate(() => { try { localStorage.clear(); } catch (e) {} }); await page.goto(PAGE);
await page.waitForFunction(() => typeof window.__almHetCompute === "function");

// Displayed number -> |shown - computed| <= half a unit in the last displayed place.
const near = (shown, value, d) => Number.isFinite(value) ? Math.abs(parseFloat(shown) - value) <= 0.5 * 10 ** -d * (1 + 1e-9) + 1e-12 : shown === "--";

const lines = [];
for (const id of ids) {
  const rows = corpus.filter((r) => r.analysis === id);
  // The app's own input format: label, estimate, SE. A label must not start with "#" (the app's comment marker).
  const text = rows.map((r) => `${r.slab.replace(/^#/, "No. ")}, ${r.yi}, ${r.sei}`).join("\n");
  const rec = { analysis: id, k_input: rows.length, configs: {}, display: {} };
  for (const key of KEYS) {
    const res = await page.evaluate(([t, k]) => window.__almHetCompute(t, k), [text, key]);
    rec.configs[key] = res;
    // render the same input for this estimator and read what the page shows
    const shown = await page.evaluate(([t, k]) => {
      const ta = document.getElementById("f-data"); ta.value = t;
      document.getElementById("f-tau2").value = k;
      ta.dispatchEvent(new Event("input", { bubbles: true }));
      const cards = Object.fromEntries([...document.querySelectorAll("#stats-wrap .stat")].map((s) =>
        [s.querySelector(".k").textContent.trim(), s.querySelector(".v").textContent.trim()]));
      const loo = [...document.querySelectorAll("#loo-table tr")].slice(1).map((tr) => [...tr.children].map((td) => td.textContent.trim()));
      return { cards, loo };
    }, [text, key]);
    const fails = [];
    const nums = (s) => (s.match(/-?\d+(\.\d+)?|--/g) || []);
    const S = res.sum, C = shown.cards;
    const chk = (name, s, vals, dps) => { const n = nums(s || ""); vals.forEach((v, i) => { if (!near(n[i], v, dps[i])) fails.push(`${name}[${i}] shows ${n[i]} for ${v}`); }); };
    const qtext = C[`Q (df=${S.df})`] || "";
    chk("Q", qtext, [S.Q], [2]);
    if (S.pQ < 0.0005 ? !/p<0\.001/.test(qtext) : !near(nums(qtext)[1], S.pQ, 3)) fails.push(`p(Q) shows ${qtext} for ${S.pQ}`);
    const used = C["τ² used"] || "";
    chk("tau2used", used, [res.tau2], [4]);
    if (!used.includes(`(${res.estimator.toUpperCase()})`)) fails.push(`tau2used names ${used} for ${res.estimator}`);
    chk("I2", C["I²"], [S.I2, res.qpci.I2Lo, res.qpci.I2Hi], [1, 1, 1]);
    chk("tau2CI", C["τ² 95% CI (Q-profile)"], [res.qpci.tau2Lo, res.qpci.tau2Hi], [4, 4]);
    chk("tau2PM", C["τ² (PM)"], [res.tauEstimates.pm], [4]);
    chk("tau2REML", C["τ² (REML)"], [res.tauEstimates.reml], [4]);
    if (res.tauEstimates.dl != null) chk("tau2DL", C["τ² (DL)"], [res.tauEstimates.dl], [4]);
    chk("REz", C["RE pooled (z)"], [S.mu, S.ciLo, S.ciHi], [3, 3, 3]);
    chk("REhk", C["RE pooled (HKSJ + t)"], [S.mu, S.ciLoHKSJ, S.ciHiHKSJ], [3, 3, 3]);
    chk("PI", C["95% PI"], [res.pi.lo, res.pi.hi], [3, 3]);
    res.loo.forEach((r, i) => {
      const t = shown.loo[i] || [];
      if (String(r.k) !== t[1]) fails.push(`loo[${i}].k`);
      chk(`loo[${i}].mu`, t[2], [r.mu], [3]); chk(`loo[${i}].ci`, t[3], [r.ciLo, r.ciHi], [3, 3]);
      chk(`loo[${i}].I2`, t[4], [r.I2], [1]); chk(`loo[${i}].tau2`, t[5], [r.tau2], [4]);
    });
    rec.display[key] = { numbers: 19 + 6 * res.loo.length - (res.tauEstimates.dl == null ? 1 : 0), fails };
  }
  lines.push(JSON.stringify(rec));
}
const chromiumVersion = browser.version();
await browser.close();
writeFileSync(out, lines.join("\n") + "\n");
const sha = createHash("sha256").update(readFileSync(resolve(ROOT, "app", "heterogeneity", "index.html"))).digest("hex").slice(0, 12);
console.log(`app: ${ids.length} meta-analyses x ${KEYS.length} estimators (app/heterogeneity/index.html sha256 ${sha}; Chromium ${chromiumVersion})` +
            (errors.length ? `; PAGE ERRORS: ${errors.join(" | ")}` : ""));
if (errors.length) process.exit(1);

# heterogeneity-reproducible

[![reproduce](https://github.com/mahmood726-cyber/heterogeneity-reproducible/actions/workflows/reproduce.yml/badge.svg)](https://github.com/mahmood726-cyber/heterogeneity-reproducible/actions/workflows/reproduce.yml)
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/mahmood726-cyber/heterogeneity-reproducible?quickstart=1)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Latest verified run](https://img.shields.io/badge/latest%20verified%20run-results%20page-2c5e8a)](https://mahmood726-cyber.github.io/heterogeneity-reproducible/)

The [allmeta](https://github.com/mahmood726-cyber/allmeta) **heterogeneity app** quantifies between-study heterogeneity in a
pairwise meta-analysis offline in the browser ([live](https://mahmood726-cyber.github.io/allmeta/heterogeneity/)). From one row per
study (label, estimate, standard error) it reports:

- **Between-study variance τ²** by eight estimators: Paule–Mandel (PM), REML, maximum likelihood (ML), empirical Bayes (EB),
  Sidik–Jonkman (SJ), Hedges (HE), Hunter–Schmidt (HS) and DerSimonian–Laird (DL; offered only for k ≥ 10, otherwise PM is
  used and the page says so).
- **Heterogeneity:** Q with its df and p-value, I² (Higgins–Thompson, from Q), and Q-profile 95% confidence intervals for τ² and I².
- **Pooled estimate:** random-effects mean with a normal (z) 95% CI and a Hartung–Knapp–Sidik–Jonkman (HKSJ) 95% CI on t(k−1),
  with the scaling factor floored at 1; the 95% prediction interval on t(k−1).
- **Influence:** leave-one-out estimates (τ² re-estimated) and a Baujat plot; CSV, JSON and Markdown export.

This repository validates every one of those numbers against the R package **metafor**, on every random- or fixed-effects model
without moderators fitted in the examples of the dataset package **metadat**, and checks every number in the accompanying
F1000Research article.

## Reproduce in one click

**1. See the latest verified run (nothing to run).** The [results page](https://mahmood726-cyber.github.io/heterogeneity-reproducible/)
is republished by CI after every push to `main`: the PASS/FAIL table for every number in the paper, the result on Docker, Linux,
Windows and macOS, the cross-platform comparison, and the figures.

**2. Open in GitHub Codespaces (one click).** Click the *Open in GitHub Codespaces* badge above, then *Create codespace*.
- The pinned environment is built from this repository's `Dockerfile`: R 4.6.0, metafor and metadat from a dated package
  snapshot, Node 24.15.0 with Playwright's Chromium, and Python.
- The quick reproduction (3 meta-analyses) then runs automatically. Its log ends with `QUICK RUN: ALL PASS`; the report is in
  `outputs/quick/reproduction_report.md`.
- For the full run, type `python reproduce.py` in the terminal (about 10 minutes; writes `outputs/full/`).

Limits: you need to be signed in to GitHub; the codespace uses your own Codespaces allowance (personal accounts get a free monthly
quota; this uses a 2-core machine); the first build takes several minutes. `codespaces-check` in Actions builds the same
devcontainer and runs its automatic quick run on every relevant change.

**3. Re-run the CI yourself (one click in a fork).** Only maintainers can trigger workflows here, so use your own copy:
1. Click **Fork**.
2. In your fork, open the **Actions** tab and click *I understand my workflows, go ahead and enable them*.
3. Choose **reproduce**, then **Run workflow** (branch `main`).

The run is the full validation on Docker, Linux, Windows and macOS. Each job's **summary** shows its PASS/FAIL report;
**Artifacts** hold `reproduction-report-<platform>` and the complete outputs (`full-<platform>`); the *compare* job shows the
cross-platform check. Publishing to Pages happens only on this repository.

**On your own machine:**

```bash
git clone https://github.com/mahmood726-cyber/heterogeneity-reproducible && cd heterogeneity-reproducible
docker build -t heterogeneity . && docker run --rm -v "$PWD/outputs:/work/outputs" heterogeneity        # canonical
```

Without Docker you need R 4.6.0, Node 24.15.0 and Python 3.12 or 3.13:
1. `Rscript bench/install_r_packages.R`
2. `python -m pip install -r requirements.txt`
3. `npm ci` and `npx playwright install chromium`
4. `python reproduce.py` (or `--quick`)

`make setup` and `make reproduce` do the same. **To use the app**, open `app/heterogeneity/index.html` in a browser.

## What it shows

The app is validated at **allmeta commit `7cb5975`** (the merge of
[allmeta PR #82](https://github.com/mahmood726-cyber/allmeta/pull/82)). `app/` is byte-identical to that commit.

| | Result |
|---|---|
| Corpus: every random- or fixed-effects model without moderators fitted in the examples of metadat 1.6-0 — 88 meta-analyses from 49 datasets (2,241 study rows; 4–160 studies; 23 effect measures) — each with the app's 8 τ² estimators = 704 analyses | All 131,781 checks pass: the same 28 analyses refused by both (DerSimonian–Laird with fewer than 10 studies) and every reported number of the other 676 within 10⁻⁹ — in fact below 5 × 10⁻¹⁰, and below 10⁻¹⁰ for estimates and intervals. |
| What the page displays | All 120,720 displayed numbers equal the computed values as rounded. |
| metafor's own convergence | With metafor's default controls τ² moves by up to 10⁻⁴ relative (Table 4); the comparison uses tight controls. In one meta-analysis the upper Q-profile limit of τ² lies beyond metafor's default search range (100). |
| Worked example: BCG vaccine (13 trials) | Q = 152.2 (12 df); I² 92.1% (81.9% to 97.7%); τ² from 0.228 (Hunter–Schmidt) to 0.346 (Sidik–Jonkman). REML: risk ratio 0.49 (Hartung–Knapp 95% CI 0.33 to 0.73; prediction interval 0.14 to 1.76); Hart & Sutherland (1977) most influential. |

Earlier versions of the app had known issues, found by this validation and fixed in allmeta PR #82; see [CHANGELOG.md](CHANGELOG.md).

**What is not compared:** moderators and multilevel models (the app has none); the Baujat *plot* itself (its coordinates are
compared); the 2 metadat help pages whose examples exceed the time limit fit only multilevel models (`rma.mv`), so no
univariate model is lost.

## How the comparison works

- **Corpus.** `bench/build_corpus.py` runs the help-page examples of every dataset in metadat 1.6-0 (including those marked "do not
  run", which hold the analyses), each in its own R process, with `rma()`/`rma.uni()` shadowed by a function that calls
  `metafor::rma.uni()` and records the exact `yi` and `vi` of every model fitted without moderators. Each distinct set of data is one
  meta-analysis; the same data fitted again (another estimator, a plot) counts once. Included: at least 2 studies, every variance
  positive. `corpus/corpus_log.tsv` lists every help page and what happened to it. This takes about half an hour, so the corpus is
  committed in `corpus/`; `python reproduce.py --rebuild-corpus` regenerates it and stops unless it is byte-identical.
- **The app** (`app/`, byte-identical to the validated allmeta commit) runs unchanged in headless Chromium. Each meta-analysis is typed
  in the app's own input format (`label, estimate, SE`) and analysed by the page's own parser and statistics
  (`window.__almHetCompute`, the function the page renders from) for each of the eight estimators. The page is then rendered and
  every number it displays is checked against the computed value, rounded as displayed.
- **metafor** (`bench/reference_metafor.R`) analyses the same data (variance = the square of the SE the app was given):

  | App | metafor |
  |---|---|
  | τ², pooled estimate, SE, 95% CI (z) | `rma(yi, vi, method = M)` |
  | HKSJ 95% CI (scaling factor floored at 1) | `rma(..., test = "adhoc")` |
  | 95% prediction interval (t, k − 1 df, unadjusted SE) | `predict(rma(..., test = "t"))` |
  | Q, df, p; I² from Q | `rma()$QE`, `$QEp`; `rma(..., method = "DL")$I2` |
  | Q-profile 95% CIs of τ² and I² | `confint(rma(...))` |
  | Leave-one-out estimate, 95% CI, τ², I² | `rma(..., method = M)` refitted without each study, as `leave1out()` (I² from its Q) |
  | Baujat x and y | `baujat(rma(..., method = M))` |

  Iterative estimators are fitted with tight convergence controls (metafor's threshold is an absolute change in τ²: 1e-12, and
  1e-12 × τ² for τ² < 10⁻³); `confint()` searches for the upper bound up to τ² = 10⁹ (metafor's default stops at 100 and then
  reports 100). Results with metafor's default controls are recorded too (Table 4).
- **Checks and tolerances** are defined in `analysis/checks.py`. A check is one number the app reports for one meta-analysis, compared
  with metafor's. Relative tolerance 10⁻⁹ (difference divided by max(1, |metafor|)) for estimates, SEs, intervals, τ² and its CI, Q,
  leave-one-out values and Baujat coordinates; absolute 10⁻⁹ for I², its CI and the p-value of Q; exact for k, df and refusals.

## Layout

| Path | Contents |
|---|---|
| `app/` | The app, byte-identical to the validated allmeta commit |
| `corpus/` | The corpus (`corpus.csv`), the log of every metadat help page, and its summary |
| `bench/build_corpus.py`, `capture_one.R`, `assemble_corpus.R` | Build the corpus from metadat's examples |
| `bench/reference_metafor.R` | metafor reference analyses |
| `bench/run_app.mjs` | Runs the app itself in headless Chromium on the same data |
| `analysis/checks.py` | What one check is, and the tolerances |
| `analysis/make_outputs.py` | Tables, figures, statistics, PASS/FAIL |
| `analysis/compare_runs.py` | Cross-platform comparison |
| `expected/` | Every number as printed in the paper |
| `docs/` | Paper, `numbers.json`, Figure 1 screenshots and their capture script |
| `ci/build_site.py` | Builds the live results page from a CI run (reads outputs only) |
| `.devcontainer/` | Codespaces / dev-container definition; runs the quick reproduction on creation |

## Outputs and how they map to the paper

`python reproduce.py` writes to `outputs/full/`:

| File | Paper |
|---|---|
| `docs/screenshots/step1.png` … `step6.png` | Figure 1: using the app, step by step (`captions.md`) |
| `figure2_worked_example.png` (+ `.csv`) | Figure 2: BCG vaccine, estimates by τ² estimator and Baujat plot |
| `figure3_agreement.png` (+ `.csv`) | Figure 3: agreement for every quantity and meta-analysis |
| `table1_by_dataset.csv` | Table 1: agreement by dataset |
| `table2_by_quantity.csv` | Table 2: largest difference by quantity, with its tolerance |
| `table3_all_analyses.csv` | Every meta-analysis and estimator (extended data) |
| `table4_metafor_default_controls.csv` | Table 4: metafor's default convergence controls versus the tight ones |
| `visual_abstract.png` | Visual abstract |
| `stats.json` | Every number quoted in the text |
| `reproduction_report.md` | Expected versus reproduced, PASS/FAIL per number |

## Environment and determinism

- **R 4.6.0.** The image is `rocker/r-ver:4.6.0`; metafor 5.2-1, metadat 1.6-0 and their dependencies come from the Posit Package
  Manager snapshot of 2026-10-01.
- **Node 24.15.0** (`.nvmrc`) with **Playwright 1.63.0** (`package-lock.json`) and its own Chromium runs the app.
- **Python** builds the tables and figures (numpy and matplotlib, pinned in `requirements.txt`).
- **Docker is the canonical environment.** CI runs the full validation on every push on Linux, Windows, macOS and Docker.
  `analysis/compare_runs.py` then requires the corpus and the app's output to be bit-identical across the x86-64 runs; macOS on ARM is
  reported but not required to match.
- **metafor's own values** differ between operating systems in the last bits. The printed numbers are chosen to be robust to this,
  and are checked on every platform.

## Data

The corpus comes from the examples of metadat 1.6-0 (GPL (>= 2)), whose help pages document each dataset's original source; the
paper cites every one. `dat.colditz1994` repeats `dat.bcg` (metadat ships both) and is kept as metadat ships it.

## Cite

Ahmad M. Heterogeneity in meta-analysis in the browser: a tool validated against the R package metafor [software], v1.0.0. Zenodo;
2026. (DOI to be added on release.) Machine-readable metadata: `CITATION.cff`.

## Licence

MIT, the same as allmeta.

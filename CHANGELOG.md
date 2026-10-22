# Changelog

## v1.1.0 — 2026-10-22

**Release run passed (RUN_EXIT 0).** Updated the app and its runtime/data dependencies to
allmeta v1.8.0, commit `1cb3f8409c7af75ed41f7e1811f9c502f900fc79`,
release DOI 10.5281/zenodo.23515177 (concept 10.5281/zenodo.20516880).

The original corpus, R reference code, expected values and tolerances are
byte-identical to the pre-recut archive. The display runner follows the current
card labels, retaining the original Q-based I² point and both model-based interval
endpoints. The original targets remain 131,781 numerical and 120,720 display
checks; the final run met both targets. No numerical plus suite applies (APP.txt:
PR #163, strict numeric input usability).

Added portable runner instructions, SHA-256 manifests and verification, output
preservation, and an explicit extras scope note. Desktop R metafor 5.2-1 remains
the reference; the bundled optional live webR metafor 4.8-0 is documented separately.
All app source bytes, including manifests and references, are copied unchanged.

Quick: 4934/4934 numerical, 4480/4480 display, 11/11 expected values. Full: 131781/131781 numerical, 120720/120720 display, 44/44 expected values.
No expected count differs from the final log. R 4.6.0 (metafor 5.2.1, metadat 1.6.0), Node 24.16.0 (Playwright 1.59.1), Python 3.13.13, Windows AMD64; Chromium 148.0.7778.96.
The alternate tool versions were permitted with `--allow-version-mismatch`;
see RECUT_NOTES.md and the [release log](provenance/run_plan-2026-10-22-release.log).

## v1.0.0 — historical validated version

The previous archive validated allmeta commit
`7cb5975429531791d1879e80cf5c05f765e82c21`, the merge of
[allmeta PR #82](https://github.com/mahmood726-cyber/allmeta/pull/82).

## Earlier versions of the app (history)

Versions of the app before PR #82 had known issues, all found by this repository's validation against metafor 5.2-1 and fixed in
PR #82. The τ² estimators, Q, I² and the Q-profile intervals already matched metafor to about 10⁻¹² on well-conditioned data.

| Issue | Before PR #82 | Since PR #82 |
|---|---|---|
| t quantile | The page's own bisection stopped at a 10⁻⁶ bracket (2.1788131 for 12 df; R's `qt(0.975, 12)` is 2.1788128), so the Hartung–Knapp interval and the prediction interval differed from metafor in the 7th significant digit. | The shared exact inversion in `shared/ma-core.js`. |
| REML and ML τ² | The fixed-point iteration stopped at an absolute change of 10⁻¹², leaving a relative error of about 10⁻⁷ when τ² is about 10⁻⁵ (studies with very small variances, e.g. `dat.hart1999`). | Polished to machine precision on the likelihood score (safeguards unchanged). |
| Baujat plot | The influence axis held τ² fixed and divided by the variance of the full-model estimate — neither Baujat et al.'s definition nor metafor's — while the page's own leave-one-out table re-estimated τ². Labels ran off the plot and over each other; text too small to read in print. | Influence from the leave-one-out refit (τ² re-estimated) divided by its variance, as `metafor::baujat()`; labels kept inside and apart, each point labelled as a tooltip; larger text; axes titled as defined. |
| Reporting | The τ² actually used, and its estimator, were not shown for ML, EB, SJ, HE and HS; uppercasing turned μ into "M" and τ into "T"; p-value of Q shown as 0.000; the note for DerSimonian–Laird below 10 studies named an internal file; the results export lacked the prediction interval. | A "τ² used" card names the estimator; labels shown as written; p < 0.001; plain-language note; the export includes the prediction interval and the estimator. |
| Built-in BCG dataset | Shared by several allmeta apps: four wrong variances (Ferguson 1949 0.0786, should be 0.1946; Rosenthal 1960 0.0408 → 0.4154; Hart 1977 0.0203 → 0.0200; TPT Madras 0.0044 → 0.0040) and a wrong year (Comstock & Webster 1956 → 1969). | Matches `metadat::dat.bcg`. |

PR #82 also adds a metafor parity test (`hub/shared/tests/heterogeneity-metafor-parity.spec.mjs`) and makes every reported number
available at full precision from one function (`window.__almHetCompute`), which this repository's runner calls.

## This repository

- **v1.0.0 (historical):** validation of the app against metafor 5.2-1 on every intercept-only `rma()` fit in the examples of metadat 1.6-0
  (88 meta-analyses, 49 datasets) with all eight τ² estimators: all 131,781 checks pass.

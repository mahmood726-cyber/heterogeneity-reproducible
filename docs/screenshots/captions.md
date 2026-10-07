# Figure 1: using the app, step by step

Data: the BCG vaccine trials exactly as in the corpus (metadat `dat.bcg`, log risk ratios from each trial's 2×2 counts; 13
trials; analysis `dat.bcg#1`), typed in the app's own `label, estimate, SE` format at full precision. Step 5 uses the app's
built-in 8-trial example. App: the validated allmeta commit (see CHANGELOG.md).

## How the images were captured
- **Browser:** Chromium, driven by Playwright (`capture.mjs`), light theme. The floating method-help language switch and the
  back-to-hub link are hidden (page furniture that otherwise overlaps the panels).
- **Window:** 640 × 900 CSS px (the page's single-column layout).
- **Resolution:** 4 device pixels per CSS pixel (at least the 3× asked for; 4 so that every panel is at least 300 dpi at 170 mm
  with text of at least 8 pt). No image is enlarged.
- **Cropping:** each image is cropped tightly to the panels it shows.
- **Composites:** steps 4–6 are labelled composites (A, B) of regions of one page state, stacked by `compose.py`. Steps 1–3 are
  single crops.
- **Formats:** final width 2392–2543 px, lossless PNG plus uncompressed TIFF at 357–380 dpi for a 170 mm print width.
- **Legibility:** text measured in the page prints at 8.4 pt or larger at 170 mm. See `legibility.json`.

## Steps
- **step1: Data entry.** One row per study (`label, estimate, SE`; the estimate is the log risk ratio).
- **step2: The τ² estimator.** REML chosen from the eight the app offers.
- **step3: Summary.** k = 13; Q = 152.23 (12 df, p < 0.001); I² 92.1% (Q-profile 95% CI 81.9 to 97.7); τ² 95% CI 0.1197 to 1.1115;
  τ² by Paule–Mandel 0.3181, REML 0.3132 and DerSimonian–Laird 0.3088; the τ² used (REML); the pooled log risk ratio −0.715
  with its normal 95% CI (−1.067 to −0.362) and Hartung–Knapp 95% CI (−1.108 to −0.321); the 95% prediction interval
  (−1.995 to 0.566).
- **step4: Influence (composite).**
  - (A) Baujat plot: squared Pearson residual against influence on the overall result; Hart & Sutherland (1977) is the most
    influential trial.
  - (B) Leave-one-out table: number of studies, estimate, 95% CI, I² and τ² with each trial omitted.
- **step5: DerSimonian–Laird below 10 studies (composite).** For the app's built-in 8-trial example:
  - (A) the note that DerSimonian–Laird is not used for k < 10 and Paule–Mandel is used instead;
  - (B) the summary, with τ² (DL) shown as skipped and the τ² used marked (PM).
- **step6: Export (composite).**
  - (A) Results as Markdown, text, JSON, CSV and data.
  - (B) Downloads of the Baujat plot (SVG, PNG) and the session (JSON), import, the shared-data buttons used by other allmeta apps, and a check in R run in the browser (WebR).

## To regenerate
Serve the repository root, for example `python -m http.server 8000`, then:

```bash
node docs/screenshots/capture.mjs work http://localhost:8000/app/heterogeneity/index.html corpus/corpus.csv
python docs/screenshots/compose.py work docs/screenshots
```

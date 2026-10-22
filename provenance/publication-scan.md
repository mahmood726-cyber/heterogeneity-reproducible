# Publication scan (2026-10-22)

Scope: every file under archive/ that is not excluded by .gitignore; repository
metadata is excluded. This includes the archive manifest and both scan reports.
The ignore-based inventory agrees exactly with scripts/recut.py plus its
self-excluded manifest. No previous-output or temporary folder is publishable.
No ignored output directory was deleted.

The scan uses case-insensitive byte-substring matching for every machine-path,
account-name and credential-prefix candidate requested in TASK_finalize2.md,
plus an email-address expression that also recognizes the CI bot address.
Text and binary files are scanned alike. Offsets are zero-based, end-exclusive;
line numbers are one-based byte line counts (not source lines for binary files).
Compressed files are scanned as published bytes, without decompression.
Every candidate has its own row in [publication-scan.csv](publication-scan.csv);
the report records locations and actions without repeating sensitive-looking
values. Short byte matches in binary or compressed data are candidates, not
proof of credentials. This is a pattern audit, not a guarantee about all content.

No local machine identity, personal email or credential value was found in
archive-owned publication files; no redaction was required there or in the
release log. Public author and copyright credit, source repository links,
the public automation no-reply identity, technical names and ordinary prose
are retained as reviewed false positives. Original author metadata is preserved.

All copied app candidates below are retained byte-for-byte under the explicit
upstream preservation requirement. They include virtual runtime home paths,
dependency attribution, public CA certificates and binary-prefix coincidences.
They are disclosed rather than scrubbed. The archive-owned original validation
and historical paper files also remain protected by their raw-byte anchors.

Files scanned: **227**. Candidate hits: **621**, in **46** files.

| Action | Hits |
|---|---:|
| retained-attribution | 3 |
| retained-automation | 1 |
| retained-public | 24 |
| retained-technical | 11 |
| retained-upstream | 582 |

## Files with candidates and disposition

| File | Hits | Ownership / action |
|---|---:|---|
| `.github/workflows/reproduce.yml` | 8 | Archive-owned; reviewed false positives retained |
| `.zenodo.json` | 3 | Archive-owned; reviewed false positives retained |
| `APP_SOURCE_FILES.json` | 1 | Archive-owned; reviewed false positives retained |
| `CHANGELOG.md` | 1 | Archive-owned; reviewed false positives retained |
| `CITATION.cff` | 4 | Archive-owned; reviewed false positives retained |
| `LICENSE` | 1 | Archive-owned; reviewed false positives retained |
| `README.md` | 10 | Archive-owned; reviewed false positives retained |
| `RUN_PLAN.cmd` | 1 | Archive-owned; reviewed false positives retained |
| `RUN_PLAN_EXPECTED.md` | 3 | Archive-owned; reviewed false positives retained |
| `analysis/make_outputs.py` | 1 | Archive-owned; reviewed false positives retained |
| `app/heterogeneity/validate/MANIFEST.json` | 1 | Copied allmeta; unchanged |
| `app/heterogeneity/validate/adapter.js` | 2 | Copied allmeta; unchanged |
| `app/hub/shared/vendor/jspdf.min.js` | 31 | Copied allmeta; unchanged |
| `app/r-shiny/shinylive/webr/R.js` | 235 | Copied allmeta; unchanged |
| `app/r-shiny/shinylive/webr/R.wasm` | 106 | Copied allmeta; unchanged |
| `app/r-shiny/shinylive/webr/library.data.gz` | 2 | Copied allmeta; unchanged |
| `app/r-shiny/shinylive/webr/library.js.metadata` | 9 | Copied allmeta; unchanged |
| `app/r-shiny/shinylive/webr/packages/mathjaxr/mathjaxr_2.0-0.tgz` | 2 | Copied allmeta; unchanged |
| `app/r-shiny/shinylive/webr/packages/metadat/metadat_1.4-0.tgz` | 2 | Copied allmeta; unchanged |
| `app/r-shiny/shinylive/webr/packages/numDeriv/numDeriv_2016.8-1.1.tgz` | 1 | Copied allmeta; unchanged |
| `app/r-shiny/shinylive/webr/vfs/etc/fonts/fonts.conf` | 2 | Copied allmeta; unchanged |
| `app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem` | 149 | Copied allmeta; unchanged |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/doc.data.gz` | 1 | Copied allmeta; unchanged |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/libs.data.gz` | 1 | Copied allmeta; unchanged |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/graphics/help.data.gz` | 1 | Copied allmeta; unchanged |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/methods/help.data.gz` | 1 | Copied allmeta; unchanged |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/parallel.data.gz` | 1 | Copied allmeta; unchanged |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats/help.data.gz` | 1 | Copied allmeta; unchanged |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/translations/DESCRIPTION` | 1 | Copied allmeta; unchanged |
| `app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-Italic.ttf` | 3 | Copied allmeta; unchanged |
| `app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-Regular.ttf` | 3 | Copied allmeta; unchanged |
| `app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSansMono-Regular.ttf` | 1 | Copied allmeta; unchanged |
| `app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSerif-Regular.ttf` | 1 | Copied allmeta; unchanged |
| `app/r-shiny/shinylive/webr/vfs/usr/share/proj.data.gz` | 1 | Copied allmeta; unchanged |
| `app/r-shiny/shinylive/webr/webr-worker.js` | 6 | Copied allmeta; unchanged |
| `app/r-shiny/shinylive/webr/webr.mjs` | 2 | Copied allmeta; unchanged |
| `app/shared/alm-validate.js` | 2 | Copied allmeta; unchanged |
| `app/shared/app-flow.js` | 1 | Copied allmeta; unchanged |
| `app/shared/autosave.js` | 2 | Copied allmeta; unchanged |
| `app/shared/build-info.js` | 1 | Copied allmeta; unchanged |
| `app/shared/citation.js` | 3 | Copied allmeta; unchanged |
| `app/shared/ma-pooled-v1.js` | 1 | Copied allmeta; unchanged |
| `app/shared/ma-studies-v1.js` | 4 | Copied allmeta; unchanged |
| `app/shared/truthcert-export.js` | 2 | Copied allmeta; unchanged |
| `bench/install_r_packages.R` | 1 | Archive-owned; reviewed false positives retained |
| `docs/paper.md` | 5 | Archive-owned; reviewed false positives retained |

## Files scanned with no candidate hits

- `.devcontainer/devcontainer.json`
- `.devcontainer/post-create.sh`
- `.dockerignore`
- `.gitattributes`
- `.github/workflows/devcontainer.yml`
- `.gitignore`
- `.nvmrc`
- `Dockerfile`
- `Makefile`
- `ORIGINAL_VALIDATION_SHA256.json`
- `RECUT_NOTES.md`
- `SOURCE_SHA256.json`
- `STUCK_FAILURES.md`
- `analysis/checks.py`
- `analysis/compare_runs.py`
- `analysis/set_expected.py`
- `app/heterogeneity/index.html`
- `app/heterogeneity/validate/corpus/corpus.json`
- `app/heterogeneity/validate/corpus/reference.json`
- `app/hub/app-style.css`
- `app/hub/shared/a11y-landmarks.js`
- `app/hub/shared/analysis-lifecycle.js`
- `app/hub/shared/axis-controls.js`
- `app/hub/shared/csv-upload.js`
- `app/hub/shared/glossary.ar.json`
- `app/hub/shared/glossary.es.json`
- `app/hub/shared/glossary.json`
- `app/hub/shared/glossary.zh.json`
- `app/hub/shared/plot-export.js`
- `app/hub/shared/reset-undo.js`
- `app/hub/shared/results-export.js`
- `app/hub/shared/tooltips.js`
- `app/hub/shared/url-state.js`
- `app/r-shiny/shinylive/webr/libRblas.so`
- `app/r-shiny/shinylive/webr/libRlapack.so`
- `app/r-shiny/shinylive/webr/packages/Matrix/Matrix_1.7-5.tgz`
- `app/r-shiny/shinylive/webr/packages/lattice/lattice_0.22-9.tgz`
- `app/r-shiny/shinylive/webr/packages/metafor/metafor_4.8-0.tgz`
- `app/r-shiny/shinylive/webr/packages/nlme/nlme_3.1-169.tgz`
- `app/r-shiny/shinylive/webr/packages/pbapply/pbapply_1.7-4.tgz`
- `app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/digest_0.6.39.tgz`
- `app/r-shiny/shinylive/webr/repo/manifest.json`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/doc.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/base/demo.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/base/demo.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/base/help.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/base/help.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/base/html.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/base/html.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/compiler/help.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/compiler/help.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/compiler/html.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/compiler/html.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/datasets/help.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/datasets/help.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/datasets/html.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/datasets/html.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/afm.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/afm.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/demo.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/demo.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/enc.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/enc.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/fonts.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/fonts.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/help.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/help.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/html.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/html.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/libs.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/graphics/demo.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/graphics/demo.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/graphics/help.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/graphics/html.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/graphics/html.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grid/doc.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grid/doc.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grid/help.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grid/help.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grid/html.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grid/html.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/methods/help.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/methods/html.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/methods/html.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/parallel.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/splines/help.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/splines/help.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/splines/html.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/splines/html.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats/demo.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats/demo.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats/doc.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats/doc.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats/help.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats/html.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats/html.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats4/help.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats4/help.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats4/html.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats4/html.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/tcltk.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/tcltk.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/tools/help.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/tools/help.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/tools/html.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/tools/html.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/translations.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/translations.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/utils/doc.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/utils/doc.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/utils/help.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/utils/help.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/utils/html.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/utils/html.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/utils/misc.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/utils/misc.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/webr/help.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/webr/help.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/webr/html.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/webr/html.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/share.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/share.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-Bold.ttf`
- `app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-BoldItalic.ttf`
- `app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSansMono-Bold.ttf`
- `app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSerif-Bold.ttf`
- `app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSerif-BoldItalic.ttf`
- `app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSerif-Italic.ttf`
- `app/r-shiny/shinylive/webr/vfs/usr/share/gdal.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/share/gdal.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/share/proj.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/usr/share/udunits.data.gz`
- `app/r-shiny/shinylive/webr/vfs/usr/share/udunits.js.metadata`
- `app/r-shiny/shinylive/webr/vfs/var/cache/fontconfig/3830d5c3ddfd5cd38a049b759396e72e-le32d8.cache-9`
- `app/r-shiny/shinylive/webr/vfs/var/cache/fontconfig/CACHEDIR.TAG`
- `app/shared/canonical-datasets.js`
- `app/shared/forced-colors.css`
- `app/shared/hero-examples.js`
- `app/shared/heterogeneity-ci.js`
- `app/shared/ma-core.js`
- `app/shared/toast.js`
- `app/shared/truthcert-ui.js`
- `app/shared/webr-runner.js`
- `bench/assemble_corpus.R`
- `bench/build_corpus.py`
- `bench/capture_one.R`
- `bench/reference_metafor.R`
- `bench/run_app.mjs`
- `ci/build_site.py`
- `corpus/corpus.csv`
- `corpus/corpus_log.tsv`
- `corpus/corpus_summary.json`
- `docs/make_numbers.py`
- `docs/numbers.json`
- `docs/references.py`
- `docs/render_references.py`
- `docs/screenshots/captions.md`
- `docs/screenshots/capture.mjs`
- `docs/screenshots/compose.py`
- `docs/screenshots/legibility.json`
- `docs/screenshots/shots_log.json`
- `docs/screenshots/step1.png`
- `docs/screenshots/step2.png`
- `docs/screenshots/step3.png`
- `docs/screenshots/step4.png`
- `docs/screenshots/step5.png`
- `docs/screenshots/step6.png`
- `expected/paper_values.json`
- `expected/quick_values.json`
- `index.html`
- `package-lock.json`
- `package.json`
- `provenance/publication-scan.csv`
- `provenance/publication-scan.md`
- `provenance/run_plan-2026-10-22-release.log`
- `reproduce.py`
- `requirements.txt`
- `scripts/check_reference.R`
- `scripts/recut.py`
- `tests/test_recut.py`
- `validation-plus/README.md`

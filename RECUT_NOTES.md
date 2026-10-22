# v1.1.0 recut and finalization notes

Release date **2026-10-22**. **Final release run passed (RUN_EXIT 0).**
The preparation history below is retained; the Finalize section records the
completed runner evidence and publication checks.
Task sources: ../TASK.md and ../APP.txt. Work is confined to this task folder;
archive/.git and allmeta source files were not modified. No Git, Node or R release
command was run after reading the environment restriction. The baseline for the
change inventory is the archive's on-disk state before edits; Git status/tag
comparison could not run in this sandbox.

## How this archive is built and verified

The v1.0.0 archive contains no validate.R and had no integrity manifest or manifest
regenerator. Its original entry point is reproduce.py. It checks versions, copies
the committed corpus to results/quick or results/full, runs
bench/reference_metafor.R for metafor references, drives the actual page in
Chromium through bench/run_app.mjs, and invokes analysis/make_outputs.py.
The latter imports analysis/checks.py (typed REL/ABS 1e-9, structural exact),
creates tables/figures/stats, and compares against expected/quick_values.json
or expected/paper_values.json. analysis/compare_runs.py compares separate platform
outputs; no multi-platform run is claimed here. analysis/set_expected.py exists
but is intentionally not run: it would overwrite the protected expectations.

bench/build_corpus.py, capture_one.R and assemble_corpus.R build the corpus from
metadat examples. The recut instead keeps corpus/ byte-identical.
The historical R reference source is bench/reference_metafor.R; reference.jsonl
is generated at runtime, not committed in the original archive. Historical paper,
numbers and screenshots under docs/ are retained unchanged and labelled as such.

RUN_PLAN.cmd runs original quick and full modes and prints N/N from newly generated
stats.json files. Before either mode, scripts/recut.py preserve renames existing
results and outputs to <mode>.prev-N; .gitignore and the file manifest exclude
every *.prev-* folder. No old output is deleted by this preparation.
--allow-version-mismatch permits the coordinator's alternate Playwright environment,
but scripts/check_reference.R independently requires desktop R 4.6.0,
metafor 5.2-1 and metadat 1.6-0. Actual environment mismatches must stay visible.

The new SOURCE_SHA256.json covers published files, including validation code and
app assets. scripts/recut.py manifest --write regenerates it only after protected
original hashes and upstream corpus/package pins verify. The manifest omits itself,
generated outputs/results, dependency installs, caches and PROGRESS.md.
ORIGINAL_VALIDATION_SHA256.json preserves the initial raw-byte anchors and is
never regenerated from current validation inputs.

## App identity and dependency coverage

The former identity was allmeta commit
7cb5975429531791d1879e80cf5c05f765e82c21 (PR #82), recorded in README/CHANGELOG.
The current source is allmeta **v1.8.0**, commit
**1cb3f8409c7af75ed41f7e1811f9c502f900fc79**, supplied in TASK.md and confirmed
by the source checkout HEAD. Source CITATION.cff also says v1.8.0 (2026-10-20).
The release DOI **10.5281/zenodo.23515177** and concept DOI
**10.5281/zenodo.20516880** are the task's supplied identifiers; the concept DOI
also appears in source CITATION.cff. Remote DOI resolution was not a release
verification step in this preparation.

Every previously archived app path was copied from the same path in allmeta.
The page's script/src and link/href references were parsed; shared scripts were
inspected recursively for import, fetch, script-relative new URL and dynamic
loader paths. This includes:
- Page scripts/styles, the plot-export PDF vendor, and the analysis lifecycle helper.
- Tooltips opts.src plus its English/Arabic/Spanish/Chinese glossary variants.
- The validation adapter, unchanged MANIFEST.json, and both fetched corpus files.
- alm-validate.js -> webr-runner.js -> the local webR module/worker/R runtime,
  its complete VFS, unchanged package manifest, and the nine-package metafor
  dependency closure. Other apps' packages, development typings/tests, source maps
  and the R.js backup are not needed by this page and are not copied.

The dependency inventory contains **161 files / 79,692,361 bytes**: 23 previously
archived files (10 changed, 13 unchanged), plus 138 added files; none removed.
APP_SOURCE_FILES.json records each source path and dependency reason.
Click-through navigation to sibling allmeta apps (for example the separate
webr-validator app) is outside this snapshot; those pages are not in-page
script/import/fetch dependencies.

The copied build-info.js reports v1.8.0 with its upstream build-time SHA
42a94da2110a02200d0b5bff4c56f636b9cbffa9, rather than the final release commit.
It remains byte-identical to upstream. APP_SOURCE_FILES.json and release metadata
record the final source commit; the build-time SHA is not used as the recut pin.

## Original scope and extras

Full expectations: 88 meta-analyses / 704 configurations, 28 DL refusals,
676 compared configurations, **131,781 numerical checks**, **120,720 original
display checks**, and **44 paper expectations**. Quick expectations:
3 meta-analyses, **4,934 numerical**, **4,480 display**, **11 paper expectations**.
The final release run met these unchanged expectations (see Finalize below).
Numerical and display denominators were
independently re-derived from the protected corpus with the original formulas.

v1.8.0 renames the HK and PI cards and splits I2 into Q-based and model-based cards.
The runner follows those labels, checking the same Q-based point and both original
model-based interval endpoints. It does not add the new model-based point to the
original audit. The upstream adapter checks that additional point and therefore
has a separate expected 121,424 display checks (120,720 + 704); that total is not
substituted into the preserved expectations.

APP.txt explicitly says: extras = none numerical; PR #163 usability (strict
numeric input; no number changes). A recursive search of the app's validate/
directory found no plus or divergences files. validation-plus/README.md records
not applicable; no plus corpus, output or N/N is invented.

The optional live webR uses metafor **4.8-0** and metadat **1.4-0**, according to
the copied package manifest; these are not the original desktop reference
versions. Its package byte hashes are verified, but no live webR execution or
complete in-page validation-widget run is claimed here.

## Protected corpus line-ending exception

Original corpus/corpus.csv stays **236,003 bytes**, with 2,242 CRLF line endings.
Its raw SHA-256 is:
8575cbb61532ed0ddfe2afc2f4699ad03505d56bc91bbba6ff10e5dbb68c5223

Copied app/heterogeneity/validate/MANIFEST.json source_files/corpus.csv refers to:
2f36c0d144fc649a68c88359eff8eb7134769096e6b60af44aaf84743725cd9a

Replacing CRLF with LF in memory only gives exactly the latter hash. Neither
the original CSV nor the copied upstream manifest was edited. The strict
scripts/recut.py source-corpus diagnostic retains its raw-byte comparison and
exits 1 for this known exception; it is not counted as a pass. It is separate
from the release file-integrity checks: the original raw-byte anchor verifies,
and the two copied app corpus files verify against their own upstream hashes.
The upstream source_files/reference.jsonl pin describes a historical external
artifact; no matching committed file exists in this original archive.

## Preparation verification (historical)

- 161/161 copied app files match the supplied upstream working-tree bytes.
- 30/30 protected originals match their pre-edit SHA-256 anchors.
- 2/2 copied app corpus files and 9/9 required webR package archives match the
  original upstream manifests' raw hashes and sizes.
- Python helper tests: **7 passed**. The first attempt hit the Windows sandbox
  ACL behavior of tempfile's 0700 directories; the test fixtures now inherit
  workspace ACLs. The second attempt passed all seven. No app data was used as
  a synthetic test result.
- Python syntax, JSON/metadata, source identity, release date, original count
  derivations, current card lookups, and machine-independent run-plan paths
  are checked locally. Final file-manifest verification: **223/223 SHA-256
  checks passed** after regeneration; this is file integrity, not a runtime result.
- Critical local imports: numpy imports; matplotlib fails to import
  _c_internal_utils because a DLL initialization routine fails. Recorded in
  STUCK_FAILURES.md. The human run plan checks both imports before reproduction;
  no dependency repair or full numerical run was attempted in this sandbox.
- At preparation time, the original numerical/browser suite and R/Node checks
  had been deferred to the human runner. The final release log now records their
  successful completion. Optional live webR execution remains outside that run.

Initial shell attempts failed before commands started; after TASK.md was read,
file work used Python. All archive creators/authors remain unchanged. No portfolio
status or submission state is promoted, so INDEX.md and the workbook are not edited.

## Static versus dynamic disclosure

| Item | Static or dynamic | Evidence / validation |
|---|---|---|
| Release version/date and source identifiers | Static release metadata | TASK_finalize2.md; TASK.md; source HEAD/CITATION.cff |
| Original numerical expectations/tolerances | Static protected baseline | Original expected/, corpus/, reference R and analysis files; SHA-256 anchors |
| App files, references and runtime assets | Copied dynamically from source files | Byte equality; source manifests and APP_SOURCE_FILES.json |
| Manifest file hashes | Computed dynamically | Python hashlib over on-disk bytes |
| Runtime numerical/display N/N | Dynamic, measured | Final run_plan.log; cross-checked against outputs/*/stats.json and reproduction reports |
| Extra numerical suite | Not applicable | APP.txt plus source-directory inspection |

## Remaining archive identifier

The archive v1.1.0 DOI awaits assignment; no identifier is invented. The old
archive DOI 10.5281/zenodo.23415772 remains labelled v1.0.0. Release results and
actual runner versions have been filled from the final log. Historical paper
author fields remain unchanged under the original-file protection contract.
No cross-platform or shipped/certified claim is made.

Local preparation helpers and the initial baseline inventory live one directory
above archive/; they are not published archive contents. The initial ACL failure
left empty _recut_test_* scratch directories outside archive/ that the sandbox
could not clean; they are not in the manifest or release tree.

## Finalize (2026-10-22)

Only ../run_plan.log is release-run evidence; prior attempts are excluded.
The runner exit record is RUN_EXIT 0 and the log ends with successful completion.
The publication copy is [the final release log](provenance/run_plan-2026-10-22-release.log).
Its source SHA-256 is d4ed5de9ca5066b5d6dfd9e48647194d3932fce5396726d08b5b8b415d0895e4. The supplied log contains no local machine
paths or account identifiers requiring removal, so the publication copy is
byte-identical. Future copies must redact local machine identity before publication.

| Run | Numerical checks | Display checks | Expected values |
|---|---:|---:|---:|
| Quick | 4934/4934 | 4480/4480 | 11/11 |
| Full | 131781/131781 | 120720/120720 | 44/44 |

Both display-failure counts are 0. Expected-count differences: **none**.
The full run records 88 meta-analyses, 704 configurations, 28 DL refusals and
676 compared configurations. The quick and full reports contain 11/11 and
44/44 numbers reproduced: ALL PASS. These results were checked against the
on-disk stats and reports. No corpus, expected value, tolerance, or upstream
app byte was changed. Extras: NOT APPLICABLE (no numerical plus suite).

R 4.6.0 (metafor 5.2.1, metadat 1.6.0), Node 24.16.0 (Playwright 1.59.1), Python 3.13.13, Windows AMD64; Chromium 148.0.7778.96.

The plan used --allow-version-mismatch. The log reports these exact deviations:

~~~text
WARNING: version mismatch: node 24.16.0 (pinned 24.15.0); playwright 1.59.1 (pinned 1.63.0); contourpy 1.3.3 (pinned 1.4.0); fonttools 4.63.0 (pinned 4.66.1); kiwisolver 1.5.0 (pinned 1.5.1); numpy 2.4.6 (pinned 2.4.4); packaging 26.2 (pinned 26.3); pillow 12.2.0 (pinned 12.3.0); pyparsing 3.3.2 (pinned 3.3.3)
~~~

Desktop R 4.6.0, metafor 5.2.1 and metadat 1.6.0 were enforced separately.
The result is for this Windows runner; canonical Docker, cross-platform,
optional live webR and the complete in-page widget are not newly validated.

The publication scan and every candidate hit/action are recorded in
[publication-scan.md](provenance/publication-scan.md) and
[publication-scan.csv](provenance/publication-scan.csv). Copied allmeta files
are listed there without alteration. Public attribution, source links,
technical identifiers and generic prose are distinguished from local identity.
No local machine paths, private account names, personal email addresses or
credential values were found in archive-owned publication files.
Previous-output and temporary directories are excluded by .gitignore;
the publication inventory was checked against those rules.

Finalization changed the release metadata and result prose in README.md,
RECUT_NOTES.md, CHANGELOG.md, CITATION.cff, .zenodo.json and RUN_PLAN_EXPECTED.md;
annotated the resolved runner status in STUCK_FAILURES.md; hardened temporary
folder exclusions in .gitignore and scripts/recut.py, with matching coverage
in tests/test_recut.py; added the release log
and scan reports under provenance/; and regenerated SOURCE_SHA256.json.
ORIGINAL_VALIDATION_SHA256.json remains an immutable anchor; upstream
manifests are not regenerated.

Final Python verification (run from the archive root):

~~~text
python -X utf8 scripts/recut.py manifest --write --upstream ../allmeta
MANIFEST WRITTEN: 226 files

python -X utf8 scripts/recut.py manifest --upstream ../allmeta
PROTECTED ORIGINALS: 30/30 byte-identical
UPSTREAM APP BYTES: 161/161 identical
APP CORPUS PINS: 2/2
WEBR PACKAGE PINS: 9/9
MANIFEST: 226/226 SHA-256 checks passed
~~~

Python helper suite: 7 tests passed (OK), including exclusion of temporary and
previous-output folders. Publication scan: 227 files, 621 candidate hits in
46 files, all listed with actions; no archive-owned sensitive hits.
The final manifest has 226 entries versus 223 in the original release log:
the difference is exactly the three added provenance files (release log,
scan report and candidate CSV). The manifest excludes itself, explaining
227 files scanned versus 226 files hashed. This is a publication inventory
change, not a changed numerical or display expectation.
After inserting this verifier transcript, the manifest was regenerated and
verified again so the final notes and audit reports are included.

## Added and changed archive files

The table below lists every added/changed published file relative to the
pre-edit snapshot. **Removed files: none.** Unchanged app files are also
enumerated in APP_SOURCE_FILES.json; protected originals are enumerated in
ORIGINAL_VALIDATION_SHA256.json.

| Path | Status | Why |
|---|---|---|
| `.gitignore` | changed | Ignore PROGRESS.md and every preserved *.prev-* output folder. |
| `.zenodo.json` | changed | Version 1.1.0, measured release-run description, retained prior identifiers plus prior archive and allmeta v1.8.0 DOI relationships; creators unchanged. |
| `APP_SOURCE_FILES.json` | added | Source release identity, exhaustive copied file inventory, changes and dependency reasons. |
| `CHANGELOG.md` | changed | v1.1.0 entry; preserve earlier history with historical labels. |
| `CITATION.cff` | changed | Version/date and allmeta release reference; retain prior archive DOI as explicitly v1.0.0, remove misleading top-level DOI for the new version; authors unchanged. |
| `ORIGINAL_VALIDATION_SHA256.json` | added | Raw-byte anchors for 30 pre-recut original validation and paper artifacts. |
| `README.md` | changed | New v1.1.0 scope, measured results, run instructions and historical-results/citation distinction. |
| `RECUT_NOTES.md` | added | Build/review record, integrity exception, coverage, final results and exhaustive changed-file list. |
| `RUN_PLAN.cmd` | added | Portable fail-closed Windows command sequence for original quick/full validation, applicability and hashes. |
| `RUN_PLAN_EXPECTED.md` | added | Expected outcomes, runtime variables, original denominators and second-pass procedure. |
| `SOURCE_SHA256.json` | added | Deterministic published-file inventory; regenerated by Python, excludes itself and generated/local-only content. |
| `STUCK_FAILURES.md` | added | Record sandbox runtime blockers, including the Matplotlib DLL import failure; no app numerical failure is inferred. |
| `app/heterogeneity/index.html` | changed | existing archived app file |
| `app/heterogeneity/validate/MANIFEST.json` | added | unchanged upstream corpus hash contract |
| `app/heterogeneity/validate/adapter.js` | added | page script |
| `app/heterogeneity/validate/corpus/corpus.json` | added | adapter corpus fetch via AlmValidate |
| `app/heterogeneity/validate/corpus/reference.json` | added | adapter corpus fetch via AlmValidate |
| `app/hub/app-style.css` | changed | existing archived app file; page link |
| `app/hub/shared/analysis-lifecycle.js` | added | page script |
| `app/hub/shared/csv-upload.js` | changed | existing archived app file; page script |
| `app/hub/shared/glossary.ar.json` | added | tooltips opts.src and language variants |
| `app/hub/shared/glossary.es.json` | added | tooltips opts.src and language variants |
| `app/hub/shared/glossary.json` | added | tooltips opts.src and language variants |
| `app/hub/shared/glossary.zh.json` | added | tooltips opts.src and language variants |
| `app/hub/shared/plot-export.js` | added | page script |
| `app/hub/shared/results-export.js` | changed | existing archived app file; page script |
| `app/hub/shared/url-state.js` | changed | existing archived app file; page script |
| `app/hub/shared/vendor/jspdf.min.js` | added | script-relative URL in hub/shared/plot-export.js |
| `app/r-shiny/shinylive/webr/R.js` | added | lazy webR runtime |
| `app/r-shiny/shinylive/webr/R.wasm` | added | lazy webR runtime |
| `app/r-shiny/shinylive/webr/libRblas.so` | added | lazy webR runtime |
| `app/r-shiny/shinylive/webr/libRlapack.so` | added | lazy webR runtime |
| `app/r-shiny/shinylive/webr/library.data.gz` | added | lazy webR runtime |
| `app/r-shiny/shinylive/webr/library.js.metadata` | added | lazy webR runtime |
| `app/r-shiny/shinylive/webr/packages/Matrix/Matrix_1.7-5.tgz` | added | live metafor dependency Matrix |
| `app/r-shiny/shinylive/webr/packages/lattice/lattice_0.22-9.tgz` | added | live metafor dependency lattice |
| `app/r-shiny/shinylive/webr/packages/mathjaxr/mathjaxr_2.0-0.tgz` | added | live metafor dependency mathjaxr |
| `app/r-shiny/shinylive/webr/packages/metadat/metadat_1.4-0.tgz` | added | live metafor dependency metadat |
| `app/r-shiny/shinylive/webr/packages/metafor/metafor_4.8-0.tgz` | added | live metafor dependency metafor |
| `app/r-shiny/shinylive/webr/packages/nlme/nlme_3.1-169.tgz` | added | live metafor dependency nlme |
| `app/r-shiny/shinylive/webr/packages/numDeriv/numDeriv_2016.8-1.1.tgz` | added | live metafor dependency numDeriv |
| `app/r-shiny/shinylive/webr/packages/pbapply/pbapply_1.7-4.tgz` | added | live metafor dependency pbapply |
| `app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/digest_0.6.39.tgz` | added | live metafor dependency digest |
| `app/r-shiny/shinylive/webr/repo/manifest.json` | added | webR package manifest (copied intact) |
| `app/r-shiny/shinylive/webr/vfs/etc/fonts/fonts.conf` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/doc.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/doc.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/base/demo.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/base/demo.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/base/help.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/base/help.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/base/html.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/base/html.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/compiler/help.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/compiler/help.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/compiler/html.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/compiler/html.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/datasets/help.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/datasets/help.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/datasets/html.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/datasets/html.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/afm.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/afm.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/demo.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/demo.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/enc.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/enc.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/fonts.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/fonts.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/help.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/help.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/html.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/html.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/libs.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/libs.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/graphics/demo.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/graphics/demo.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/graphics/help.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/graphics/help.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/graphics/html.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/graphics/html.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grid/doc.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grid/doc.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grid/help.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grid/help.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grid/html.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grid/html.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/methods/help.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/methods/help.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/methods/html.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/methods/html.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/parallel.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/parallel.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/splines/help.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/splines/help.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/splines/html.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/splines/html.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats/demo.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats/demo.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats/doc.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats/doc.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats/help.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats/help.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats/html.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats/html.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats4/help.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats4/help.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats4/html.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats4/html.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/tcltk.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/tcltk.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/tools/help.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/tools/help.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/tools/html.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/tools/html.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/translations.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/translations.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/translations/DESCRIPTION` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/utils/doc.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/utils/doc.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/utils/help.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/utils/help.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/utils/html.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/utils/html.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/utils/misc.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/utils/misc.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/webr/help.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/webr/help.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/webr/html.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/webr/html.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/share.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/share.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-Bold.ttf` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-BoldItalic.ttf` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-Italic.ttf` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-Regular.ttf` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSansMono-Bold.ttf` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSansMono-Regular.ttf` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSerif-Bold.ttf` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSerif-BoldItalic.ttf` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSerif-Italic.ttf` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSerif-Regular.ttf` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/share/gdal.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/share/gdal.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/share/proj.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/share/proj.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/share/udunits.data.gz` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/usr/share/udunits.js.metadata` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/var/cache/fontconfig/3830d5c3ddfd5cd38a049b759396e72e-le32d8.cache-9` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/vfs/var/cache/fontconfig/CACHEDIR.TAG` | added | webR virtual filesystem and lazy data |
| `app/r-shiny/shinylive/webr/webr-worker.js` | added | lazy webR runtime |
| `app/r-shiny/shinylive/webr/webr.mjs` | added | lazy webR runtime |
| `app/shared/alm-validate.js` | added | page script |
| `app/shared/build-info.js` | changed | existing archived app file; page script |
| `app/shared/canonical-datasets.js` | changed | existing archived app file; page script |
| `app/shared/forced-colors.css` | changed | existing archived app file; page link |
| `app/shared/hero-examples.js` | changed | existing archived app file; page script |
| `app/shared/ma-core.js` | changed | existing archived app file; page script |
| `app/shared/webr-runner.js` | added | script-relative URL in shared/alm-validate.js |
| `bench/run_app.mjs` | changed | Use the same optional Playwright directory; adapt I2/HK/PI display lookups without changing original quantities, counts or tolerances. |
| `reproduce.py` | changed | Allow PLAYWRIGHT_MODULE package directory for version discovery; default pinned local package unchanged. |
| `scripts/check_reference.R` | added | Enforce original desktop R/metafor/metadat versions before the runtime-mismatch-permitted reproduction. |
| `scripts/recut.py` | added | Verify hashes and upstream pins; preserve prior output folders; preflight; print measured output counts; keep strict cross-source corpus diagnostic. |
| `tests/test_recut.py` | added | Seven filesystem tests for tampering, missing/empty manifests, traversal, ignored output trees and collision-safe output preservation. |
| `validation-plus/README.md` | added | Record absence of a numerical extras suite and distinguish optional webR from desktop reference validation. |

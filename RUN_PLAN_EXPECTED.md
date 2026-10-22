# v1.1.0 runner contract and expected outcomes

**Release date: 2026-10-22. Final release run passed (RUN_EXIT 0).**
Run RUN_PLAN.cmd with Windows cmd from this archive's root. The observed
results below come from the [final release log](provenance/run_plan-2026-10-22-release.log),
with the original expected outcomes retained unchanged.

| Run | Numerical checks | Display checks | Expected values |
|---|---:|---:|---:|
| Quick | 4934/4934 | 4480/4480 | 11/11 |
| Full | 131781/131781 | 120720/120720 | 44/44 |

No expected count differs from the log. Display failures: 0 in both modes.
The helper suite passed 7 tests; the release-run manifest passed 223/223
checks before and after execution. Protected originals: 30/30; app corpus
pins: 2/2; webR package pins: 9/9. Extras: NOT APPLICABLE.

R 4.6.0 (metafor 5.2.1, metadat 1.6.0), Node 24.16.0 (Playwright 1.59.1), Python 3.13.13, Windows AMD64; Chromium 148.0.7778.96.

~~~text
WARNING: version mismatch: node 24.16.0 (pinned 24.15.0); playwright 1.59.1 (pinned 1.63.0); contourpy 1.3.3 (pinned 1.4.0); fonttools 4.63.0 (pinned 4.66.1); kiwisolver 1.5.0 (pinned 1.5.1); numpy 2.4.6 (pinned 2.4.4); packaging 26.2 (pinned 26.3); pillow 12.2.0 (pinned 12.3.0); pyparsing 3.3.2 (pinned 3.3.3)
~~~

## Environment

| Variable or dependency | Contract |
|---|---|
| R_BIN | Optional inherited directory containing Rscript; prepended to PATH if defined. No installation path is embedded. |
| PATH | Inherited, with optional R_BIN prefix; must resolve Python, Node and Rscript. |
| R_HOME | Optional inherited R installation root; never overwritten. It must agree with R_BIN when supplied. |
| R_LIBS_USER, R_LIBS | Inherited R library search paths; never overwritten. Required desktop packages: metafor 5.2-1 and metadat 1.6-0. |
| R_ENVIRON_USER | Set to NUL, following the non-path-specific runner setting in RENV.txt. |
| PYTHONUTF8 | Set to 1 so Python logs and subprocess I/O use UTF-8 on Windows. |
| PLAYWRIGHT_MODULE | Optional inherited path to the Playwright package directory containing package.json and index.mjs. Without it, use the archive's node_modules/playwright from npm ci. Both reproduce.py and the browser runner use the same directory. |
| PLAYWRIGHT_BROWSERS_PATH | Optional Playwright browser cache location, inherited unchanged. Install the browser matching the selected Playwright package before running. |
| APP_CHROME_CHANNEL | Optional existing runner setting for a browser channel such as chrome or msedge. Without it, use Playwright's Chromium. Any alternate channel must be disclosed in the run log. |
| OMP_NUM_THREADS, OPENBLAS_NUM_THREADS, MKL_NUM_THREADS | reproduce.py sets these to 1 for the R and Node subprocesses, as in v1.0.0. |
| Python packages | Install requirements.txt for the canonical pins; numpy and matplotlib must import. |
| R / Node / Playwright | Canonical pins remain R 4.6.0 / Node 24.15.0 / Playwright 1.63.0. RENV.txt indicates alternate Playwright 1.59.1 on the coordinator's runner. |

The plan explicitly uses --allow-version-mismatch to permit the coordinator's
alternate Playwright/Python/Node environment, logging every mismatch through the
existing version checker. A separate check_reference.R step still **requires**
R 4.6.0, metafor 5.2-1 and metadat 1.6-0. An alternate-runtime pass must be labelled
with the actual versions; it is not a canonical Docker or cross-platform pass.
RENV.txt supplies machine-specific values for the human runner only; none are
copied into published files. Creators and numerical tolerances are unchanged.

## Expected outcomes, in RUN_PLAN.cmd order

| Label / command | Expected outcome |
|---|---|
| Use inherited R location | Optional R_BIN prepended to PATH. |
| Disable personal R environ file | R_ENVIRON_USER=NUL. |
| Use UTF-8 Python I/O | PYTHONUTF8=1. |
| Verify manifests before running: python scripts/recut.py manifest | All entries in SOURCE_SHA256.json verify; 30/30 protected originals, 2/2 copied corpus pins, and 9/9 copied webR package pins verify. File denominator is the manifest's files count. |
| Test helpers: python -m unittest discover -s tests -v | 7/7 filesystem contract tests pass; these are not numerical app checks. |
| Preflight: python scripts/recut.py preflight | Python imports and runner syntax work; Rscript/node paths and selected Playwright package exist; actual versions are logged. |
| Reference versions: Rscript scripts/check_reference.R | 2/2 package pins; R 4.6.0, metafor 5.2.1, metadat 1.6.0 (R's dotted version spelling). |
| Preserve quick: python scripts/recut.py preserve quick | Existing results/quick and outputs/quick renamed to quick.prev-N using the next free positive integer; otherwise explicitly absent. |
| Original quick: python reproduce.py --quick --allow-version-mismatch | R reference plus browser computation/rendering plus original expected-value comparison. Exit 0; 3 meta-analyses, 4,934 numerical checks, 11/11 numbers reproduced: ALL PASS. |
| Measured quick counts: python scripts/recut.py counts quick | QUICK NUMERICAL: 4934/4934; QUICK DISPLAY: 4480/4480; QUICK EXPECTED VALUES: 11/11. Counts are read from newly generated outputs/quick/stats.json, not printed constants. |
| Preserve full: python scripts/recut.py preserve full | Existing results/full and outputs/full renamed to full.prev-N; otherwise explicitly absent. |
| Original full: python reproduce.py --allow-version-mismatch | R reference plus browser computation/rendering plus unchanged paper expectations. Exit 0; 88 meta-analyses, 704 configurations, 28 refused and 676 compared; 44/44 numbers reproduced: ALL PASS. |
| Measured full counts: python scripts/recut.py counts full | FULL NUMERICAL: 131781/131781; FULL DISPLAY: 120720/120720; FULL EXPECTED VALUES: 44/44. No failures. |
| Extras applicability: python scripts/recut.py extras | EXTRAS: NOT APPLICABLE (no numerical plus suite; APP.txt PR #163). No plus N/N exists. |
| Verify manifests after running: python scripts/recut.py manifest | Same file-integrity denominators as before; generated results, outputs and *.prev-* folders are excluded. |
| Completion | Exit 0 only after every required step succeeds. An earlier failure stops the plan. |

Full targets are read from unchanged expected/paper_values.json; quick numerical
and paper targets from expected/quick_values.json. The original display formula
is 8 × (19 + 6k − 1[k < 10]) per meta-analysis, evaluated on the preserved corpus:
4,480 quick and 120,720 full. Expected-value files contain 11 and 44 entries.
The v1.8.0 in-page adapter has a separate model-based I² point check; its display
denominator is 121,424, outside the original 120,720-check scope. It is not a plus
suite and is not used to inflate the archive's expected count.

## Integrity exception and second pass

The strict cross-source diagnostic, python scripts/recut.py source-corpus,
**exits 1**: the protected original corpus has CRLF bytes while the copied
upstream manifest's source_files/corpus.csv pin identifies LF bytes. This check
is retained without changing its comparison; it is not reported as passing.
RECUT_NOTES.md records both hashes and the read-only normalization proof.
The release plan checks the original file against its preserved raw-byte anchor
and the copied corpus/reference files against their own upstream pins. The
upstream source reference.jsonl pin has no committed matching file here; newly
generated R output is compared numerically by the original analysis, not claimed
to be a byte-identical copy of the historical source.

Finalization checked ../run_plan.log against both output reports and stats files.
The measured counts and actual runtime versions above are from that final run.
Do not use analysis/set_expected.py or rebuild/change the protected corpus to
force agreement. After intentional documentation edits, run
python scripts/recut.py manifest --write and then manifest again.
The finalization integrity result is recorded in RECUT_NOTES.md; its file
denominator includes the added provenance and audit files.
All *.prev-* folders are ignored and must stay out of the published tree.

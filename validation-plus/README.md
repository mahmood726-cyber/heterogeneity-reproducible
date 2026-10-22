# Heterogeneity extras scope

No numerical extras suite applies to this recut. The coordinator's APP.txt identifies
PR #163 as strict numeric input usability, with no numerical change and no stated
plus count. The v1.8.0 heterogeneity/validate directory contains adapter.js,
MANIFEST.json, and corpus/reference JSON files, but no *plus* files or plus-corpus.

Expected extras count: **not applicable** (no numerical extras; not a 0/0 pass).
There is no plus-count placeholder because there is no plus suite to execute.
The original validation against desktop R metafor **5.2-1**, using metadat **1.6-0**,
remains the release gate; run RUN_PLAN.cmd from the archive root. Its extras
stage prints: EXTRAS: NOT APPLICABLE (no numerical plus suite; APP.txt PR #163).

The copied app's validation widget is an app dependency, not a new plus suite.
Its stored-reference replay is under app/heterogeneity/validate/. Its optional
live webR runtime ships metafor **4.8-0** and metadat **1.4-0**, as recorded in
app/r-shiny/shinylive/webr/repo/manifest.json; it does not replace the desktop R
reference. Browser and desktop release runs are pending.

#!/usr/bin/env bash
# Runs once when the Codespace (or local dev container) is created: the pinned environment is already
# installed by the Dockerfile, so this goes straight to the quick reproduction and prints the result.
set -uo pipefail
cd "$(dirname "$0")/.."
# The image installs Playwright in /work/node_modules; the workspace is mounted elsewhere, so link it in.
if [ ! -e node_modules ] && [ -d /work/node_modules ]; then ln -s /work/node_modules node_modules; fi
echo
echo "== heterogeneity-reproducible: quick reproduction (3 meta-analyses, about a minute) =="
python reproduce.py --quick
rc=$?
echo
if [ $rc -eq 0 ]; then echo "QUICK RUN: ALL PASS  (report: outputs/quick/reproduction_report.md)"; else echo "QUICK RUN FAILED (exit $rc); see the output above and outputs/quick/reproduction_report.md"; fi
cat <<'EOF'

Next:
  python reproduce.py            # full run: every number in the paper (about 10 minutes)
  results land in outputs/full/  (reproduction_report.md = expected vs reproduced, PASS/FAIL per number)
  the app itself: open app/heterogeneity/index.html (or the live app linked in README.md)
EOF
exit $rc

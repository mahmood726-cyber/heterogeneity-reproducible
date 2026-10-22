@echo off
setlocal EnableExtensions DisableDelayedExpansion
echo === Use inherited R location
if defined R_BIN set "PATH=%R_BIN%;%PATH%"
echo === Disable personal R environ file
set "R_ENVIRON_USER=NUL"
echo === Use UTF-8 Python I/O
set "PYTHONUTF8=1"
echo === Verify archive and protected original manifests before running
python scripts/recut.py manifest || exit /b 1
echo === Test integrity and output-preservation helpers
python -m unittest discover -s tests -v || exit /b 1
echo === Preflight executable paths, Python imports and Playwright package
python scripts/recut.py preflight || exit /b 1
echo === Enforce original desktop R and package versions
Rscript scripts/check_reference.R || exit /b 1
echo === Preserve previous quick outputs
python scripts/recut.py preserve quick || exit /b 1
echo === Original quick validation on v1.8.0 app
python reproduce.py --quick --allow-version-mismatch || exit /b 1
echo === Print measured quick N/N
python scripts/recut.py counts quick || exit /b 1
echo === Preserve previous full outputs
python scripts/recut.py preserve full || exit /b 1
echo === Original full validation on v1.8.0 app
python reproduce.py --allow-version-mismatch || exit /b 1
echo === Print measured full N/N
python scripts/recut.py counts full || exit /b 1
echo === Extras applicability
python scripts/recut.py extras || exit /b 1
echo === Verify archive and protected original manifests after running
python scripts/recut.py manifest || exit /b 1
echo === Run plan completed successfully
exit /b 0

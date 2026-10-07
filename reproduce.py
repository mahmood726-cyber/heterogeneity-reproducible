#!/usr/bin/env python3
"""Re-run the heterogeneity validation and check every number in the paper.

  python reproduce.py                    # full run: every meta-analysis in the corpus, 8 tau^2 estimators (about 10 minutes)
  python reproduce.py --quick            # 3 meta-analyses, about a minute
  python reproduce.py --rebuild-corpus   # first regenerate the corpus from metadat's examples (about half an hour) and
                                         # stop unless it is identical to the committed corpus/corpus.csv

Steps: check tool versions -> corpus (committed copy of every intercept-only rma() fit in the examples of R package
metadat; see bench/build_corpus.py) -> metafor reference analyses (R) -> the app itself in headless Chromium (Node,
Playwright) on the same data -> tables, figures, statistics -> expected vs reproduced, PASS/FAIL per number.
Exit code 0 only if all pass.
"""
import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
R_PINS = {"metafor": "5.2.1", "metadat": "1.6.0"}
PLAYWRIGHT = "1.63.0"
QUICK = ["dat.bcg#1", "dat.begg1989#1", "dat.crede2010#1"]


def sh(cmd, **kw):
    p = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, **kw)
    if p.returncode:
        sys.exit(f"command failed ({p.returncode}): {' '.join(map(str, cmd))}\n{p.stdout}\n{p.stderr}")
    return p.stdout


def check_versions(strict):
    problems = []
    rscript = shutil.which("Rscript") or sys.exit("Rscript not found on PATH (R 4.6.0 needed; see README or use Docker)")
    node = shutil.which("node") or sys.exit("node not found on PATH (Node 24.15.0 needed)")
    pk = ",".join(f"'{p}'" for p in R_PINS)
    rv = sh([rscript, "-e", f"cat(as.character(getRversion()), sapply(c({pk}), function(p) tryCatch(as.character(packageVersion(p)), error=function(e) 'missing')))"]).split()
    nv = sh([node, "--version"]).strip().lstrip("v")
    if rv[0] != "4.6.0": problems.append(f"R {rv[0]} (pinned 4.6.0)")
    for (p, want), got in zip(R_PINS.items(), rv[1:]):
        if got == "missing": sys.exit(f"R package {p} missing: run  Rscript bench/install_r_packages.R")
        if got != want: problems.append(f"{p} {got} (pinned {want})")
    want_node = (ROOT / ".nvmrc").read_text().strip()
    if nv != want_node: problems.append(f"node {nv} (pinned {want_node})")
    pw = ROOT / "node_modules" / "playwright" / "package.json"
    if not pw.exists(): sys.exit("Playwright missing: run  npm ci  and  npx playwright install chromium")
    pwv = json.loads(pw.read_text())["version"]
    if pwv != PLAYWRIGHT: problems.append(f"playwright {pwv} (pinned {PLAYWRIGHT})")
    from importlib.metadata import version
    for line in (ROOT / "requirements.txt").read_text().splitlines():
        line = line.split("#")[0].split(";")[0].strip()
        if "==" in line:
            k, v = line.split("==", 1)
            try:
                if version(k) != v: problems.append(f"{k} {version(k)} (pinned {v})")
            except Exception:
                sys.exit(f"python package {k} missing: run  python -m pip install -r requirements.txt")
    print(f"environment: R {rv[0]} (metafor {rv[1]}, metadat {rv[2]}), Node {nv} (Playwright {pwv}), Python {platform.python_version()}, "
          f"{platform.system()} {platform.machine()}")
    if problems:
        msg = "version mismatch: " + "; ".join(problems)
        if strict: sys.exit(msg + "\n(use --allow-version-mismatch to run anyway)")
        print("WARNING: " + msg)
    return rscript, node


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--rebuild-corpus", action="store_true")
    ap.add_argument("--allow-version-mismatch", action="store_true")
    a = ap.parse_args()
    mode = "quick" if a.quick else "full"
    res, out = ROOT / "results" / mode, ROOT / "outputs" / mode
    t0 = time.time()
    rscript, node = check_versions(strict=not a.allow_version_mismatch)
    if res.exists(): shutil.rmtree(res)
    res.mkdir(parents=True)
    env = {**os.environ, "OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1"}
    corpus = ROOT / "corpus"
    if a.rebuild_corpus:
        rebuilt = res / "corpus_rebuilt"
        print(sh([sys.executable, "bench/build_corpus.py", str(rebuilt)], env=env).strip().splitlines()[-1])
        for f in ("corpus.csv", "corpus_summary.json"):
            if sha(rebuilt / f) != sha(corpus / f):
                sys.exit(f"the rebuilt {f} differs from the committed corpus/{f}")
        print("corpus rebuilt from metadat's examples: identical to the committed copy")
    lines = (corpus / "corpus.csv").read_text(encoding="utf-8").splitlines(keepends=True)
    if a.quick:
        lines = [lines[0]] + [l for l in lines[1:] if l.split(",", 1)[0].strip('"') in QUICK]
        print("quick mode: meta-analyses", ", ".join(QUICK))
    (res / "corpus.csv").write_text("".join(lines), encoding="utf-8", newline="")
    shutil.copy2(corpus / "corpus_summary.json", res / "corpus_summary.json")
    print(f"corpus: {len(lines) - 1} study rows (corpus/corpus.csv sha256 {sha(corpus / 'corpus.csv')[:12]})")
    print(sh([rscript, "bench/reference_metafor.R", str(res / "corpus.csv"), str(res / "reference.jsonl")], env=env).strip().splitlines()[-1])
    print(sh([node, "bench/run_app.mjs", str(res / "corpus.csv"), str(res / "app.jsonl")], env=env).strip())
    expected = "expected/quick_values.json" if a.quick else "expected/paper_values.json"
    rc = subprocess.run([sys.executable, "analysis/make_outputs.py", "--results", str(res), "--outputs", str(out), "--expected", expected],
                        cwd=ROOT).returncode
    print(f"total time {time.time() - t0:.0f} s; outputs in {out.relative_to(ROOT)}")
    sys.exit(rc)


if __name__ == "__main__":
    main()

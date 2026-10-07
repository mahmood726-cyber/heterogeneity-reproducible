"""Build the validation corpus: every intercept-only random- or fixed-effects model (rma / rma.uni) fitted in the
help-page examples of the R package metadat, with the exact data each model used.

  python bench/build_corpus.py corpus [--workers 3] [--timeout 600]

Each metadat help page's examples (including those marked "do not run", which hold the analyses) are run in a separate
Rscript with rma() and rma.uni() shadowed by a function that calls metafor::rma.uni() and records the yi and vi of every
fit with no moderators (bench/capture_one.R). A page whose examples fail or exceed the time limit is listed, never
dropped silently. bench/assemble_corpus.R then writes corpus.csv (one row per study of each distinct meta-analysis),
corpus_log.tsv (every help page and what happened) and corpus_summary.json.

This takes about half an hour (the examples include slow analyses), so the corpus is committed in corpus/ and
reproduce.py uses that copy; `python reproduce.py --rebuild-corpus` regenerates it and stops if it differs.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def kill_tree(pid):
    if os.name == "nt":
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        try:
            os.killpg(pid, 9)
        except OSError:
            pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("outdir"); ap.add_argument("--workers", type=int, default=3); ap.add_argument("--timeout", type=int, default=600)
    a = ap.parse_args()
    rscript = shutil.which("Rscript") or sys.exit("Rscript not found on PATH")
    out = Path(a.outdir); out.mkdir(parents=True, exist_ok=True)
    caps = Path(tempfile.mkdtemp(prefix="metadat_caps_"))
    names = subprocess.run([rscript, "-e", 'cat(names(tools::Rd_db("metadat")), sep="\\n")'], capture_output=True, text=True,
                           check=True).stdout.split()

    def one(nm):
        t0 = time.time()
        kw = {"start_new_session": True} if os.name != "nt" else {}
        p = subprocess.Popen([rscript, str(ROOT / "bench" / "capture_one.R"), nm, str(caps)],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, **kw)
        try:
            p.wait(timeout=a.timeout)
            st = "RAN" if (caps / (nm[:-3] + ".rds")).exists() else "NO_OUTPUT"
        except subprocess.TimeoutExpired:
            kill_tree(p.pid); p.wait(); st = "TIMEOUT"
        return nm, st, time.time() - t0

    with ThreadPoolExecutor(a.workers) as ex:
        runs = list(ex.map(one, names))
    with open(caps / "runs.tsv", "w", encoding="utf-8") as f:
        for nm, st, dt in runs:
            f.write(f"{nm}\t{st}\t{dt:.1f}\n")
    p = subprocess.run([rscript, str(ROOT / "bench" / "assemble_corpus.R"), str(caps), str(out)], capture_output=True, text=True)
    sys.stdout.write(p.stdout); sys.stderr.write(p.stderr)
    shutil.rmtree(caps, ignore_errors=True)
    sys.exit(p.returncode)


if __name__ == "__main__":
    main()

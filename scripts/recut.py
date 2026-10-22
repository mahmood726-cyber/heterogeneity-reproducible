"""Recut integrity, safe output preservation, and measured result summaries."""
import argparse
import ast
import hashlib
import importlib
import json
import math
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = "SOURCE_SHA256.json"
IGNORED_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "outputs", "results", ".tmp", "tmp", "temp", ".pytest_cache"}
IGNORED_FILES = {MANIFEST, "PROGRESS.md"}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(root=ROOT):
    files = {}
    for current, dirs, names in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in IGNORED_DIRS and ".prev-" not in d
                         and not d.startswith("_recut_test_") and not d.endswith(".tmp"))
        for name in sorted(names):
            p = Path(current) / name
            if name in IGNORED_FILES or p.suffix in {".pyc", ".sqlite"}:
                continue
            rel = p.relative_to(root).as_posix()
            if rel.startswith("docs/screenshots/") and (p.suffix == ".tif" or name.startswith("_full_")):
                continue
            if p.is_symlink():
                raise ValueError(f"Published symlink refused: {rel}")
            files[rel] = sha(p)
    return dict(sorted(files.items()))


def checked_path(root, relative):
    p = (root / relative).resolve()
    if not p.is_relative_to(root.resolve()) or p == root.resolve():
        raise ValueError(f"Path escapes archive: {relative}")
    return p


def verify_hashes(records, root=ROOT):
    if not records:
        raise ValueError("Empty hash manifest")
    for rel, want in records.items():
        p = checked_path(root, rel)
        if not p.is_file() or sha(p) != want:
            raise ValueError(f"SHA-256 mismatch or missing file: {rel}")
    return len(records)


def protected():
    records = json.loads((ROOT / "ORIGINAL_VALIDATION_SHA256.json").read_text())["sha256"]
    n = verify_hashes(records)
    print(f"PROTECTED ORIGINALS: {n}/{n} byte-identical")
    return n


def app_integrity(upstream=None):
    provenance = json.loads((ROOT / "APP_SOURCE_FILES.json").read_text())
    paths = [row["path"] for row in provenance["files"]]
    actual = {p.relative_to(ROOT).as_posix() for p in (ROOT / "app").rglob("*") if p.is_file()}
    if len(paths) != len(set(paths)) or set(paths) != actual:
        raise ValueError("App file inventory differs from provenance")
    if upstream is not None:
        source = Path(upstream).resolve()
        for rel in paths:
            p = checked_path(source, rel.removeprefix("app/"))
            if not p.is_file() or p.read_bytes() != (ROOT / rel).read_bytes():
                raise ValueError(f"Upstream byte mismatch: {rel}")
        print(f"UPSTREAM APP BYTES: {len(paths)}/{len(paths)} identical")
    manifest = json.loads((ROOT / "app/heterogeneity/validate/MANIFEST.json").read_text())
    count = 0
    for spec in manifest["files"]:
        p = checked_path(ROOT / "app/heterogeneity", spec["path"])
        if sha(p) != spec["sha256"] or p.stat().st_size != spec["bytes"]:
            raise ValueError(f"Upstream corpus pin mismatch: {spec['path']}")
        count += 1
    print(f"APP CORPUS PINS: {count}/{count}")
    base = ROOT / "app/r-shiny/shinylive/webr"
    wm = json.loads((base / "repo/manifest.json").read_text())
    records = {p["package"]: p for p in wm["packages"]}
    for name in provenance["webR_packages"]:
        spec = records[name]
        p = checked_path(base, spec.get("path", "repo/" + wm["layout"] + spec["file"]))
        if sha(p) != spec["sha256"] or p.stat().st_size != spec["bytes"]:
            raise ValueError(f"webR package pin mismatch: {name}")
    n = len(provenance["webR_packages"])
    print(f"WEBR PACKAGE PINS: {n}/{n}")



def source_corpus():
    """Strict cross-source byte check; retained as a failing diagnostic for the documented CRLF exception."""
    manifest = json.loads((ROOT / "app/heterogeneity/validate/MANIFEST.json").read_text())
    original_sha = sha(ROOT / "corpus/corpus.csv")
    if original_sha != manifest["source_files"]["corpus.csv"]:
        raise ValueError("Original corpus bytes differ from upstream source pin; investigate without editing originals")
    print("Original corpus source pin matches")


def manifest(write=False, upstream=None):
    protected()
    app_integrity(upstream)
    current = inventory()
    p = ROOT / MANIFEST
    if write:
        p.write_text(json.dumps({"algorithm": "sha256",
            "scope": "Published archive files; excludes this manifest, generated results/outputs, dependencies, caches, temporary folders, PROGRESS.md and *.prev-* folders",
            "files": current}, indent=2) + "\n", encoding="utf-8", newline="\n")
        print(f"MANIFEST WRITTEN: {len(current)} files")
    else:
        recorded = json.loads(p.read_text())["files"]
        if set(recorded) != set(current):
            raise ValueError(f"Manifest inventory differs; missing={sorted(set(recorded)-set(current))}; unlisted={sorted(set(current)-set(recorded))}")
        n = verify_hashes(recorded)
        print(f"MANIFEST: {n}/{n} SHA-256 checks passed")


def preserve(mode):
    for area in ("results", "outputs"):
        p = checked_path(ROOT, f"{area}/{mode}")
        if not p.exists():
            print(f"PRESERVE: {area}/{mode} absent")
            continue
        if not p.is_dir() or p.is_symlink():
            raise ValueError(f"Not an ordinary output directory: {area}/{mode}")
        n = 1
        while p.with_name(f"{mode}.prev-{n}").exists():
            n += 1
        dest = checked_path(ROOT, f"{area}/{mode}.prev-{n}")
        p.rename(dest)
        print(f"PRESERVED: {area}/{mode} -> {area}/{dest.name}")


def summarize(mode):
    st = json.loads((ROOT / "outputs" / mode / "stats.json").read_text())
    expected_name = "quick_values.json" if mode == "quick" else "paper_values.json"
    expected = json.loads((ROOT / "expected" / expected_name).read_text())["values"]
    bad = []
    passed = 0
    for key, spec in expected.items():
        got, want = st.get(key), spec["value"]
        if isinstance(want, str):
            ok = got == want
        else:
            ok = isinstance(got, (int, float)) and math.isfinite(got) and round(got, spec["decimals"]) == round(want, spec["decimals"])
        passed += ok
        if not ok:
            bad.append(key)
    total, numerical = st["checks_total"], st["checks_passed"]
    displayed, display_fail = st["displayed_numbers"], st["displayed_fail"]
    print(f"{mode.upper()} NUMERICAL: {numerical}/{total}")
    print(f"{mode.upper()} DISPLAY: {displayed-display_fail}/{displayed} (recorded display failures: {display_fail})")
    print(f"{mode.upper()} EXPECTED VALUES: {passed}/{len(expected)}")
    if bad or numerical != total or st["checks_failed"] != 0 or display_fail != 0:
        raise ValueError(f"Original validation failed: {bad}; numerical failures={total-numerical}; display failures={display_fail}")


def preflight():
    for name in ("numpy", "matplotlib"):
        module = importlib.import_module(name)
        print(f"PYTHON IMPORT: {name} {module.__version__}")
    for name in ("Rscript", "node"):
        if not shutil.which(name):
            raise ValueError(f"{name} missing from PATH")
    pw = Path(os.environ["PLAYWRIGHT_MODULE"]).resolve() if os.environ.get("PLAYWRIGHT_MODULE") else ROOT / "node_modules/playwright"
    for name in ("package.json", "index.mjs"):
        if not (pw / name).is_file():
            raise ValueError(f"Playwright package lacks {name}; set PLAYWRIGHT_MODULE or npm ci")
    print("PLAYWRIGHT VERSION:", json.loads((pw / "package.json").read_text())["version"])
    for name in ("reproduce.py", "analysis/checks.py", "analysis/make_outputs.py"):
        ast.parse((ROOT / name).read_text(encoding="utf-8"), filename=name)
    print("PREFLIGHT: Python imports, runner syntax, executable paths and Playwright package present")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)
    m = sub.add_parser("manifest")
    m.add_argument("--write", action="store_true")
    m.add_argument("--upstream")
    for name in ("preserve", "counts"):
        sub.add_parser(name).add_argument("mode", choices=("quick", "full"))
    sub.add_parser("preflight")
    sub.add_parser("extras")
    sub.add_parser("source-corpus")
    args = ap.parse_args()
    try:
        if args.command == "manifest":
            manifest(args.write, args.upstream)
        elif args.command == "preserve":
            preserve(args.mode)
        elif args.command == "counts":
            summarize(args.mode)
        elif args.command == "source-corpus":
            source_corpus()
        elif args.command == "preflight":
            preflight()
        else:
            print("EXTRAS: NOT APPLICABLE (no numerical plus suite; APP.txt PR #163)")
    except (OSError, ValueError, KeyError, ImportError) as exc:
        sys.exit(f"RECUT FAILED: {exc}")


if __name__ == "__main__":
    main()

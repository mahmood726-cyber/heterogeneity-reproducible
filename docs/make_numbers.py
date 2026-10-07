"""Write docs/numbers.json: every number printed in docs/paper.md, its value as printed, and the stats key it comes from.

  python docs/make_numbers.py outputs/full/stats.json "<source description>"
Fails if a printed value is not what the run gives after rounding as printed, or if a printed number is missing from the
paper's text.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# (quantity, as printed, stats key, how the printed text is derived from the value)
N = [
    ("tau^2 estimators", "eight", "estimators", "word"),
    ("Meta-analyses in the corpus", "88", "meta_analyses", "int"),
    ("metadat datasets contributing", "49", "pages_contributing", "int"),
    ("Fewest studies in a meta-analysis", "4", "k_min", "int"),
    ("Most studies in a meta-analysis", "160", "k_max", "int"),
    ("Study rows", "2,241", "studies_total", "comma"),
    ("Effect measures", "23", "measures", "int"),
    ("Help pages that exceeded the time limit", "two", "pages_timed_out", "word"),
    ("Analyses (meta-analyses x estimators)", "704", "configurations", "int"),
    ("Checks", "131,781", "checks_total", "comma"),
    ("Checks passed", "131,781", "checks_passed", "comma"),
    ("The check count as the paper defines it", "yes", "check_formula_holds", "flag"),
    ("Analyses refused by both (DL, k < 10)", "28", "dl_refused", "int"),
    ("Analyses compared", "676", "configurations_compared", "int"),
    ("Every difference below 5e-10", "yes", "all_below_5e-10", "flag"),
    ("Estimates and intervals below 1e-10", "yes", "estimates_below_1e-10", "flag"),
    ("Displayed numbers that matched", "120,720", "displayed_numbers", "comma"),
    ("Displayed numbers that did not match", "0", "displayed_fail", "int"),
    ("metafor default controls move tau^2 by up to 1e-4 (between 1e-5 and 1e-4)", "yes", "metafor_default_between_1e-5_and_1e-4", "flag"),
    ("Worked example: studies", "13", "ex_k", "int"),
    ("Worked example: Q", "152.2", "ex_Q", "1dp"),
    ("Worked example: df", "12", "ex_df", "int"),
    ("Worked example: I^2 (%)", "92.1", "ex_I2", "1dp"),
    ("Worked example: I^2 lower limit (%)", "81.9", "ex_I2_lo", "1dp"),
    ("Worked example: I^2 upper limit (%)", "97.7", "ex_I2_hi", "1dp"),
    ("Worked example: smallest tau^2", "0.228", "ex_tau2_min", "3dp"),
    ("Worked example: its estimator (Hunter-Schmidt)", "HS", "ex_tau2_min_est", "HS"),
    ("Worked example: largest tau^2", "0.346", "ex_tau2_max", "3dp"),
    ("Worked example: its estimator (Sidik-Jonkman)", "SJ", "ex_tau2_max_est", "SJ"),
    ("Worked example: REML risk ratio", "0.49", "ex_rr_reml", "2dp"),
    ("Worked example: HKSJ lower limit", "0.33", "ex_rr_reml_hk_lo", "2dp"),
    ("Worked example: HKSJ upper limit", "0.73", "ex_rr_reml_hk_hi", "2dp"),
    ("Worked example: prediction interval lower", "0.14", "ex_rr_reml_pi_lo", "2dp"),
    ("Worked example: prediction interval upper", "1.76", "ex_rr_reml_pi_hi", "2dp"),
    ("Worked example: most influential trial", "Hart & Sutherland, 1977", "ex_baujat_top", "Hart & Sutherland, 1977"),
]
WORDS = {2: "two", 8: "eight"}
# where each printed text must appear in the paper (the word form or the digits as printed)
IN_TEXT = {"Hart & Sutherland, 1977": "Hart and Sutherland", "HS": "Hunter–Schmidt", "SJ": "Sidik–Jonkman", "yes": None}


def shown(v, how):
    if how == "int": return str(int(round(v)))
    if how == "comma": return f"{int(round(v)):,}"
    if how == "word": return WORDS.get(int(round(v)), str(v))
    if how == "flag": return "yes" if v == 1 else "no"
    if how.endswith("dp"): return f"{v:.{int(how[0])}f}"
    return how if v == how else f"MISMATCH {v}"


st = json.loads(Path(sys.argv[1]).read_text())
src = sys.argv[2] if len(sys.argv) > 2 else "reproduce.py full run"
paper = (ROOT / "docs" / "paper.md").read_text(encoding="utf-8").split("## References")[0]
out, bad = [], []
for q, printed, k, how in N:
    s = shown(st[k], how)
    if s != printed: bad.append(f"{q}: printed {printed}, run gives {s}")
    needle = IN_TEXT.get(printed, printed)
    if needle and needle not in paper: bad.append(f"{q}: '{needle}' not found in paper.md")
    out.append({"quantity": q, "printed": printed, "stats_key": k, "value": st[k]})
if bad: sys.exit("numbers.json NOT written:\n  " + "\n  ".join(bad))
(ROOT / "docs" / "numbers.json").write_text(json.dumps({"source": src, "numbers": out}, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"docs/numbers.json: {len(out)} numbers, all as printed")

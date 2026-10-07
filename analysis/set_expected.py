"""Write expected/*.json from a run's stats.json (used once, to record the canonical run).

  python analysis/set_expected.py outputs/full/stats.json expected/paper_values.json full
  python analysis/set_expected.py outputs/quick/stats.json expected/quick_values.json quick
Each number is stored rounded to the precision at which the paper prints it. Discrepancy maxima, which differ between
platforms in their last digits, enter only as threshold indicators (0/1).
"""
import json
import sys

# quantity -> decimals ("str" for text)
FULL = {"help_pages": 0, "pages_contributing": 0, "pages_timed_out": 0, "meta_analyses": 0, "studies_total": 0, "k_min": 0,
        "k_max": 0, "measures": 0, "estimators": 0, "configurations": 0, "dl_refused": 0, "configurations_compared": 0,
        "checks_total": 0, "checks_passed": 0, "checks_failed": 0, "all_pass": 0, "check_formula_holds": 0, "refusals_agree": 0,
        "all_below_5e-10": 0, "estimates_below_1e-10": 0, "displayed_numbers": 0, "displayed_fail": 0,
        "baujat_crosschecks_agree": 0, "baujat_crosschecks_other": 0, "metafor_default_between_1e-5_and_1e-4": 0,
        "qprofile_upper_beyond_metafor_default": 0,
        "ex_k": 0, "ex_Q": 1, "ex_df": 0, "ex_I2": 1, "ex_I2_lo": 1, "ex_I2_hi": 1, "ex_tau2_lo": 4, "ex_tau2_hi": 4,
        "ex_tau2_min": 3, "ex_tau2_max": 3, "ex_tau2_min_est": "str", "ex_tau2_max_est": "str", "ex_rr_reml": 2,
        "ex_rr_reml_hk_lo": 2, "ex_rr_reml_hk_hi": 2, "ex_rr_reml_pi_lo": 2, "ex_rr_reml_pi_hi": 2, "ex_baujat_top": "str"}
QUICK = {"meta_analyses": 0, "checks_total": 0, "checks_passed": 0, "all_pass": 0, "check_formula_holds": 0, "all_below_5e-10": 0,
         "displayed_fail": 0, "ex_Q": 1, "ex_I2": 1, "ex_rr_reml": 2, "ex_baujat_top": "str"}

stats, out, mode = sys.argv[1:4]
st = json.load(open(stats))
spec = FULL if mode == "full" else QUICK
vals = {}
for k, d in spec.items():
    if d == "str":
        vals[k] = {"value": st[k], "decimals": 0}
        continue
    v = round(float(st[k]), d)
    vals[k] = {"value": int(v) if d <= 0 else v, "decimals": d}
json.dump({"source": f"Canonical run ({mode} mode): values as printed in the paper.", "values": vals}, open(out, "w"), indent=1)
print(f"wrote {len(vals)} expected values to {out}")

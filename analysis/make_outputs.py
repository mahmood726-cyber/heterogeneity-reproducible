"""Compare the app with metafor and build every table, figure and number in the paper.

  python analysis/make_outputs.py --results results/full --outputs outputs/full --expected expected/paper_values.json

The comparison (what one check is, and the typed tolerances) is defined in analysis/checks.py. Exit code 0 only if
every number in the expected file is reproduced (after rounding to its stated decimals).
"""
import argparse
import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from checks import KEYS, LABEL, TOL, checks  # noqa: E402

PRETTY = {"k": "Studies read", "Q": "Q", "df": "df of Q", "p(Q)": "p-value of Q", "I2": "I²", "tau2 CI lower": "τ² CI, lower",
          "tau2 CI upper": "τ² CI, upper", "I2 CI lower": "I² CI, lower", "I2 CI upper": "I² CI, upper", "tau2": "τ²",
          "mu": "Pooled estimate", "SE": "Its SE", "CI lower (z)": "95% CI (z), lower", "CI upper (z)": "95% CI (z), upper",
          "HKSJ CI lower": "HKSJ CI, lower", "HKSJ CI upper": "HKSJ CI, upper", "PI lower": "Prediction interval, lower",
          "PI upper": "Prediction interval, upper", "LOO mu": "Leave-one-out estimate", "LOO CI lower": "Leave-one-out CI, lower",
          "LOO CI upper": "Leave-one-out CI, upper", "LOO I2": "Leave-one-out I²", "LOO tau2": "Leave-one-out τ²",
          "Baujat x": "Baujat x", "Baujat y": "Baujat y"}
EXAMPLE = "dat.bcg#1"   # worked example: BCG vaccine (log risk ratios, 13 trials)


def jl(p):
    return {json.loads(l)["analysis"]: json.loads(l) for l in open(p, encoding="utf-8") if l.strip()}


def write(out, name, rows):
    with open(out / f"{name}.csv", "w", newline="", encoding="utf-8") as fh:
        fields = list(dict.fromkeys(k for r in rows for k in r))
        w = csv.DictWriter(fh, fieldnames=fields, restval=""); w.writeheader(); w.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", required=True); ap.add_argument("--outputs", required=True); ap.add_argument("--expected", required=True)
    ap.add_argument("--corpus-summary", default=None)
    a = ap.parse_args()
    res, out = Path(a.results), Path(a.outputs)
    out.mkdir(parents=True, exist_ok=True)
    R, A = jl(res / "reference.jsonl"), jl(res / "app.jsonl")
    corpus = list(csv.DictReader(open(res / "corpus.csv", encoding="utf-8")))
    summ = json.loads(Path(a.corpus_summary or (res / "corpus_summary.json")).read_text())
    ids = list(dict.fromkeys(r["analysis"] for r in corpus))
    if set(ids) != set(R) or set(ids) != set(A):
        sys.exit("corpus, reference and app runs cover different meta-analyses")
    info = {i: next(r for r in corpus if r["analysis"] == i) for i in ids}
    ds_of = {i: info[i]["dataset"] for i in ids}
    k_of = {i: int(info[i]["k"]) for i in ids}

    # ---- every check ----
    st = {"help_pages": summ["help_pages"], "pages_contributing": summ["pages_contributing"],
          "pages_timed_out": summ["pages_timed_out"], "pages_with_errors": summ["pages_with_errors"],
          "meta_analyses": len(ids), "studies_total": len(corpus), "k_min": min(k_of.values()), "k_max": max(k_of.values()),
          "k_median": sorted(k_of.values())[len(ids) // 2] if len(ids) % 2 else
                      0.5 * (sorted(k_of.values())[len(ids) // 2 - 1] + sorted(k_of.values())[len(ids) // 2]),
          "estimators": len(KEYS), "metadat": summ["metadat"], "metafor": summ["metafor"]}
    measures = defaultdict(int)
    for i in ids: measures[info[i]["measure"] or "(precomputed)"] += 1
    st["measures"] = len(measures)
    worst_q, worst_g, per_ds, per_conf, allrows = defaultdict(float), defaultdict(float), defaultdict(lambda: defaultdict(float)), {}, []
    n_checks = n_pass = 0
    n_by_q, kind_of, group_of = defaultdict(int), {}, {}
    fails = []
    for i in ids:
        for q, g, kind, key, idx, av, bv, d in checks(A[i], R[i]):
            n_checks += 1
            ok = d <= TOL[kind]
            n_pass += ok
            if not ok:
                fails.append((i, q, key, idx, av, bv, d))
            if q == "refusal":
                continue
            kind_of[q], group_of[q] = kind, g
            n_by_q[q] += 1
            worst_q[q] = max(worst_q[q], d); worst_g[g] = max(worst_g[g], d)
            per_ds[ds_of[i]][kind] = max(per_ds[ds_of[i]][kind], d)
            ck = (i, key or "all")
            per_conf.setdefault(ck, defaultdict(float))
            per_conf[ck][kind] = max(per_conf[ck][kind], d)
    for f in fails[:40]:
        print("OUTSIDE TOLERANCE:", *f)
    refusals = sum(1 for i in ids if k_of[i] < 10)
    # the count as the paper defines it: per meta-analysis 9 + 8 refusal checks, and 9 + 7k per estimator offered
    st["check_formula_holds"] = int(n_checks == sum(9 + 8 + (8 if k_of[i] >= 10 else 7) * (9 + 7 * k_of[i]) for i in ids))
    st.update({"configurations": len(ids) * len(KEYS), "dl_refused": refusals, "configurations_compared": len(ids) * len(KEYS) - refusals,
               "checks_total": n_checks, "checks_passed": n_pass, "checks_failed": n_checks - n_pass,
               "all_pass": int(n_checks == n_pass),
               "max_rel": max(v for q, v in worst_q.items() if kind_of[q] == "REL"),
               "max_abs": max(v for q, v in worst_q.items() if kind_of[q] == "ABS"),
               "all_below_1e-11": int(max(worst_q.values()) < 1e-11),
               "max_estimates": worst_g["estimates"], "max_heterogeneity": worst_g["heterogeneity"],
               "max_leave_one_out": worst_g["leave-one-out"], "max_baujat": worst_g["Baujat"], "max_pvalues": worst_g["p-values"],
               "max_overall": max(worst_q.values()),
               # printed as thresholds (the maxima move in their last digits between platforms with R's maths library)
               "all_below_5e-10": int(max(worst_q.values()) < 5e-10), "estimates_below_1e-10": int(worst_g["estimates"] < 1e-10),
               "refusals_agree": int(all(d == 0 for i in ids for q, *_r, d in checks(A[i], R[i]) if q == "refusal"))})
    # numbers displayed on the page (rounded) that agree with the computed values
    disp = sum(A[i]["display"][k]["numbers"] for i in ids for k in KEYS)
    disp_fail = sum(len(A[i]["display"][k]["fails"]) for i in ids for k in KEYS)
    st.update({"displayed_numbers": disp, "displayed_fail": disp_fail})
    for i in ids:
        for k in KEYS:
            for f in A[i]["display"][k]["fails"][:3]: print("DISPLAY MISMATCH:", i, k, f)

    # ---- metafor's own default convergence controls (reported, not a check) ----
    iterative = {"pm", "reml", "ml", "eb"}
    dflt = defaultdict(float)
    for i in ids:
        for k in KEYS:
            r = R[i]["configs"][k]
            if r.get("refused") in (True, "true") or "error" in r or r.get("tau2_default") is None: continue
            dflt[k] = max(dflt[k], abs(r["tau2_default"] - r["tau2"]) / max(1.0, abs(r["tau2"])))
    st.update({"metafor_default_max_tau2_rel": max(dflt[k] for k in iterative), "metafor_default_closed_form_max": max(dflt[k] for k in KEYS if k not in iterative)})
    st["metafor_default_between_1e-5_and_1e-4"] = int(1e-5 < st["metafor_default_max_tau2_rel"] <= 1e-4)
    # the leave-one-out form of the Baujat y-axis against metafor::baujat() itself (run for k <= 40)
    bjc = [R[i]["configs"][k].get("baujat_check") for i in ids for k in KEYS if "baujat_check" in R[i]["configs"][k]]
    st.update({"baujat_crosschecks_agree": sum(c == "agrees" for c in bjc),
               "baujat_crosschecks_other": sum(c not in ("agrees", "not run (k < 3 or k > 40)") for c in bjc)})
    if st["baujat_crosschecks_other"]:
        sys.exit("the leave-one-out Baujat values disagree with metafor::baujat(): " + "; ".join(sorted({c for c in bjc if c not in ("agrees", "not run (k < 3 or k > 40)")})))
    st["qprofile_upper_beyond_metafor_default"] = sum(1 for i in ids if R[i]["common"]["tau2_hi"] is not None and R[i]["common"]["tau2_hi"] > 100)

    # ---- tables ----
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "docs"))
    import references as REFS
    refno, _ = REFS.numbering(list(dict.fromkeys(ds_of[i] for i in ids)))
    T1 = []
    for ds in dict.fromkeys(ds_of[i] for i in ids):
        its = [i for i in ids if ds_of[i] == ds]
        T1.append({"dataset": ds, "source_reference": refno[ds], "meta_analyses": len(its), "measures": "; ".join(sorted({info[i]["measure"] or "(precomputed)" for i in its})),
                   "studies_min": min(k_of[i] for i in its), "studies_max": max(k_of[i] for i in its),
                   "max_relative_difference": per_ds[ds]["REL"], "max_absolute_difference": per_ds[ds]["ABS"],
                   "all_within_tolerance": not any(f[0] in its for f in fails)})
    write(out, "table1_by_dataset", T1)
    T2 = [{"quantity": q, "label": PRETTY.get(q, q), "group": group_of[q], "tolerance": f"{kind_of[q].lower()} {TOL[kind_of[q]]:g}" if kind_of[q] != "EXACT" else "exact",
           "checks": n_by_q[q], "max_difference": worst_q[q], "all_within": worst_q[q] <= TOL[kind_of[q]]} for q in n_by_q]
    if all(t["all_within"] for t in T2) != (not [f for f in fails if f[1] != "refusal"]):
        sys.exit("internal inconsistency: table 2 disagrees with the per-check verdicts")
    write(out, "table2_by_quantity", T2)
    T3 = [{"analysis": i, "dataset": ds_of[i], "measure": info[i]["measure"], "k": k_of[i], "estimator": LABEL.get(key, key),
           "refused": key == "dl" and k_of[i] < 10, "max_relative_difference": v["REL"], "max_absolute_difference": v["ABS"]}
          for (i, key), v in per_conf.items()]
    write(out, "table3_all_analyses", T3)
    write(out, "table4_metafor_default_controls", [{"estimator": LABEL[k], "iterative": k in iterative, "max_relative_tau2_change_default_vs_tight": dflt[k]} for k in KEYS])

    # ---- worked example: BCG ----
    if EXAMPLE in ids:
        r, ap_ = R[EXAMPLE], A[EXAMPLE]
        c = ap_["configs"]
        st.update({"ex_k": k_of[EXAMPLE], "ex_Q": c["pm"]["sum"]["Q"], "ex_df": c["pm"]["sum"]["df"], "ex_I2": c["pm"]["sum"]["I2"],
                   "ex_I2_lo": c["pm"]["qpci"]["I2Lo"], "ex_I2_hi": c["pm"]["qpci"]["I2Hi"],
                   "ex_tau2_lo": c["pm"]["qpci"]["tau2Lo"], "ex_tau2_hi": c["pm"]["qpci"]["tau2Hi"],
                   "ex_tau2_min": min(c[k]["tau2"] for k in KEYS), "ex_tau2_max": max(c[k]["tau2"] for k in KEYS),
                   "ex_tau2_min_est": LABEL[min(KEYS, key=lambda k: c[k]["tau2"])], "ex_tau2_max_est": LABEL[max(KEYS, key=lambda k: c[k]["tau2"])],
                   "ex_rr_reml": math.exp(c["reml"]["sum"]["mu"]), "ex_rr_reml_hk_lo": math.exp(c["reml"]["sum"]["ciLoHKSJ"]),
                   "ex_rr_reml_hk_hi": math.exp(c["reml"]["sum"]["ciHiHKSJ"]), "ex_rr_reml_pi_lo": math.exp(c["reml"]["pi"]["lo"]),
                   "ex_rr_reml_pi_hi": math.exp(c["reml"]["pi"]["hi"]),
                   "ex_max_rel": max(per_conf[(EXAMPLE, k)]["REL"] for k in KEYS)})
        # the most influential trial by Baujat (REML)
        bj = c["reml"]["baujat"]
        top = max(range(len(bj)), key=lambda j: bj[j]["y"])
        st.update({"ex_baujat_top": bj[top]["label"], "ex_baujat_top_y": bj[top]["y"]})
    (out / "stats.json").write_text(json.dumps(st, indent=1, default=float))

    # ---- figures ----
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "figure.facecolor": "white", "savefig.facecolor": "white"})
    meta = {"Software": None}
    C = {"app": "#1b6ca8", "ref": "#333333", "pi": "#999999"}
    if EXAMPLE in ids:
        r, c = R[EXAMPLE]["configs"], A[EXAMPLE]["configs"]
        fig, axs = plt.subplots(1, 2, figsize=(9.6, 4.4), gridspec_kw={"width_ratios": [1.35, 1]})
        ax = axs[0]
        order = ["dl", "he", "hs", "sj", "ml", "reml", "pm", "eb"]
        for y, k in enumerate(order):
            rk, ck = r[k], c[k]
            ax.plot([math.exp(rk["pi_lo"]), math.exp(rk["pi_hi"])], [y, y], "-", color=C["pi"], lw=6, alpha=0.35, solid_capstyle="butt", label="metafor: 95% prediction interval" if y == 0 else None)
            ax.plot([math.exp(rk["hk_lo"]), math.exp(rk["hk_hi"])], [y, y], "-", color=C["ref"], lw=1.8, label="metafor: 95% CI (HKSJ)" if y == 0 else None)
            ax.plot([math.exp(rk["mu"])], [y], "s", color=C["ref"], ms=7, label="metafor: estimate" if y == 0 else None)
            ax.plot([math.exp(ck["sum"]["mu"])], [y], "o", color=C["app"], ms=4, label="App: estimate" if y == 0 else None)
            ax.plot([math.exp(v) for v in (ck["sum"]["ciLoHKSJ"], ck["sum"]["ciHiHKSJ"], ck["pi"]["lo"], ck["pi"]["hi"])], [y] * 4, "|", color=C["app"], ms=11, mew=1.6, label="App: interval limits" if y == 0 else None)
        ax.axvline(1, color="#bbbbbb", lw=0.8); ax.set_xscale("log")
        from matplotlib.ticker import FixedFormatter, FixedLocator, NullLocator
        tk = [0.1, 0.2, 0.5, 1, 2]; ax.xaxis.set_major_locator(FixedLocator(tk)); ax.xaxis.set_major_formatter(FixedFormatter([f"{t:g}" for t in tk])); ax.xaxis.set_minor_locator(NullLocator())
        ax.set_yticks(range(len(order)), [f"{LABEL[k]} (τ² = {c[k]['tau2']:.3f})" for k in order]); ax.set_ylim(-0.6, len(order) - 0.4)
        ax.set_xlabel("Risk ratio of tuberculosis, BCG vaccine versus control")
        ax.set_title("A. Pooled estimate by τ² estimator", fontsize=9.5)
        ax.legend(fontsize=7, frameon=False, loc="upper center", bbox_to_anchor=(0.45, -0.17), ncol=3)
        ax = axs[1]
        bx_r, by_r = r["reml"]["baujat_x"], r["reml"]["baujat_y"]
        ax.plot(bx_r, by_r, "s", color=C["ref"], ms=8, mfc="none", label="metafor::baujat")
        ax.plot([b["x"] for b in c["reml"]["baujat"]], [b["y"] for b in c["reml"]["baujat"]], "o", color=C["app"], ms=4, label="App")
        for b in sorted(c["reml"]["baujat"], key=lambda b: -b["y"])[:3]:   # the three most influential trials
            ax.annotate(b["label"], (b["x"], b["y"]), fontsize=7, xytext=(-6, 5), textcoords="offset points", ha="right")
        ax.set_xlabel("Squared Pearson residual (REML)"); ax.set_ylabel("Influence on the pooled estimate")
        ax.set_title("B. Baujat plot (REML)", fontsize=9.5); ax.legend(fontsize=7.5, frameon=False, loc="upper left")
        fig.suptitle(f"Figure 2. Worked example: BCG vaccine ({k_of[EXAMPLE]} trials); the app (blue) over metafor", fontsize=10)
        fig.tight_layout(); fig.savefig(out / "figure2_worked_example.png", dpi=300, metadata=meta); plt.close(fig)
        with open(out / "figure2_worked_example.csv", "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh); w.writerow(["estimator", "tau2_app", "tau2_metafor", "RR_app", "RR_metafor", "HKSJ_low_app", "HKSJ_high_app", "PI_low_app", "PI_high_app"])
            for k in order:
                w.writerow([LABEL[k], c[k]["tau2"], r[k]["tau2"], math.exp(c[k]["sum"]["mu"]), math.exp(r[k]["mu"]), math.exp(c[k]["sum"]["ciLoHKSJ"]),
                            math.exp(c[k]["sum"]["ciHiHKSJ"]), math.exp(c[k]["pi"]["lo"]), math.exp(c[k]["pi"]["hi"])])
    # Figure 3: largest difference per meta-analysis for each quantity (strip), tolerance line
    qs = list(n_by_q)
    per_q_an = defaultdict(lambda: defaultdict(float))
    for i in ids:
        for q, g, kind, key, idx, av, bv, d in checks(A[i], R[i]):
            if q not in ("refusal", "k", "df"): per_q_an[q][i] = max(per_q_an[q][i], d)
    qs = [q for q in qs if q not in ("k", "df")]
    fig, ax = plt.subplots(figsize=(7.8, 0.32 * len(qs) + 2.0))
    lg = lambda v: math.log10(max(v, 1e-17))
    import random
    rnd = random.Random(1)
    for y, q in enumerate(qs):
        vals = list(per_q_an[q].values())
        ax.plot([lg(v) for v in vals], [y + rnd.uniform(-0.25, 0.25) for _ in vals], "o", ms=2.2, alpha=0.5,
                color="#1b6ca8" if kind_of[q] == "REL" else "#c27c0e")
    ax.axvline(-9, color="#444444", ls="--", lw=0.8)
    ax.set_yticks(range(len(qs)), [f"{PRETTY.get(q, q)} ({'relative' if kind_of[q] == 'REL' else 'absolute'})" for q in qs]); ax.invert_yaxis(); ax.set_xlim(-17.5, -7)
    ax.set_xlabel("log10 largest difference from metafor in one meta-analysis (exact agreement shown at -17)")
    ax.set_title(f"Figure 3. App versus metafor: {len(ids)} meta-analyses, {len(KEYS)} τ² estimators\n(each point: one meta-analysis; dashed: tolerance 1e-9)", fontsize=9.5)
    ax.grid(axis="x", color="#eeeeee", lw=0.6)
    fig.tight_layout(); fig.savefig(out / "figure3_agreement.png", dpi=300, metadata=meta); plt.close(fig)
    with open(out / "figure3_agreement.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["quantity", "tolerance_kind", "analysis", "largest_difference"])
        for q in qs:
            for i, v in per_q_an[q].items(): w.writerow([q, kind_of[q], i, v])
    # visual abstract
    fig = plt.figure(figsize=(11, 4.6)); fig.patch.set_facecolor("white")
    boxes = [("Problem", "Heterogeneity in a\nmeta-analysis is usually\nquantified in R (metafor)\nor Stata."),
             ("Tool", "allmeta heterogeneity app:\noffline, in the browser.\n8 τ² estimators, Q, I² with\nits CI, HKSJ and prediction\nintervals, leave-one-out,\nBaujat plot."),
             ("Validation", f"Against R metafor on\n{st['meta_analyses']} meta-analyses from the\nexamples of {st['pages_contributing']} metadat datasets,\n{len(KEYS)} τ² estimators each."),
             ("Result", f"All {st['checks_total']:,} checks pass:\nevery difference below\n5 × 10⁻¹⁰, and the same\n{st['dl_refused']} refusals.")]
    for j, (hh, txt) in enumerate(boxes):
        x = 0.02 + j * 0.245
        fig.patches.append(matplotlib.patches.FancyBboxPatch((x, 0.22), 0.22, 0.60, boxstyle="round,pad=0.01", transform=fig.transFigure,
                                                             facecolor=["#f4ece8", "#e8f0f7", "#eaf4ec", "#fdf6e3"][j], edgecolor="#999"))
        fig.text(x + 0.11, 0.75, hh, ha="center", fontsize=13, weight="bold")
        fig.text(x + 0.11, 0.48, txt, ha="center", va="center", fontsize=10.5, linespacing=1.4)
        if j < 3: fig.text(x + 0.2325, 0.52, "→", ha="center", va="center", fontsize=18)
    fig.text(0.5, 0.09, "One command reproduces every number on Linux, Windows, macOS and Docker: github.com/mahmood726-cyber/heterogeneity-reproducible",
             ha="center", fontsize=9, color="#333333")
    fig.text(0.5, 0.91, "A browser tool for heterogeneity in meta-analysis, validated against R metafor", ha="center", fontsize=13.5, weight="bold")
    fig.savefig(out / "visual_abstract.png", dpi=300, metadata=meta); plt.close(fig)

    # ---- PASS/FAIL against the expected values ----
    exp = json.loads(Path(a.expected).read_text())
    rep = []
    for k, spec in exp["values"].items():
        g_ = st.get(k)
        if isinstance(spec["value"], str):
            okv = g_ == spec["value"]; shown = g_
        else:
            d = spec["decimals"]
            okv = g_ is not None and round(float(g_), d) == round(float(spec["value"]), d)
            shown = None if g_ is None else (int(round(float(g_), d)) if d <= 0 else round(float(g_), d + 2))
        rep.append((k, spec["value"], shown, "PASS" if okv else "FAIL"))
    npass = sum(r_[3] == "PASS" for r_ in rep)
    md = ["| Quantity | Expected | Reproduced | Result |", "|---|--:|--:|---|"] + [f"| {a_} | {b} | {c_} | {d} |" for a_, b, c_, d in rep]
    (out / "reproduction_report.md").write_text(f"# Reproduction report\n\n{npass}/{len(rep)} numbers reproduced\n\n" + "\n".join(md) + "\n", encoding="utf-8")
    w = max((len(r_[0]) for r_ in rep), default=0)
    for a_, b, c_, d in rep: print(f"{a_.ljust(w)}  {str(b):>14}  {str(c_):>16}  {d}")
    print(f"\n{npass}/{len(rep)} numbers reproduced: {'ALL PASS' if rep and npass == len(rep) else 'FAILURES PRESENT'}")
    sys.exit(0 if rep and npass == len(rep) else 1)


if __name__ == "__main__":
    main()

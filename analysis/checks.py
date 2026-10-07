"""The comparison itself: every number the app reports against its metafor counterpart.

A CHECK is one number the app reports for one meta-analysis, compared with the corresponding metafor value:
  per meta-analysis (they do not depend on the tau^2 estimator):
      k (every study read), Q, df, p-value of Q, I^2, and the Q-profile 95% CIs of tau^2 and I^2  -> 9 checks
  per meta-analysis and tau^2 estimator the app offers (8: PM, REML, ML, EB, SJ, HE, HS, DL):
      refusal: both sides agree whether the estimator is offered                                  -> 1 check
      and, if offered: tau^2, mu, SE, 95% CI (z), 95% HKSJ CI, 95% prediction interval            -> 9 checks
      leave-one-out mu, 95% CI (z) (2 limits), I^2 and tau^2 for each of the k studies            -> 5k checks
      Baujat coordinates (x, y) for each of the k studies                                          -> 2k checks
  So a meta-analysis with k studies gives 9 + 8 + n_offered * (9 + 7k) checks. DerSimonian-Laird with k < 10 is not
  offered by the app (it says so and shows PM): only its refusal check (the numbers then shown are the PM ones, checked
  under PM).
TOLERANCES (typed by kind of quantity):
  REL  |app - metafor| / max(1, |metafor|) <= 1e-9   estimates, SEs, CIs, PIs, tau^2 and its CI, Q, LOO, Baujat
  ABS  |app - metafor| <= 1e-9                       I^2 and its CI (percentage points), p-value of Q
  EXACT                                               df, k, refusal
"""
import math

TOL = {"REL": 1e-9, "ABS": 1e-9, "EXACT": 0.0}
KEYS = ["pm", "reml", "ml", "eb", "sj", "he", "hs", "dl"]
LABEL = {"pm": "PM", "reml": "REML", "ml": "ML", "eb": "EB", "sj": "SJ", "he": "HE", "hs": "HS", "dl": "DL"}


def _d(a, b, kind):
    if a is None or b is None or (isinstance(a, float) and math.isnan(a)) or (isinstance(b, float) and math.isnan(b)):
        return 0.0 if (a is None) == (b is None) else math.inf
    if kind == "REL":
        return abs(a - b) / max(1.0, abs(b))
    return abs(a - b)


def checks(app, ref):
    """Yield (quantity, group, kind, estimator, index, app_value, metafor_value, discrepancy) for one meta-analysis."""
    rc, A0 = ref["common"], app["configs"]["pm"]
    S, Q = A0["sum"], A0["qpci"]
    common = [("k", "structure", "EXACT", A0["k"], rc["k"]), ("Q", "heterogeneity", "REL", S["Q"], rc["Q"]),
              ("df", "structure", "EXACT", S["df"], rc["df"]), ("p(Q)", "p-values", "ABS", S["pQ"], rc["pQ"]),
              ("I2", "heterogeneity", "ABS", S["I2"], rc["I2"]),
              ("tau2 CI lower", "heterogeneity", "REL", Q["tau2Lo"], rc["tau2_lo"]), ("tau2 CI upper", "heterogeneity", "REL", Q["tau2Hi"], rc["tau2_hi"]),
              ("I2 CI lower", "heterogeneity", "ABS", Q["I2Lo"], rc["I2_lo"]), ("I2 CI upper", "heterogeneity", "ABS", Q["I2Hi"], rc["I2_hi"])]
    for q, g, kind, a, b in common:
        yield (q, g, kind, "", -1, a, b, _d(a, b, kind))
    for key in KEYS:
        r, A = ref["configs"][key], app["configs"][key]
        refused_app = bool(A.get("dlRefused"))
        refused_ref = r.get("refused") is True or r.get("refused") == "true"
        yield ("refusal", "structure", "EXACT", key, -1, refused_app, refused_ref, 0.0 if refused_app == refused_ref else math.inf)
        if refused_ref or refused_app or "error" in r:
            continue
        s = A["sum"]
        for q, g, a, b in [("tau2", "heterogeneity", A["tau2"], r["tau2"]), ("mu", "estimates", s["mu"], r["mu"]),
                           ("SE", "estimates", s["se"], r["se"]), ("CI lower (z)", "estimates", s["ciLo"], r["ci_lo"]),
                           ("CI upper (z)", "estimates", s["ciHi"], r["ci_hi"]), ("HKSJ CI lower", "estimates", s["ciLoHKSJ"], r["hk_lo"]),
                           ("HKSJ CI upper", "estimates", s["ciHiHKSJ"], r["hk_hi"]), ("PI lower", "estimates", A["pi"]["lo"], r["pi_lo"]),
                           ("PI upper", "estimates", A["pi"]["hi"], r["pi_hi"])]:
            yield (q, g, "REL", key, -1, a, b, _d(a, b, "REL"))
        for i, l in enumerate(A["loo"]):
            for q, g, kind, a, b in [("LOO mu", "leave-one-out", "REL", l["mu"], r["loo_mu"][i]),
                                     ("LOO CI lower", "leave-one-out", "REL", l["ciLo"], r["loo_ci_lo"][i]),
                                     ("LOO CI upper", "leave-one-out", "REL", l["ciHi"], r["loo_ci_hi"][i]),
                                     ("LOO I2", "leave-one-out", "ABS", l["I2"], r["loo_I2"][i]),
                                     ("LOO tau2", "leave-one-out", "REL", l["tau2"], r["loo_tau2"][i])]:
                yield (q, g, kind, key, i, a, b, _d(a, b, kind))
        for i, bj in enumerate(A["baujat"]):
            for q, a, b in [("Baujat x", bj["x"], r["baujat_x"][i]), ("Baujat y", bj["y"], r["baujat_y"][i])]:
                yield (q, "Baujat", "REL", key, i, a, b, _d(a, b, "REL"))

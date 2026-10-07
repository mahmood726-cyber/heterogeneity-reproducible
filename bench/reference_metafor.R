# metafor reference values for every meta-analysis in the corpus and every tau^2 estimator the app offers.
#   Rscript bench/reference_metafor.R corpus/corpus.csv results/full/reference.jsonl
#
# The app's quantities and their metafor counterparts (same yi; vi = sei^2, the variance the app forms from the SE):
#   tau^2, mu, SE, 95% CI (z)          rma(yi, vi, method = M)
#   HKSJ 95% CI (t, q* floored at 1)   rma(..., method = M, test = "adhoc")
#   95% prediction interval            predict(rma(..., method = M, test = "t"))   [t_{k-1}, unadjusted SE]
#   Q, df, p(Q); I^2 (Q-based)         rma(...)$QE, $k - 1, $QEp; rma(..., method = "DL")$I2
#   tau^2 and I^2 95% CI (Q-profile)   confint(rma(...))
#   leave-one-out mu, CI (z), tau^2    rma(..., method = M) on the other k - 1 studies (= leave1out()); I^2 from its Q
#   Baujat x, y                        baujat(rma(..., method = M)): x = squared Pearson residual,
#                                      y = (mu - mu_(-i))^2 / Var(mu_(-i)) from the leave-one-out refit
# App estimator keys: pm reml ml eb sj he hs dl. The app does not offer DL below k = 10 (it shows PM and says so); for
# those, and for leave-one-out subsets below 10 under DL, the reference is PM, as the app documents.
# Iterative estimators are fitted with tight convergence controls (TIGHT: tau^2 to 1e-12; metafor defaults 1e-5); metafor's default controls are recorded
# separately (tau2_default) so the effect of R's own convergence threshold can be reported.
suppressMessages(library(metafor))
pdf(NULL)   # baujat() draws; send it nowhere
args <- commandArgs(trailingOnly = TRUE)
corpus <- read.csv(args[1], colClasses = c(yi = "character", sei = "character"), stringsAsFactors = FALSE)
corpus$yi <- as.numeric(corpus$yi); corpus$sei <- as.numeric(corpus$sei)
TIGHT <- list(tol = 1e-15, threshold = 1e-12, maxiter = 10000)
KEYS <- c(pm = "PM", reml = "REML", ml = "ML", eb = "EB", sj = "SJ", he = "HE", hs = "HS", dl = "DL")

num <- function(x) if (length(x) == 0 || is.null(x) || is.na(x)) "null" else if (is.infinite(x)) (if (x > 0) "1e999" else "-1e999") else sprintf("%.17g", x)
arr <- function(x) paste0("[", paste(vapply(x, num, ""), collapse = ","), "]")
obj <- function(l) paste0("{", paste(sprintf('"%s":%s', names(l), unlist(l)), collapse = ","), "}")

# metafor's convergence threshold is an ABSOLUTE change in tau^2, so for a small tau^2 (or one at the boundary 0) the
# fit is refined with a threshold scaled to tau^2 (1e-12 x tau^2, floored at 1e-24); if that refit fails to converge the
# first fit is kept.
fit <- function(y, v, m, ...) {
  f <- tryCatch(suppressWarnings(rma(y, v, method = m, control = TIGHT, ...)), error = function(e) e)
  if (!inherits(f, "error") && m %in% c("REML", "ML", "EB") && f$tau2 < 1e-3) {
    thr <- max(1e-24, 1e-12 * f$tau2)
    g <- tryCatch(suppressWarnings(rma(y, v, method = m, control = list(tol = 1e-15, threshold = thr, maxiter = 1e5), ...)), error = function(e) e)
    if (!inherits(g, "error")) f <- g
  }
  f
}

lines <- character(0)
for (id in unique(corpus$analysis)) {
  d <- corpus[corpus$analysis == id, ]
  y <- d$yi; v <- d$sei * d$sei; k <- length(y)
  base <- fit(y, v, "DL")
  # Q-profile CI: metafor searches for the upper bound only up to tau2.max (default 100) and reports that limit when the
  # root lies beyond it; the search is widened to 1e9 (the app's own search limit). The default result is kept as well.
  pmfit <- fit(y, v, "PM")
  ci <- tryCatch(suppressWarnings(confint(pmfit, control = list(tol = 1e-15, maxiter = 100000, tau2.max = 1e9))$random), error = function(e) NULL)
  ci_def <- tryCatch(suppressWarnings(confint(pmfit)$random), error = function(e) NULL)
  common <- list(k = k, Q = num(base$QE), df = num(k - 1), pQ = num(base$QEp), I2 = num(base$I2),
                 tau2_lo = num(if (is.null(ci)) NA else ci["tau^2", "ci.lb"]), tau2_hi = num(if (is.null(ci)) NA else ci["tau^2", "ci.ub"]),
                 I2_lo = num(if (is.null(ci)) NA else ci["I^2(%)", "ci.lb"]), I2_hi = num(if (is.null(ci)) NA else ci["I^2(%)", "ci.ub"]),
                 tau2_hi_default = num(if (is.null(ci_def)) NA else ci_def["tau^2", "ci.ub"]))
  confs <- character(0)
  for (key in names(KEYS)) {
    m <- KEYS[[key]]
    refused <- (key == "dl" && k < 10)
    mm <- if (refused) "PM" else m
    f <- fit(y, v, mm)
    if (inherits(f, "error")) { confs <- c(confs, sprintf('"%s":{"refused":%s,"error":"%s"}', key, tolower(refused), gsub('"', "'", conditionMessage(f)))); next }
    a <- fit(y, v, mm, test = "adhoc"); t <- fit(y, v, mm, test = "t"); p <- predict(t)
    dflt <- tryCatch(suppressWarnings(rma(y, v, method = mm))$tau2, error = function(e) NA)
    # leave-one-out with the estimator the app uses for each subset (PM below k = 10 under DL)
    lm <- if (mm == "DL" && k - 1 < 10) "PM" else mm
    # each study left out in turn: an explicit refit of the remaining studies with fit() (its own convergence rule; metafor's
    # leave1out() would reuse the full fit's controls, which do not suit a subset whose tau^2 is of a different size)
    loo <- lapply(seq_len(k), function(i) fit(y[-i], v[-i], lm))
    g_ <- function(nm) vapply(loo, function(g) if (inherits(g, "error")) NA_real_ else as.numeric(g[[nm]])[1], 0)
    loo_est <- g_("beta"); loo_se <- g_("se"); loo_lo <- g_("ci.lb"); loo_hi <- g_("ci.ub"); loo_t2 <- g_("tau2"); loo_Q <- g_("QE")
    loo_I2 <- ifelse(loo_Q > 0 & k - 2 > 0, pmax(0, 100 * (loo_Q - (k - 2)) / loo_Q), 0)
    bx <- resid(f)^2 / (f$tau2 + v)
    by <- (f$beta[1] - loo_est)^2 / loo_se^2
    # that y is metafor::baujat()'s own definition: checked on one fit (metafor's default controls) by comparing baujat()
    # with leave1out() for k <= 40; the result is recorded, never assumed
    bj_check <- "not run (k < 3 or k > 40)"
    if (lm == mm && k >= 3 && k <= 40) {
      fd <- rma(y, v, method = mm)
      b <- baujat(fd, progbar = FALSE); l <- suppressWarnings(leave1out(fd))
      yy <- (fd$beta[1] - l$estimate)^2 / l$se^2; xx <- resid(fd)^2 / (fd$tau2 + v)
      dx <- max(abs(b$x - xx) / pmax(1, abs(xx))); dy <- max(abs(b$y - yy) / pmax(1, abs(yy)))
      bj_check <- if (any(is.na(c(b$x, b$y, xx, yy)))) "NA in baujat() or leave1out()" else if (dx <= 1e-12 && dy <= 1e-12) "agrees" else sprintf("differs (x %.1e, y %.1e)", dx, dy)
    }
    confs <- c(confs, sprintf('"%s":%s', key, obj(list(
      refused = tolower(refused), method = sprintf('"%s"', mm), tau2 = num(f$tau2), tau2_default = num(dflt),
      mu = num(f$beta[1]), se = num(f$se), ci_lo = num(f$ci.lb), ci_hi = num(f$ci.ub),
      hk_lo = num(a$ci.lb), hk_hi = num(a$ci.ub), pi_lo = num(p$pi.lb), pi_hi = num(p$pi.ub),
      loo_method = sprintf('"%s"', lm), loo_mu = arr(loo_est), loo_se = arr(loo_se), loo_ci_lo = arr(loo_lo),
      loo_ci_hi = arr(loo_hi), loo_tau2 = arr(loo_t2), loo_I2 = arr(loo_I2), baujat_x = arr(bx), baujat_y = arr(by), baujat_check = sprintf('"%s"', bj_check)))))
  }
  lines <- c(lines, sprintf('{"analysis":"%s","common":%s,"configs":{%s}}', id, obj(common), paste(confs, collapse = ",")))
}
writeLines(lines, args[2])
cat("reference: ", length(lines), " meta-analyses x ", length(KEYS), " estimators (metafor ", as.character(packageVersion("metafor")), ")\n", sep = "")

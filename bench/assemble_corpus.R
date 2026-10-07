# Assemble the captured fits (bench/capture_one.R, one .rds per metadat help page) into the validation corpus.
#   Rscript bench/assemble_corpus.R <caps-dir> <out-dir>
# A meta-analysis is one distinct set of (yi, vi) fitted in a page's examples; repeated fits of the same data (another
# estimator, a plot, predict()) count once. Included: k >= 2 studies, every vi finite and > 0 (the app needs a positive
# standard error). Everything else is listed in corpus_log.tsv with its reason.
args <- commandArgs(trailingOnly = TRUE)
caps <- args[1]; out <- args[2]
dir.create(out, showWarnings = FALSE, recursive = TRUE)
runs <- read.delim(file.path(caps, "runs.tsv"), header = FALSE, col.names = c("rd", "run", "seconds"), stringsAsFactors = FALSE)
f17 <- function(x) sprintf("%.17g", x)
rows <- list(); log <- list(); n_an <- 0; seen_global <- character(0); dup_across <- 0
for (i in seq_len(nrow(runs))) {
  rd <- runs$rd[i]; ds <- sub("[.]Rd$", "", rd); f <- file.path(caps, paste0(ds, ".rds"))
  if (!file.exists(f)) { log[[length(log) + 1]] <- c(ds, runs$run[i], "0", "0", "examples did not finish"); next }
  r <- readRDS(f)
  seen <- character(0); inc <- 0; exc <- c()
  for (c in r$caps) {
    key <- paste(f17(c$yi), f17(c$vi), collapse = "|")
    if (key %in% seen) next
    seen <- c(seen, key)
    if (length(c$yi) < 2) { exc <- c(exc, "k=1"); next }
    if (any(!is.finite(c$yi)) || any(!is.finite(c$vi)) || any(c$vi <= 0)) { exc <- c(exc, "non-positive or missing variance"); next }
    if (key %in% seen_global) dup_across <- dup_across + 1
    seen_global <- c(seen_global, key)
    inc <- inc + 1; n_an <- n_an + 1
    id <- sprintf("%s#%d", ds, inc)
    slab <- if (length(c$slab) == length(c$yi)) c$slab else as.character(seq_along(c$yi))
    rows[[length(rows) + 1]] <- data.frame(analysis = id, dataset = ds, measure = ifelse(is.null(c$measure), "", c$measure),
                                           example_method = c$method, k = length(c$yi), study = seq_along(c$yi), slab = slab,
                                           yi = f17(c$yi), sei = f17(sqrt(c$vi)), stringsAsFactors = FALSE)
  }
  log[[length(log) + 1]] <- c(ds, if (r$status == "ERROR") paste("ERROR:", gsub("[\t\n]", " ", r$message)) else r$status,
                              length(r$caps), inc, if (length(exc)) paste(table(exc), names(table(exc)), collapse = "; ") else "")
}
corpus <- do.call(rbind, rows)
write.csv(corpus, file.path(out, "corpus.csv"), row.names = FALSE)
L <- as.data.frame(do.call(rbind, log), stringsAsFactors = FALSE)
names(L) <- c("dataset", "examples", "fits_captured", "meta_analyses_included", "excluded")
L$run <- runs$run[match(paste0(L$dataset, ".Rd"), runs$rd)]
write.table(L, file.path(out, "corpus_log.tsv"), sep = "\t", row.names = FALSE, quote = FALSE)
ks <- tapply(corpus$k, corpus$analysis, `[`, 1)
summ <- sprintf('{"metadat":"%s","metafor":"%s","help_pages":%d,"pages_with_examples_run":%d,"pages_timed_out":%d,"pages_with_errors":%d,"pages_contributing":%d,"meta_analyses":%d,"studies":%d,"k_min":%d,"k_max":%d,"k_median":%g,"duplicates_across_pages":%d}',
                packageVersion("metadat"), packageVersion("metafor"), nrow(runs), sum(L$examples == "OK"),
                sum(runs$run == "TIMEOUT"), sum(grepl("^ERROR", L$examples)), length(unique(corpus$dataset)),
                length(ks), nrow(corpus), min(ks), max(ks), median(ks), dup_across)
writeLines(summ, file.path(out, "corpus_summary.json"))
cat("corpus:", summ, "\n")

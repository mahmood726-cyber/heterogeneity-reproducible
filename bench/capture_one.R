# Run the help-page examples of ONE metadat Rd file with rma()/rma.uni() shadowed, and save every
# intercept-only univariate random/fixed-effects fit it makes (the data the fit actually used).
args <- commandArgs(trailingOnly = TRUE)
nm <- args[1]; outdir <- args[2]
suppressMessages({library(metafor); library(metadat)})
db <- tools::Rd_db("metadat")
caps <- list()
shim <- function(...) {
  # rebuild the call and evaluate it where it was made, so metafor's lookup of yi, vi, ... inside data= still works
  cl <- match.call(); cl[[1]] <- quote(metafor::rma.uni)
  r <- eval(cl, parent.frame())
  if (inherits(r, "rma.uni") && !inherits(r, "rma.mh") && !inherits(r, "rma.peto") && r$p == 1 && isTRUE(r$int.only)) {
    caps[[length(caps) + 1]] <<- list(yi = as.numeric(r$yi), vi = as.numeric(r$vi), k = r$k,
                                     method = r$method, measure = r$measure, slab = as.character(r$slab))
  }
  r
}
ex <- tempfile(fileext = ".R")
tools::Rd2ex(db[[nm]], ex, commentDontrun = FALSE, commentDonttest = FALSE)
status <- "NO_EXAMPLES"; msg <- ""
if (file.exists(ex)) {
  e <- new.env(); assign("rma", shim, e); assign("rma.uni", shim, e)
  status <- tryCatch({ suppressWarnings(suppressMessages(capture.output(sys.source(ex, envir = e)))); "OK" },
                     error = function(err) { msg <<- conditionMessage(err); "ERROR" })
}
saveRDS(list(rd = nm, status = status, message = msg, caps = caps), file.path(outdir, paste0(sub("[.]Rd$", "", nm), ".rds")))

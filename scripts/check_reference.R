# Desktop reference versions must remain the original validation versions.
expected <- c(metafor = "5.2.1", metadat = "1.6.0")
if (as.character(getRversion()) != "4.6.0") stop("R 4.6.0 required for the original validation")
for (name in names(expected)) {
  actual <- as.character(packageVersion(name))
  if (actual != expected[[name]]) stop(sprintf("%s %s found; %s required", name, actual, expected[[name]]))
  cat(name, actual, "\n")
}
cat("REFERENCE VERSIONS: 2/2 package pins; R 4.6.0\n")


# Import zcurve library
library(zcurve)

# Import JATSdecoder library
library(JATSdecoder)

# Set cwd to the folder containing this file
setwd("C:/Users/olefr/OneDrive/Dokumenter/Psykologisk Tidsskrift/Replikasjonsprosjekt")

# Iterate through all immediate subdirectories of ./Papers
paths = list.dirs("./Papers", recursive = FALSE, full.names = TRUE)
paths

results = data.frame(name=character(), ERR = double(), EDR = double(), ARR = double())
# For each subdirectory, get all .cermxml files and compute p-values
lapply(paths, function(x){
  tryCatch(expr = {
    files = list.files(x, pattern="*.cermxml", full.names = TRUE)
    stats = lapply(files, function(x) {get.stats(x, stats.mode="computable", T2t = TRUE, R2r = TRUE, estimateZ = TRUE)})
    errors = data.frame(filename = character(), error=character(), reported_p = double(), real_p = double())
    for (i in seq_along(files)) {
      stat = stats[[i]]$standardStats
      if (length(stat) == 0){
          next;
      }
      apply(stat, 1, function(s) {
          if ((!is.na(s["p"]) && !is.na(s["recalculatedP"])) && (s["p"] <= 0.05 && (s["p_op"] == '<' || s["p_op"] == '=') && s["recalculatedP"] > 0.05)){
              errors[nrow(errors) + 1,] <<- c(files[i], s["result"], s["p"], s["recalculatedP"])
          }
      });
    }
    if (nrow(errors) > 0){
      # Write to file with name of subdirectory in ./Outputs
      write.csv(errors, paste0("./Outputs/", basename(x), ".csv"), row.names = FALSE, quote = c(1,2))
    } 
    stats = stats[lapply(stats, function(x) {length(x$standardStats)}) > 0]
    stats = lapply(stats, function(x) {x$standardStats})
    stats = lapply(stats, function(x) {x$recalculatedP})
    stats = unlist(stats)
    if (length(stats) < 50){
      return()
    }
    fit = zcurve(p = stats)
  
    results[nrow(results)+1, ] <<- c(basename(x), fit$coefficients["ERR"], fit$coefficients["EDR"], (fit$coefficients["ERR"] + fit$coefficients["EDR"])/2)
    # Save plot to file with name of subdirectory in ./Outputs
    png(paste("./Outputs/", basename(x), ".png", sep=""), width = 800, height = 500)

    plot(fit, CI = TRUE, annotation = TRUE, main = basename(x))
    dev.off()
  }, error = function(e) {
    print(e)
  })
})

write.csv(results, "./Outputs/results.csv", row.names = FALSE, quote = c(1))

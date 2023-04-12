
# Import zcurve library
library(zcurve)

# Import JATSdecoder library
library(JATSdecoder)

# Set cwd to the folder containing this file
setwd("C:/Users/olefr/OneDrive/Dokumenter/Psykologisk Tidsskrift/Replikasjonsprosjekt")

# Iterate through all immediate subdirectories of ./Papers where the papers are stored
paths = list.dirs("./Papers", recursive = FALSE, full.names = TRUE)
paths

results = data.frame(name=character(), ERR = double(), EDR = double(), ARR = double())

# For each subdirectory, get all .cermxml files and compute p-values
lapply(paths, function(x){
  tryCatch(expr = {
    files = list.files(x, pattern="*.cermxml", full.names = TRUE)
    # Use JATSdecoder to extract statistical results from the article
    stats = lapply(files, function(x) {get.stats(x, stats.mode="computable", T2t = TRUE, R2r = TRUE, estimateZ = TRUE)})
    errors = data.frame(filename = character(), error=character(), reported_p = double(), real_p = double())
    
    # Go through all the results and see if there are cases where the reported p-value is < 0.05 and the calculated p-value from the test-statistic is > 0.05
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
    
    # If there are any errors: write the errors to a file with name of the author
    if (nrow(errors) > 0){
      write.csv(errors, paste0("./Outputs/", basename(x), ".csv"), row.names = FALSE, quote = c(1,2))
    }
    
    # Filter out all the papers where JATSdecoder couldn't find any statistical results
    stats = stats[lapply(stats, function(x) {length(x$standardStats)}) > 0]
    
    # Join all the p-values from all the papers into a single list
    # Use p-values calculated from the test-statistics as you get an exact p-value, otherwise they are often on the form "p < 0.05" or "p < 0.01", which does not
    # allow for a smooth graph
    stats = lapply(stats, function(x) {x$standardStats})
    stats = lapply(stats, function(x) {x$recalculatedP})
    stats = unlist(stats)
    
    # Drop authors where the number of p-values are less than 50, in order to avoid spurious graphs
    if (length(stats) < 50){
      return()
    }
    
    # Use z-curve library to generate a model based on the p-values
    fit = zcurve(p = stats)
  
    # Store the author's ERR, EDR and ARR
    results[nrow(results)+1, ] <<- c(basename(x), fit$coefficients["ERR"], fit$coefficients["EDR"], (fit$coefficients["ERR"] + fit$coefficients["EDR"])/2)
    
    # Generate and save the z-value plot to file with name of the author in ./Outputs
    png(paste("./Outputs/", basename(x), ".png", sep=""), width = 800, height = 500)
    plot(fit, CI = TRUE, annotation = TRUE, main = basename(x))
    dev.off()
  }, error = function(e) {
    print(e)
  })
})

# Write all the authors' ERR, EDR and ARR to a file
write.csv(results, "./Outputs/results.csv", row.names = FALSE, quote = c(1))

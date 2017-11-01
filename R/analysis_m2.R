# Random Walk
library(stringr)
library(MASS)

N_STEPS <- 500000
earthworm_data <- list()
xRadius <- c()
yPointsClose <- c()
yAverage <- c()
allData <- list()
# This is every file with earthworm format for method 2
files <- list.files('../Data/')[grep("data_for_5000_steps_1_radius_\\d+_M2.csv", list.files('../Data/'))]
for (f in files) {
  # Need to set header to FALSE so we can read the first line
  csvData <- read.csv(paste0("../Data/", f), header = TRUE)
  radius <- str_split(f, "_")[[1]][7]
  allData[[radius]] <- csvData
  
  
  names(csvData) <- c("x", "y", "isFrontier", "close")
  csvData$isFrontier = as.logical(csvData$isFrontier)
  
  yFrontierPointsClose <- csvData$close[csvData$isFrontier]
  
  yPointsClose <- c(yPointsClose, yFrontierPointsClose)
  yAverage <- c(yAverage, mean(yFrontierPointsClose))
  xRadius <- c(xRadius, rep(as.integer(radius), length(yFrontierPointsClose)))
  
  earthworm_data[[radius]] <- csvData
}

logX <- log(xRadius)
logY <- log(yPointsClose) # This creates -Inf values for log(0), we will replace with 0
logY <- replace(logY, logY == -Inf, 0)
allModel <- lm(logY ~ logX)
meanModel <- lm(log(yAverage) ~ log(unique(xRadius)))

#image
# plot(csvData$y~csvData$x, pch='.')
# points(csvData$y[csvData$isFrontier]~csvData$x[csvData$isFrontier], pch='.', col='red')

# All points
# plot(logY ~ logX, ylab = "Surrounding Points", xlab = "Radius Size", main = paste0('In Log Scale, ', allModel$coefficients[2]))
# abline(allModel$coefficients[1], allModel$coefficients[2], col='red')

# Averages for each radius 
plot(log(yAverage) ~ log(unique(xRadius)), ylab = "Average Surrounding Points", xlab = "Radius Size", main = paste0('In Log Scale, ', allModel$coefficients[2]))
abline(meanModel$coefficients[1], meanModel$coefficients[2], col = 'red')

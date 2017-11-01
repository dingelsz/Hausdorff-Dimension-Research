library(stringr)

x <- c()
yFrontier <- c()
yArea <- c()
yDiameter <- c()
for (f in list.files('../Data/')) {
  csvData <- read.csv(paste0("../Data/", f))
  
  # Get the indexes of each _
  underscoreIndexes <- str_locate_all(f, "_")[[1]]
  # The number of steps is inside the 2nd and 3rd _. +1 and -1 to not include the _
  steps = as.integer(substr(f, underscoreIndexes[2] + 1, underscoreIndexes[3] - 1))
  
  
  names(csvData) <- c("x", "y", "isFrontier")
  csvData$isFrontier = as.logical(csvData$isFrontier)
  
  x <- c(x, steps)
  yFrontier <- c(yFrontier, sum(csvData$isFrontier))
  yArea <- c(yArea, length(csvData$x))
  
  width = max(csvData$x) - min(csvData$x)
  height = max(csvData$y) - min(csvData$y)
  yDiameter <- c(yDiameter, sqrt(width^2 + height^2))
}

fFrontier <- lm(log(yFrontier) ~ log(x))
fArea <- lm(log(yArea) ~ log(x))
fDiameter <- lm(log(yDiameter) ~ log(x))

par(mar=c(1,1,1,1))
par(mfrow=c(3,1))

plot(log(yFrontier) ~ log(sqrt(x)), main = 'Logarithmic Number of Frontier Points vs Logarithmic Number of Steps')
abline(fFrontier$coefficients[1], fFrontier$coefficients[2], col='red')

plot(log(yArea) ~ log(sqrt(x)), main = 'Logarithmic Area vs Logarithmic Number of Steps')
abline(fArea$coefficients[1], fArea$coefficients[2], col='red')

plot(log(yDiameter) ~ log(sqrt(x)), main = 'Logarithmic Diameter vs Logarithmic Number of Steps')
abline(fDiameter$coefficients[1], fDiameter$coefficients[2], col='red')

print(paste0("Frontier Coefficient: ", fFrontier$coefficients[2]))
print(paste0("Area Coefficient: ", fArea$coefficients[2]))
print(paste0("Diameter Coefficient: ", fDiameter$coefficients[2]))

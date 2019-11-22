library(ggplot2)

cd.data <- read.csv("~/ReinforcementLearning/WaypointLearning/CoordinateDescentData.csv")
names(cd.data) <- c("step.size", "lr", "Cost", "count.tsocs")

print(ggplot(cd.data, aes(x=lr, y=Cost, col=factor(step.size))) + geom_line())
print(ggplot(cd.data, aes(x=lr, y=count.tsocs, col=factor(step.size))) + geom_line())
library(minet)
filename <- '/home/user/Sirius/MutualInformation_2/experiment.txt'
first <- readLines(filename, n=1)
names <- strsplit(first, '\t')
names <- unlist(names, use.names=FALSE)
d <- read.table(filename, skip=1, col.names = names)

mim <- build.mim(d, estimator = "mi.empirical", disc = "equalfreq")

weight_adjacency_matrix <- minet(mim, method="mrnetb", estimator="mi.empirical", disc="equalfreq")

show(weight_adjacency_matrix)


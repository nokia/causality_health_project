##Aggregted Implementation of PC algorithm using multinomial logistic regression for mixed data

setwd("C:/Users/rideo/OneDrive - Nokia/Code/Exported from python discretized")
Subj_recoded <- read.csv('Discretized_S3.csv')
Subj_recoded$BR <- 1/Subj_recoded$BR
library(dplyr)
library(pcalg)
library(MXM)
library(Rcpp)
Subj_recoded <- select(Subj_recoded, -X)
Subj_recoded <- data.matrix(Subj_recoded)

n <- nrow(Subj_recoded) ## sample size
p <- ncol(Subj_recoded) ## number of variables (or nodes)



g1 <- MXM::pc.skel(Subj_recoded, method = "cat", alpha = 0.01) ## skeleton
g1 <- MXM::pc.or(g1)$G ## orientation rules
MXM::plotnetwork(g1)





# a <- pc.skel(Subj_recoded, method = "pearson", alpha = 0.01, 
# rob = FALSE, R = 1, stat = NULL, ini.pvalue = NULL) 
# a1 <- pcalg::pc(suffStat = list(C = cor(Subj_recoded), n = n), indepTest =
#                   gaussCItest, p = p, alpha = 0.01) ## skeleton and orientation phase
# g2 <- a1@graph
# g2 <- pcalg::wgtMatrix(g2, transpose = FALSE)
# MXM::plotnetwork(2 * a$G)

# k1 <- which( g2 == 1 & t(g2) == 0 )
# k2 <- which( g2 == 0 & t(g2) == 1 )
# g2[k1] <- 2
# g2[k2] <- 3
# colnames(g2) <- rownames(g2) <- colnames(g1)
# MXM::plotnetwork(g2) #This also makes a cyclic graph


##### license 

## Copyright 2021 Nokia

## Licensed under the BSD 3-Clause License

## SPDX-License-Identifier: BSD-3-Clause


##Aggregated & Individual Implementations of PC algorithm using MXM package for discretized data
setwd("C:/Users/rideo/OneDrive - Nokia/Code/Exported from python recoded")
Subj_cont <- read.csv('Full-set-aggregated-recoded.csv')


## Eliminate missing data
Subj_cont <- Subj_cont[complete.cases(Subj_cont), ]

library(dplyr)
library(pcalg)
library(MXM)
library(Rcpp)
Subj_mixed <-  cbind.data.frame(Subj_cont$PEEGd, Subj_cont$PEEGa, Subj_cont$PEEGb, Subj_cont$PEEGs,
                                Subj_cont$PEEGt, Subj_cont$PECG_HF, Subj_cont$PECG_LF,
                                Subj_cont$BR, Subj_cont$BPM, Subj_cont$AUC_Resp, 
                                Subj_cont$SS, Subj_cont$AEI, Subj_cont$HEI, Subj_cont$LEI)
colnames(Subj_mixed) <- c('PEEGd', 'PEEGa', 'PEEGb', 'PEEGs', 'PEEGt',
                          'PECG_HF', 'PECG_LF', 'BR', 'BPM', 'AUC_Resp',
                          'SS', 'AEI', 'HEI','LEI')


## Eliminate missing data
Subj_mixed <- Subj_mixed[complete.cases(Subj_mixed), ]
Subj_mixed <- data.matrix(Subj_mixed)
Subj_mixed <- data.frame(Subj_mixed)

g1 <- MXM::pc.skel(Subj_mixed, method = "comb.mm", alpha = 0.01) ## skeleton
g1 <- MXM::pc.or(g1)$G ## orientation rules
MXM::plotnetwork(g1)



##### license 

## Copyright 2021 Nokia

## Licensed under the BSD 3-Clause License

## SPDX-License-Identifier: BSD-3-Clause


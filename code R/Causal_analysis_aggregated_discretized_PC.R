##Discretized Implementation of PC algorithm on aggregated data
##Use the folder with data from aggregated records 

setwd("C:/Users/rideo/OneDrive - Nokia/Code/Exported from python recoded")
Subj_recoded <- read.csv('Full-set-aggregated-recoded.csv')
Subj_recoded$BR <- 1/Subj_recoded$BR
library(dplyr)
library(pcalg)

Subj_recoded <- select(Subj_recoded, -X)

## Discretizing the BR and BPM columns 
# Based on the histograms of BR and BPM, the discretization levels are as follows
# BR: 0-15 is the range:
  # 0-1:0
  # 1-3:1
  # 4-6:2
  # 7-9:3
  #10-12:4
  #13-15:5
  #16-18:6
library(arules)
BR_discretized =  as.data.frame(cut(Subj_recoded$BR,
                     breaks=c(0,1,3,6,9,12,15,18,Inf),
                     include.lowest=TRUE,
                     labels=c("0","1","2","3","4","5","6","Inf")))

colnames(BR_discretized) <-"BR"

## Discretization levels for BPM are in the following range:
# BPM: 0-2843 is the range:
  # 0-5:0
  # 0-50:1
  # 51-100:2
  # 101-150:3
  # 151-200:4
  # 201-250:5
  # 251-300:6
  # 301-350:7
  # 351-400:8
  # 401-450:9
  # 451-500:10
  # 501-550:11
  # 551-3000:12

BPM_discretized =  as.data.frame(cut(Subj_recoded$BPM,
                                    breaks=c(0,5,50,100,150,200,250,300,350,400,450,500,550,3000,Inf),
                                    include.lowest=TRUE,
                                    labels=c("0","1","2","3","4","5","6","7","8","9","10","11","12", "Inf")))

colnames(BPM_discretized) <-"BPM"

## Create a discretized dataset
data = data.frame(SS = Subj_recoded$SS,
                  AEI = Subj_recoded$AEI,
                  HEI = Subj_recoded$HEI,
                  LEI = Subj_recoded$LEI, 
                  BR = BR_discretized$BR, 
                  BPM = BPM_discretized$BPM)




mat1 = matrix(1, ncol = 6,nrow = 10261)

## Eliminate missing data
data <- data[complete.cases(data), ]


data <- data.matrix(data)
#intdata <- as.integer(data)
tempcor <- data - mat1
suff_stat <- list(dm = tempcor, nlev = c(9,5,4,4,7,13), adaptDF = FALSE)
pc_data <- pc(suff_stat, indepTest = disCItest, 
              labels = colnames(data), alpha = 0.05, 
              fixedGaps = NULL, fixedEdges = NULL,
              NAdelete = TRUE, m.max = Inf,skel.method = "stable", 
              conservative = TRUE,solve.confl = TRUE, 
              verbose = TRUE)
png("Aggregated_discretized_dicsCI.png",width=3.25,height=3.25,units="in",res=1200)
plot(pc_data, main = "")
dev.off()
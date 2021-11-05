
# General description 
The project is dedicated to the for health research about sleep apnea using causal methods. 
The project was part of  AI Health project with summer intern at Nokia Bell labs during summer 2021.

## General motivation for the project

In this project, a healthcare use case was identified for the validation of specific causal inference techniques. 
The identified Sleep Apnea dataset was pre-processed and specific causal inference techniques (Causal discovery and Causal effect estimation) 
were implemented and applied. Preliminary results show promising results by identification of important causal relationships for sleep apnea condition. 
Current research in the field of causal AI was reviewed and limitations of some of the techniques were identified. Future work includes the application of non-linear causal estimation, refutation, and data aggregation (in time-series). The obtained results are then planned to be validated using existing literature and domain expertise. Finally, the methods developed are planned to be transferred to the telecom use case, which also has mixed and time-series datasets.

## General information about the data

The data we used in the project is from open dataset base from Physionet https://physionet.org/content/slpdb/1.0.0/
The MIT-BIH Polysomnographic Database was used in this project. This dataset contains the physiological signals from 16 subjects, collected while the subjects were asleep.
Electroencephalogram (EEG), Electrooculogram (ECG), invasive blood pressure (BP), respiratory wave (Resp) data are available publicly.


# Structure of the repository

The repository contains notebooks, code, report summary and links to datasets.

## Notebooks 

### How to use notebook to preprocess the data 

There is main notebook and corresponding python code for data preprocessing. It contains the code to slice the data used in the project. 

### How to use general folder with notebooks: 
1. first we need to run Jupyter notebook "data slice and categorise"
2. then we need to use methods notebooks, such as "PCMCI", as well as R programs "MXM PC aggregated.R"

### How to run notebook on PCMCI method 
1. loading the data and setting up variable names (they will be considered as separate entities)
2. creating dataframe for the causality analysis using tigramite tools: "dataframe = pp.DataFram"
3. choosing conditional independence test: e.g. cond_ind_test = ParCorr()
4. causality analysis of dataframe: for this one would need to choose tau_max (the time series graph resolves also the time-dependence structure up to some maximum time lag τmax) and  pc alpha parameter often set to 0.2 value, testing this value may be helpful as well
5. printing significant links: based on the value on links with significant parents at different values of alpha 
More examples on PCMCI are shown on https://github.com/jakobrunge/tigramite 


# Contributions
The project was done by the summer intern Ridhi Deo (Purdue University) and co-supervised by Anne Lee, Liubov Tupikina and Armen Aghasaryan (Nokia Bell labs). Authors also are thankful for Daniele Marinazzo 
for sharing his expertise for the project.

## How to contribute?

Feel free to contribute to the repository and create a pull request if you prefer to have an extension of the methods applied to healthcare data.

# License 

Copyright 2021 Nokia

Licensed under the BSD 3-Clause License

SPDX-License-Identifier: BSD-3-Clause


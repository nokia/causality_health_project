# Data preprocessing splitting

# This code is written to split the raw signals from the MIT BIH sleep dataset into 30 second epochs. These epochs are then split further into 4 channels (ECG, BP, EEG and Resp)

from IPython.display import display
import matplotlib.pyplot as plt
import numpy as np
import os
import shutil
import posixpath
import wfdb
import csv
from scipy import signal
import pandas as pd


import mne
from mne.datasets.sleep_physionet.age import fetch_data
from mne.time_frequency import psd_welch
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer

from scipy.signal import welch
import heartpy as hp

# R code calling 
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr

from rpy2.robjects import pandas2ri

import rpy2.robjects as robjects



# Each individual slice/piece can be accessed by using obs1_split[i] where i = 1:240 This pertains to subject 1. Similar sizes are calculated for each subject

fs = 250

obs = wfdb.rdsamp('mit-bih-polysomnographic-database-1.0.0/slp16')

obs = obs[0]

size = len(obs)/(fs*30)

obs_split = np.split(obs,size)

# 240 is derived by dividing the entire record by number of samples in a 30 second period (1800000/(250*30)) - 
# here Fs: 250 and each annotation duration is 30 seconds


## Set this value based on the subject being used
## For example: if I want to extract 5th subject's information then set sub = 5
##(Since python's indexing starts from 0, I added the -1)
sub = 6 - 1;


#Read data files 

apnea_indicators = pd.read_excel('Annotations\processed_apnea_indicators.xlsx')
sleep_stages = pd.read_excel('Annotations\processed_sleep_stages.xlsx')
HA_indicators = pd.read_excel('Annotations\processed_HA_indicators.xlsx')
LA_indicators = pd.read_excel('Annotations\processed_LA_indicators.xlsx')


# Splitting the apnea indicator array of observation 1 into individual annotations
size = len(obs)/(fs*30)
size = int(size)
aei = ["" for i in range(size)]
for i in range (size):
    individual_aei = apnea_indicators.iloc[:,sub]
    aei[i] = individual_aei[i]


# Variables assignment: sleep stages, hei, lei 

ss = ["" for i in range(size)]
for i in range(size):
    individual_ss = sleep_stages.iloc[:,sub]
    ss[i] = individual_ss[i]

hei = ["" for i in range(size)]
for i in range(size):
    individual_hei = HA_indicators.iloc[:,sub]
    hei[i] = individual_hei[i]

lei = ["" for i in range(size)]
for i in range(size):
    individual_lei = LA_indicators.iloc[:,sub]
    lei[i] = individual_lei[i]
    
    
# Code to make a dataframe of ECG, Bp, EEG and resp amplitude data with their corresponding annotations

ECG = {
    'SS': [ss[i] for i in range(size)],
    'Apnea_Indicator' : [aei[i] for i in range (size)],
    'HEI': [hei[i] for i in range(size)],
    'LEI': [lei[i] for i in range(size)],
    'ECG_amps': [obs_split[i][:,0] for i in range (size)] #obs_split[i][:,0] corresponds to ECG data.
    # if we change [:,0] to [:,1] then it corresponds to BP. [:,2] for EEG and [:,3] for Resp
}
ECG = pd.DataFrame(ECG, columns = ['SS','Apnea_Indicator','HEI','LEI','ECG_amps'])
print('created ECG dataframe') #print(ECG)

BP = {
    'SS': [ss[i] for i in range(size)],
    'Apnea_Indicator' : [aei[i] for i in range (size)],
    'HEI': [hei[i] for i in range(size)],
    'LEI': [lei[i] for i in range(size)],
    'BP_amps': [obs_split[i][:,1] for i in range (size)] #obs1_split[i][:,0] corresponds to ECG data.
    # if we change [:,0] to [:,1] then it corresponds to BP. [:,2] for EEG and [:,3] for Resp
}
BP = pd.DataFrame(BP, columns = ['SS','Apnea_Indicator','HEI','LEI','BP_amps'])
print(BP)

Resp = {
    'SS': [ss[i] for i in range(size)],
    'Apnea_Indicator' : [aei[i] for i in range (size)],
    'HEI': [hei[i] for i in range(size)],
    'LEI': [lei[i] for i in range(size)],
    'Resp_amps': [obs_split[i][:,3] for i in range (size)] #obs1_split[i][:,0] corresponds to ECG data.
    # if we change [:,0] to [:,1] then it corresponds to BP. [:,2] for EEG and [:,3] for Resp
}
Resp = pd.DataFrame(Resp, columns = ['SS','Apnea_Indicator','HEI','LEI','Resp_amps'])
print(Resp)


#Extracting sub-band EEG power

# Sort the strings and remove whitespace 
#sort_var1 = ''.join(sorted(var1)).strip()
#sort_var2 = ''.join(sorted(var2)).strip()

# specific frequency bands - referred from Danielle and Faes (2014)

bands = {"delta": [0.5, 3],

                  "theta": [3, 8],

                  "alpha": [8, 12],

                  "sigma": [12, 16],

                  "beta": [16, 25]}

PEEG = np.zeros([size,5],float)

from scipy.signal import welch

for j in range(size):

    temp = EEG.EEG_amps[j]

    f, psd = welch(temp, fs=250,nperseg=7500,noverlap=1875) #30% overelap - similar to Danielle and Faes (2014)

    psd /= np.sum(psd, axis=-1, keepdims=True) #Normalizing the PSD

    i = 0

    psds_band = np.zeros(5,float) #Initiating an empty array to contain the power for each band

    for fmin, fmax in bands.values():

            psds_band[i] = psd[(f >= fmin) & (f < fmax)].mean(axis=-1)

            PEEG[j,i] = psds_band[i]

            i = i+1

#saving PEEG of different subbands 
PEEGd = PEEG[:,0]
PEEGt = PEEG[:,1]
PEEGa = PEEG[:,2]
PEEGs = PEEG[:,3]

ECG Feature extraction - incomplete




# Specific frequency bands - referred from Danielle and Faes (2014)

ECG_bands = {"HF": [0.15, 0.4],
                  "LF": [0.04,0.4]
        }

PECG = np.zeros([size,2],float)

for j in range(size):
    temp = ECG.ECG_amps[j]
    f, psd = welch(temp, fs=250,nperseg=7500,noverlap=1875) #50% overelap - similar to Danielle and Faes (2014)
    psd /= np.sum(psd, axis=-1, keepdims=True) #Normalizing the PSD
    i = 0
    ECG_psds_band = np.zeros(2,float) #Initiating an empty array to contain the power for each band
    for fmin, fmax in ECG_bands.values():
            ECG_psds_band[i] = psd[(f >= fmin) & (f < fmax)].mean(axis=-1)
            PECG[j,i] = ECG_psds_band[i]
            i = i+1
            
PECG_HF = PECG[:,0]

PECG_LF = PECG[:,1]

np.shape(PECG_HF)



'''
Breathing rate and BPM detection using ECG
additional measurements can also be computed using this package (heartpy) , if needed
'''



BR = np.zeros(size,'float')

BPM = np.zeros(size,'float')

for j in range(size):

    data = ECG.ECG_amps[j]

    fs = 250

    working_data, measures = hp.process(data, fs)

    BR[j] = measures['breathingrate']

    BPM[j] = measures['bpm']
            
'''
Computing AUC respiration
'''


# Using the trapezoidal rule np.trapz
#x = [i+1 for i in range(7500)] - checked it, the AUC with or without x is the same

AUC = np.zeros(size,'float')

for i in range(size):

    AUC[i] = np.trapz(Resp['Resp_amps'][i])

    
'''
Splitting each of the annotation string into corresponding 30 second bits
'''

ss_split = [0 for i in range(size)]

for i in range (size):

    temp = str(ss[i])

    ss_split[i] = str.split(temp)

aei_split = [0 for i in range(size)]

for i in range (size):

    temp = str(aei[i])

    aei_split[i] = str.split(temp)
    
    
hei_split = [0 for i in range(size)]

for i in range (size):

    temp = str(hei[i])

    hei_split[i] = str.split(temp)

lei_split = [0 for i in range(size)]

for i in range (size):

    temp = str(lei[i])

    lei_split[i] = str.split(temp)

SS = pd.DataFrame(columns=['SS'], data=ss_split)
AEI = pd.DataFrame(columns=['AEI'], data=aei_split)
HEI = pd.DataFrame(columns=['HEI'], data=hei_split)
LEI = pd.DataFrame(columns=['LEI'], data=lei_split)
AUC = pd.DataFrame(columns=['AUC'], data = AUC)


Integrating all the extracted features into a pandas df for easy access

### Change Subj1 to appropriate value

Subj = {

    'SS' : SS['SS'],

    'AEI' : AEI['AEI'],

    'HEI' : HEI['HEI'],

    'LEI' : LEI['LEI'],

    'PEEGd': PEEGd, 

    'PEEGt': PEEGt,

    'PEEGa': PEEGa,

    'PEEGs': PEEGs,

    'PEEGb': PEEGb,

    'PECG_HF': PECG_HF,

    'PECG_LF': PECG_LF,

    'BR': BR,

    'BPM': BPM,

    'AUC_Resp':AUC['AUC']

}

Subj = pd.DataFrame(Subj, columns = ['SS','AEI','HEI','LEI','PEEGd','PEEGt','PEEGa','PEEGs','PEEGb','PECG_HF','PECG_LF','BR','BPM','AUC_Resp'])

print(Subj)

%store subj


'''
R code
'''

pandas2ri.activate()
base = importr('base')

# call an R function on a Pandas DataFrame
base.summary(Subj)



## get a reference to the R function 

write_csv = robjects.r('write.csv')

## save 

write_csv(Subj,'ExportedS6.csv')
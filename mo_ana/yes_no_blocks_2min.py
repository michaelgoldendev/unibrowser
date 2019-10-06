#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 18:37:31 2019

@author: mo
"""

import numpy as np
from scipy.signal import butter, sosfilt, iirnotch, welch, lfilter
import matplotlib.pyplot as plt
from scipy.signal import freqz
import time
from sklearn.cross_decomposition import CCA
from sklearn import metrics

freq = 250
freqlist = [8,14]
names = "data/data_yes8.0Hz_no14.0Hz_06-Oct-2019.19h29m29s602328.csv"

EEG = np.loadtxt(names, delimiter=",")

# %%

no_nonsense_EEG = EEG[120*250:,:]


yes_EEG_list = []
no_EEG_list = []

for i in range(3):
    yes_EEG_list.append(no_nonsense_EEG[:10*250,:])
    no_nonsense_EEG = no_nonsense_EEG[10*250:,:]
    
    no_EEG_list.append(no_nonsense_EEG[:10*250,:])
    no_nonsense_EEG = no_nonsense_EEG[10*250:,:]
    
# %% filtering

coi = np.arange(8)
lcoi = len(coi)

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    sos = butter(order, [low, high], btype='band',output='sos')
    return sos

lowcut = 5
highcut = 30

def filter_and_cut_EGG_signal(EEG):
    
    sos = butter_bandpass(lowcut, highcut, freq, order=15)
    a,b = iirnotch(50.0,30,freq)
    filteredEEG = EEG
    
    for i in range(lcoi):
        filteredEEG[:,i] = sosfilt(sos, EEG[:,i])
        filteredEEG[:,i] = lfilter(b, a, filteredEEG[:,i])
    
    # filteredEEG = filteredEEG[30*freq:,:]  
    
    return filteredEEG

filteredyesEEG = []
filterednoEEG = []

for E in no_EEG_list:
    filterednoEEG.append(filter_and_cut_EGG_signal(E))
    
for E in yes_EEG_list:
    filteredyesEEG.append(filter_and_cut_EGG_signal(E))
    
# %% CCA approach

def freq_basis(f, sr, T):
    # T is length of time interval, sr is sample freuqency
    time = np.linspace(0,T,T*sr)
    
    for i in range(1,5):
        if i == 1:
            Y =  np.vstack([np.sin(2*np.pi*f*time*i), np.cos(2*np.pi*f*time*i)])
        else:
            Y = np.vstack([Y, np.sin(2*np.pi*f*time*i), np.cos(2*np.pi*f*time*i)])
            
    return Y.transpose()

cca = CCA(n_components=1)
scores = np.zeros((6,2))
T = int(len(filterednoEEG[0])/freq)

# X : array-like, shape = [n_samples, n_features]
# Y : array-like, shape = [n_samples, n_targets]

for t in range(3):
    for f in range(len(freqlist)):
        X = filterednoEEG[t]
        Y = freq_basis(freqlist[f], freq, T)
        cca.fit(X, Y)
        scores[t, f] = metrics.r2_score(Y,cca.predict(X))#cca.score(X,Y)
        
        X = filteredyesEEG[t]
        Y = freq_basis(freqlist[f], freq, T)
        cca.fit(X, Y)
        scores[t + 3,f] = metrics.r2_score(Y,cca.predict(X))#cca.score(X,Y)
        
fig, ax = plt.subplots(1, 1, figsize=(12, 4))
plt.imshow(scores)
plt.colorbar()
    

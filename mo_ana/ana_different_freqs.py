#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 17:05:31 2019

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
freqlist = [5,8,13,15,17,19]
names = ["data/data_yes5.0Hz_no8.0Hz_06-Oct-2019.17h59m00s677198.csv",\
         "data/data_yes8.0Hz_no14.0Hz_06-Oct-2019.18h07m35s853176.csv",\
         "data/data_yes13.0Hz_no14.0Hz_06-Oct-2019.18h10m20s513759.csv",\
         "data/data_yes15.0Hz_no14.0Hz_06-Oct-2019.18h49m08s711330.csv",\
         "data/data_yes17.0Hz_no14.0Hz_06-Oct-2019.18h51m33s744422.csv",\
         "data/data_yes19.0Hz_no14.0Hz_06-Oct-2019.18h55m07s088066.csv"]

# %% load data

EEG = []
for s in names:
    EEG.append(np.loadtxt(s, delimiter=","))

# %% filtering

coi = np.arange(8)
lcoi = len(coi)

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    sos = butter(order, [low, high], btype='band',output='sos')
    return sos

lowcut = 4
highcut = 20

def filter_and_cut_EGG_signal(EEG):
    
    sos = butter_bandpass(lowcut, highcut, freq, order=9)
    a,b = iirnotch(50.0,30,freq)
    filteredEEG = EEG[30*freq:,coi]
    
    for i in range(lcoi):
        filteredEEG[:,i] = sosfilt(sos, EEG[30*freq:,i])
        filteredEEG[:,i] = lfilter(b, a, filteredEEG[:,i])
    
    # filteredEEG = filteredEEG[30*freq:,:]  
    
    return filteredEEG

filteredEEG = []

for E in EEG:
    filteredEEG.append(filter_and_cut_EGG_signal(E))
    
# %% plot time series before filter 
    
for E in EEG:
    fig, ax = plt.subplots(1, figsize=(12, 4))
    plt.plot(E)
    
# %% plot time series before filter 
    
for fE in filteredEEG:
    fig, ax = plt.subplots(1, figsize=(12, 4))
    plt.plot(fE)
    
# %% plot power spec  

for fE in filteredEEG:
    fig, ax = plt.subplots(1, 1, figsize=(12, 4))   
    for i in range(lcoi):
        freqs, psd = welch(fE[:,i], freq, nperseg=freq*4)
        plt.plot(freqs, psd, lw=2,label=str(coi[i]))
        plt.xlim(left=0, right=20)
    
# %% CCA approach

def freq_basis(f, sr, T):
    # T is length of time interval, sr is sample freuqency
    time = np.linspace(0,T,T*sr)
    
    for i in range(1,4):
        if i == 1:
            Y =  np.vstack([np.sin(2*np.pi*f*time*i), np.cos(2*np.pi*f*time*i)])
        else:
            Y = np.vstack([Y, np.sin(2*np.pi*f*time*i), np.cos(2*np.pi*f*time*i)])
            
    return Y.transpose()

cca = CCA(n_components=1)
scores = np.zeros((len(filteredEEG),len(freqlist)))
T = int(len(filteredEEG[fE])/freq)

# X : array-like, shape = [n_samples, n_features]
# Y : array-like, shape = [n_samples, n_targets]

for fE in range(len(filteredEEG)):
    for f in range(len(freqlist)):
        X = filteredEEG[fE]
        Y = freq_basis(freqlist[f], freq, T)
        cca.fit(X, Y)
        scores[f, fE] = metrics.r2_score(Y,cca.predict(X))#cca.score(X,Y)
        
fig, ax = plt.subplots(1, 1, figsize=(12, 4))
plt.imshow((scores -np.mean(scores,1)) / np.std(scores,1))
plt.colorbar()
        

#print(np.argmax(scores) + 1)
#print(scores)
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
freqlist = [5,8]

coi = np.hstack([np.arange(2), np.arange(3,8)])
lcoi = len(coi)

# %% no
#names = ["data/data_focus-no_yes5.0Hz_no8.0Hz_15.0seconds_06-Oct-2019.20h38m17s301025.csv",\
#         "data/data_focus-no_yes8.0Hz_no5.0Hz_15.0seconds_06-Oct-2019.20h36m48s136905.csv",\
#         "data/data_focus-yes_yes5.0Hz_no8.0Hz_15.0seconds_06-Oct-2019.20h37m56s187425.csv",\
#         "data/data_focus-yes_yes8.0Hz_no5.0Hz_15.0seconds_06-Oct-2019.20h35m59s789908.csv"]

#names = ["data/data_focus-yes_yes8.0Hz_no5.0Hz_15.0seconds_06-Oct-2019.21h18m07s527917.csv",\
#         "data/data_focus-yes_yes5.0Hz_no8.0Hz_15.0seconds_06-Oct-2019.21h16m41s051363.csv",\
#         "data/data_focus-no_yes8.0Hz_no5.0Hz_15.0seconds_06-Oct-2019.21h18m32s870917.csv",\
#         "data/data_focus-no_yes5.0Hz_no8.0Hz_15.0seconds_06-Oct-2019.21h17m23s077029.csv"]

names = ["data/data_focus-yes_yes8.0Hz_no5.0Hz_15.0seconds_06-Oct-2019.21h38m32s019759.csv",\
         "data/data_focus-yes_yes8.0Hz_no5.0Hz_15.0seconds_06-Oct-2019.21h35m53s417367.csv",\
         "data/data_focus-yes_yes5.0Hz_no8.0Hz_15.0seconds_06-Oct-2019.21h39m37s155413.csv",\
         "data/data_focus-yes_yes5.0Hz_no8.0Hz_15.0seconds_06-Oct-2019.21h36m57s816745.csv",\
         "data/data_focus-no_yes8.0Hz_no5.0Hz_15.0seconds_06-Oct-2019.21h39m02s131899.csv",\
         "data/data_focus-no_yes8.0Hz_no5.0Hz_15.0seconds_06-Oct-2019.21h36m22s510052.csv",\
         "data/data_focus-no_yes5.0Hz_no8.0Hz_15.0seconds_06-Oct-2019.21h40m04s170801.csv",\
         "data/data_focus-no_yes5.0Hz_no8.0Hz_15.0seconds_06-Oct-2019.21h37m28s339114.csv"]

targets = np.array([8, 8, 5, 5, 5, 5, 8, 8]);
targetsidx = np.array([1,1,0,0,0,0,1,1]);

EEG = []
for s in names:
    E = np.loadtxt(s, delimiter=",")
    E = E[1:,coi]
    E = E - np.mean(E,0).reshape(1,-1) 
    E = E - np.mean(E,1).reshape(-1,1)
    EEG.append(E)    
    
# %% plot time series before filter 
    
for E in EEG:
    fig, ax = plt.subplots(1, figsize=(12, 4))
    plt.plot(E)

# %%

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    sos = butter(order, [low, high], btype='band',output='sos')
    return sos

lowcut = 4
highcut = 30

def filter_and_cut_EGG_signal(EEG):
    
    sos = butter_bandpass(lowcut, highcut, freq, order=15)
    a,b = iirnotch(50.0,30,freq)
    filteredEEG = EEG - 0.
    
    for i in range(lcoi):
        filteredEEG[:,i] = sosfilt(sos, EEG[:,i])
        filteredEEG[:,i] = lfilter(b, a, filteredEEG[:,i])
    
    # filteredEEG = filteredEEG[30*freq:,:]  
    
    return filteredEEG

filteredEEG = []

for E in EEG:
    filteredEEG.append(filter_and_cut_EGG_signal(E))
    
    
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
        plt.legend()
        
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
scores = np.zeros((len(filteredEEG),2))
T = int(len(filteredEEG[0])/freq)

# X : array-like, shape = [n_samples, n_features]
# Y : array-like, shape = [n_samples, n_targets]

Yl = []
for f in range(len(freqlist)):
    Yl.append(freq_basis(freqlist[f], freq, T))

for t in range(len(filteredEEG)):
    for f in range(len(freqlist)):
        cca.fit(filteredEEG[t], Yl[f])
        scores[t, f] = metrics.r2_score(Yl[f],cca.predict(filteredEEG[t]))#cca.score(X,Y)
        
fig, ax = plt.subplots()
# plt.imshow(scores - np.mean(scores,1).reshape(1,-1).transpose())
plt.imshow(scores)
plt.scatter(targetsidx, np.arange(0,len(filteredEEG)), color='b')
plt.colorbar()
    
print(targetsidx)
print(np.argmax(scores,1))

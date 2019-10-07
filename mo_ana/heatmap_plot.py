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

fr = 250
freqlist = [100, 6,10,15]

# coi = np.hstack([np.arange(2), np.arange(3,7)])
coi = np.arange(8)
lcoi = len(coi)

# %% no

#names = ["no_stim.csv",\
#         "no_stim3.csv",\
#         "stim6_2.csv",\
#         "stim10_2.csv",\
#         "stim15_2.csv"]

#names = ["no_stim.csv",\
#        "no_stim2.csv",\
#        "stim6.csv",\
#        "stim10.csv",\
#        "stim15.csv"]

names = ["no_stim.csv",\
         "no_stim2.csv",\
         "no_stim3.csv",\
         "stim6.csv",\
         "stim6_2.csv",\
         "stim10.csv",\
         "stim10_2.csv",\
         "stim15_2.csv",\
         "stim15.csv"]

EEG = []
for s in names:
    E = np.loadtxt(s, delimiter=",", skiprows=1)
    E = E[1:4000,coi]
    #E = E - np.mean(E,0).reshape(1,-1) 
    #E = E - np.mean(E,1).reshape(-1,1)
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

def filter_and_cut_EGG_signal(EEG):
    
    sos = butter_bandpass(lowcut, highcut, freq, order=15)
    a,b = iirnotch(50.0,30,freq)
    filteredEEG = EEG - 0.
    
    for i in range(lcoi):
        filteredEEG[:,i] = sosfilt(sos, EEG[:,i])
        filteredEEG[:,i] = lfilter(b, a, filteredEEG[:,i])
    
    # filteredEEG = filteredEEG[30*freq:,:]  
    
    return filteredEEG

lowcut = 4
highcut = 40

filteredEEG = []

for E in EEG:
    filteredEEG.append(filter_and_cut_EGG_signal(E))
    
    
# %% plot time series before filter 
    
for fE in filteredEEG:
    fig, ax = plt.subplots(1, figsize=(12, 4))
    plt.plot(fE)
    
# %% plot power spec  
fig, ax = plt.subplots(len(filteredEEG),1) 
for j in range(len(filteredEEG)):
    
    for i in range(lcoi):
        
        fE = filteredEEG[j]
        freqs, psd = welch(fE[:,i], freq, nperseg=freq*4)
        ax[j].plot(freqs, psd, lw=2,label=str(coi[i]))
        ax[j].set_xlim(left=0, right=30)
        ax[j].set_ylim(bottom=0, top=30)
        # plt.xlim(left=0, right=30)
        plt.legend()
        
        
# %% plot power spec  
fig, ax = plt.subplots(len(filteredEEG),1) 
for j in range(len(filteredEEG)):
    
    #mean_lcoi = np.mean
    freqs, psd = welch(fE[:,0], freq, nperseg=freq*4) 
    freqm = psd + 0.
    for i in range(1, lcoi):
        fE = filteredEEG[j]
        freqs, psd = welch(fE[:,i], freq, nperseg=freq*4)
        freqm = freqm + psd
        # plt.xlim(left=0, right=30)
    ax[j].plot(freqs, psd, lw=2,label=str(coi[i]))
    ax[j].set_xlim(left=0, right=30)
    # ax[j].set_ylim(bottom=0, top=40)
        
# %% cut off first couple seconds
    
for fE in filteredEEG:
    fE = fE[100:,:]
        
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
scores = np.zeros((len(filteredEEG),len(freqlist)))
T = len(filteredEEG[0])/fr

# X : array-like, shape = [n_samples, n_features]
# Y : array-like, shape = [n_samples, n_targets]

Yl = []
for f in range(len(freqlist)):
    Yl.append(freq_basis(freqlist[f], fr, T))

for t in range(len(filteredEEG)):
    for f in range(len(freqlist)):
        cca.fit(filteredEEG[t], Yl[f])
        scores[t, f] = metrics.r2_score(Yl[f],cca.predict(filteredEEG[t]))
        
fig, ax = plt.subplots()
# plt.imshow(scores - np.mean(scores,1).reshape(1,-1).transpose())
plt.imshow(scores)
plt.scatter(targetsidx, np.arange(0,len(filteredEEG)), color='b')
plt.colorbar()
    
print(targetsidx)
print(np.argmax(scores,1))

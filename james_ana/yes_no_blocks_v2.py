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
import os

freqlist = [6,10,15]
freq = 250
lowcut = 1
highcut = 30
coi = np.arange(8)
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

#names = ["data_focus-no_yes5.0Hz_no12.0Hz_15.0seconds_06-Oct-2019.21h48m50s451534.csv",\
#         "data_focus-no_yes5.0Hz_no12.0Hz_15.0seconds_06-Oct-2019.21h49m50s067700.csv",\
#         "data_focus-no_yes12.0Hz_no5.0Hz_15.0seconds_06-Oct-2019.21h50m48s928173.csv",\
#         "data_focus-no_yes12.0Hz_no5.0Hz_15.0seconds_06-Oct-2019.21h51m34s971764.csv",\
#         "data_focus-yes_yes5.0Hz_no12.0Hz_15.0seconds_06-Oct-2019.21h48m26s609510.csv",\
#         "data_focus-yes_yes5.0Hz_no12.0Hz_15.0seconds_06-Oct-2019.21h49m24s415637.csv",\
#         "data_focus-yes_yes12.0Hz_no5.0Hz_15.0seconds_06-Oct-2019.21h50m26s364628.csv",\
#         "data_focus-yes_yes12.0Hz_no5.0Hz_15.0seconds_06-Oct-2019.21h51m11s695088.csv"]

names = ['no_stim.csv','no_stim2.csv','stim6.csv','stim6_2.csv','stim10.csv','stim10_2.csv','stim15.csv','stim15_2.csv']

#targets = np.array([12, 12, 5, 5, 5, 5, 12, 12]);
#targetsidx = np.array([1,1,0,0,0,0,1,1]);

targets = np.array([1,1,6,6,10,10,15,15]);
targetsidx = np.array([0,0,0,0,1,1,2,2]);

EEG = []
for s in names:
    E = np.loadtxt('C:/Users/Vilsnk/3D Objects/unibrowser/src/data/'+s, delimiter=",",skiprows=1)
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

def filter_and_cut_EGG_signal(EEG):
    
    sos = butter_bandpass(lowcut, highcut, freq, order=15)
    a,b = iirnotch(50.0,30,freq)
    filteredEEG = np.zeros(EEG.shape)
    
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
EEGspectras = []
freqs, psd = welch(filteredEEG[0][:,0], freq, nperseg=freq*4)
for fE in filteredEEG:
    fig, ax = plt.subplots(1, 1, figsize=(12, 4))  
    EEGspectra = np.zeros((len(psd),filteredEEG[0].shape[1]))
    for i in range(lcoi):
        freqs, EEGspectra[:,i] = welch(fE[:,i], freq, nperseg=freq*4)
        plt.plot(freqs, psd, lw=2,label=str(coi[i]))
        plt.xlim(left=0, right=20)
    EEGspectras.append(EEGspectra)
        
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

def freq_basis_emp(filteredEEG,f):
    Y = np.zeros((EEGspectras[0].shape[0],EEGspectras[0].shape[1]))        
    for i in range(len(EEGspectras)):
        if targets[i]==f:
            print(targets[i],i)
            for j in range(EEGspectras[0].shape[1]):
                Y[:,j] += EEGspectras[i][:,j]
    return Y

#cca = CCA(n_components=1)
#scores = np.zeros((len(filteredEEG),2))
#T = int(len(filteredEEG[0])/freq)
#
## X : array-like, shape = [n_samples, n_features]
## Y : array-like, shape = [n_samples, n_targets]
#
#Yl = []
#for f in range(len(freqlist)):
#    Yl.append(freq_basis(freqlist[f], freq, T))
#
#for t in range(len(filteredEEG)):
#    for f in range(len(freqlist)):
#        cca.fit(filteredEEG[t], Yl[f])
#        scores[t, f] = metrics.r2_score(Y,cca.predict(X))#cca.score(X,Y)
    
cca = CCA(n_components=1)
scores = np.zeros((len(filteredEEG),len(freqlist)))
T = int(len(filteredEEG[0])/freq)

# X : array-like, shape = [n_samples, n_features]
# Y : array-like, shape = [n_samples, n_targets]

Yl = []
for f in range(len(freqlist)):
    Yl.append(freq_basis_emp(EEGspectras,freqlist[f]))

for t in range(len(filteredEEG)):
    for f in range(len(freqlist)):
        cca.fit(EEGspectras[t], Yl[f])
        scores[t, f] = metrics.r2_score(Yl[f],cca.predict(EEGspectras[t]))#cca.score(X,Y)
        
fig, ax = plt.subplots()
# plt.imshow(scores - np.mean(scores,1).reshape(1,-1).transpose())
plt.imshow(scores)
plt.scatter(targetsidx, np.arange(0,len(filteredEEG)), color='b')
plt.colorbar()
    
print(targetsidx)
print(np.argmax(scores,1))
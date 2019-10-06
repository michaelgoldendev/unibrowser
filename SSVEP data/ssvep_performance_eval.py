#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 18:26:53 2019

@author: mo

Taken from https://figshare.com/articles/MAMEM_EEG_...
SSVEP_Dataset_III_14_channels_11_subjects_5_frequencies_presented_simultaneously_/3413851/1
"""

import scipy.io
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
from sklearn.cross_decomposition import CCA
from sklearn import metrics

# %% set params

sf = 128 # Hz
offset = int(0.1*128) # timesteps
nh = 5 # number of harmonics to include
freqs = np.array([12.00, 10.00, 8.57, 7.50, 6.66]) # stim freqs used
target = np.array([4, 2, 3, 5, 1, 2, 5, 4, 2, 3, 1, 5, 4, 3, 2, 4, 1, 2, 5, 3, 4, 1, 3, 1, 3])
sessions = ['a', 'b', 'c', 'd', 'e'] # session names
# %% CCA approach

for sub in range(1,12):
    print('Sub %i' % sub)
    for session in sessions:
        
        cca = CCA(n_components=1)
        
        if sub < 10:
            s = '/Users/mo/Collaborations/unibrowser/SSVEP data/data/EEG-SSVEP-Experiment3/U00'
        else:
            s = '/Users/mo/Collaborations/unibrowser/SSVEP data/data/EEG-SSVEP-Experiment3/U0'
        s =  s + str(sub) + session + 'i.mat'
        
        scores1 = np.ones((12,5))
        mat = scipy.io.loadmat(s)
        events = mat['events']
        timesinit = events[events[:,1] ==  32779,2]
        timesterm = events[events[:,1] ==  32780,2]
        eeg = mat['eeg']
        
        for trial in range(12):
            for f in range(5):
                X = eeg[:, (timesinit[trial] + offset):(timesterm[trial] + offset)].transpose()
                Y = freq_basis(freqs[f], sf, X.shape[0]/sf, nh)
                cca.fit(X, Y)
                scores1[trial, f] = metrics.r2_score(Y,cca.predict(X))#cca.score(X,Y)
                
        if sub < 10:
            s = '/Users/mo/Collaborations/unibrowser/SSVEP data/data/EEG-SSVEP-Experiment3/U00'
        else:
            s = '/Users/mo/Collaborations/unibrowser/SSVEP data/data/EEG-SSVEP-Experiment3/U0'
        s =  s + str(sub) + session + 'ii.mat'
        
        scores2 = np.ones((13,5))
        mat = scipy.io.loadmat(s)
        events = mat['events']
        timesinit = events[events[:,1] ==  32779,2]
        timesterm = events[events[:,1] ==  32780,2]
        eeg = mat['eeg']
        
        for trial in range(13):
            for f in range(5):
                X = eeg[:, (timesinit[trial] + offset):(timesterm[trial] + offset)].transpose()
                Y = freq_basis(freqs[f], sf, X.shape[0]/sf, nh)
                cca.fit(X, Y)
                scores2[trial, f] = metrics.r2_score(Y,cca.predict(X))#cca.score(X,Y)
                            
        scores = np.vstack([scores1, scores2])
        print(np.mean(np.equal(target, np.argmax(scores,1)+1)))
        # print(np.argmax(scores,1) + 1)
        # print(labels)

# %%

def freq_basis(f, sf, T, nh):
    
    # T is length of time interval, sr is sample freuqency
    time = np.linspace(0,T,T*sf)
    
    for i in range(1,nh):
        if i == 1:
            Y =  np.vstack([np.sin(2*np.pi*f*time*i), np.cos(2*np.pi*f*time*i)])
        else:
            Y = np.vstack([Y, np.sin(2*np.pi*f*time*i), np.cos(2*np.pi*f*time*i)])
    
    return Y.transpose()

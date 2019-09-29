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

# load data
s = '/Users/mo/Collaborations/unibrowser/SSVEP data/data/EEG-SSVEP-Experiment3/U002ai.mat'
mat = scipy.io.loadmat(s)

events = mat['events']
eeg = mat['eeg']

sr = 128 # Hz

# %% plot overview

time = np.arange(0,eeg.shape[1])/sr

fig, ax = plt.subplots(1, 1, figsize=(12, 4))
plt.plot(time, eeg[2,:]/100, lw=1.5, color='k')
eegfiltered = butter_bandpass_filter(eeg[2,:]/100, 3, 40, 128, order=5)
plt.plot(time, eegfiltered, lw=1.5, color='b')



# 32779 = trial initiation
# 32780 = trial termination

timesinit = events[events[:,1] ==  32779,2]
plt.scatter(time[timesinit], np.ones(timesinit.shape))
timesterm = events[events[:,1] ==  32780,2]
plt.scatter(time[timesterm], np.ones(timesterm.shape), color='r')

# %% cut and powerspec

labels = np.array([4, 2, 3, 5, 1, 2, 5, 4, 2, 3, 1, 5])
freq_targets = np.array([12.00, 10.00, 8.57, 7.50, 6.66])
trial = 5

# Define window length (4 seconds)
win = 16 * sr

# Plot the power spectrum
fig, ax = plt.subplots(1, 1, figsize=(12, 4))

plt.plot(np.ones((2,))*freq_targets[labels[trial]-1], np.array([0,50]))
plt.plot(np.ones((2,))*freq_targets[labels[trial]-1]*2, np.array([0,50]))
plt.plot(np.ones((2,))*freq_targets[labels[trial]-1]*3, np.array([0,50]))
plt.plot(np.ones((2,))*freq_targets[labels[trial]-1]*4, np.array([0,50]))

e1 = 6
y = eeg[e1, timesinit[trial]:timesterm[trial]]
y = butter_bandpass_filter(y, 5, 40, 128, order=5)
freqs, psd = signal.welch(y, sr, nperseg=win)
plt.plot(freqs, psd, color='k', lw=2)
electrodelabel1 = mat['info']['label'][0][0][0][e1][0]

e2 = 7
freqs, psd = signal.welch(eeg[e2, timesinit[trial]:timesterm[trial]], sr, nperseg=win)
#plt.plot(freqs, psd, color='k', lw=2)
electrodelabel2 = mat['info']['label'][0][0][0][e2][0]

plt.xlabel('Frequency (Hz)')
plt.ylabel('Power spectral density (V^2 / Hz)')
#plt.ylim([0, 100])
plt.title("Welch's periodogram")
#plt.xlim([0, 100])

# %% CCA approach

cca = CCA(n_components=1)

scores = np.ones((12,5))

for trial in range(12):

# X : array-like, shape = [n_samples, n_features]
# Y : array-like, shape = [n_samples, n_targets]
    for f in range(5):
        X = eeg[:, timesinit[trial]:timesterm[trial]].transpose()
        Y = freq_basis(freq_targets[f], 128, 5)
        cca.fit(X, Y)
        scores[trial, f] = cca.score(X,Y)
        
fig, ax = plt.subplots(1, 1, figsize=(12, 4))
plt.imshow(scores)

print(np.argmax(scores,1) + 1)
print(labels)

# %%
def freq_basis(f, sr, T):
    
    # T is length of time interval, sr is sample freuqency
    time = np.linspace(0,T,T*128)
    
    for i in range(1,4):
        if i == 1:
            Y =  np.vstack([np.sin(2*np.pi*f*time*i), np.cos(2*np.pi*f*time*i)])
        else:
            Y = np.vstack([Y, np.sin(2*np.pi*f*time*i), np.cos(2*np.pi*f*time*i)])
    
    return Y.transpose()

# %%
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y
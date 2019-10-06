# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 14:23:45 2019

@author: Vilsnk
"""
from scipy.signal import butter, lfilter, iirnotch, welch
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

fs = 250.0
lowcut = 3
highcut = 40
b, a = butter_bandpass(lowcut, highcut, fs, order=5)
y = lfilter(b, a, EEG[:,0])
y = y[1000:]
freqs, psd = welch(y,250,nperseg=1000)
plt.plot(freqs[:150], psd[:150], color='k', lw=2)
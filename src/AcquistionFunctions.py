import numpy as np
from scipy.signal import butter, sosfilt, iirnotch, welch, lfilter
import matplotlib.pyplot as plt
from scipy.signal import freqz
from sklearn.cross_decomposition import CCA
from sklearn import metrics

freq = 250
lowcut = 4
highcut = 30
coi = np.arange(8)
lcoi = len(coi)


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

def freq_basis(f, sr, T):
    # T is length of time interval, sr is sample freuqency
    time = np.linspace(0,T,T*sr)
    
    for i in range(1,5):
        if i == 1:
            Y =  np.vstack([np.sin(2*np.pi*f*time*i), np.cos(2*np.pi*f*time*i)])
        else:
            Y = np.vstack([Y, np.sin(2*np.pi*f*time*i), np.cos(2*np.pi*f*time*i)])
            
    return Y.transpose()
    
def process_EEG(E,yesfreq,nofreq):
    E = E[1:,coi]
    E -= np.mean(E,0).reshape(1,-1) 
    E -= np.mean(E,1).reshape(-1,1)
    fE = filter_and_cut_EGG_signal(E)
    cca = CCA(n_components=1)
    scores = np.zeros((len(filteredEEG),2))
    T = int(len(filteredEEG[0])/freq)
    Yyes = freq_basis(yesfreq, freq, T)
    Yno = freq_basis(nofreq, freq, T)
    
    cca.fit(fE, Yyes)
    scoreyes = metrics.r2_score(Yyes,cca.predict(fE))#cca.score(X,Y)
    
    cca.fit(fE, Yno)
    scoreno = metrics.r2_score(Yno,cca.predict(fE))
    
    return (scoreyes,scoreno)
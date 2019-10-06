from scipy.signal import butter, lfilter, iirnotch
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz


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


if __name__ == "__main__":
    data = np.genfromtxt('data.csv', delimiter=',')
    c1 = data[:,1]
    o1 = np.copy(c1)
    
    # bandpass filtering
    fs = 5000.0
    lowcut = 500.0
    highcut = 1250.0
    b, a = butter_bandpass(lowcut, highcut, fs, order=5)
    o1 = lfilter(b, a, o1)
    
    # notch filtering
    a,b = iirnotch(50.0,30.0,fs)
    o1 = lfilter(b, a, c1)
    
    fout = open("output.csv","w")
    for (x,y) in zip(c1,o1):
        fout.write("%s,%s\n" % (x,y))
    fout.close()    """
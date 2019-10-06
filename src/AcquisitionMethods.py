# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 14:52:14 2019

@author: Vilsnk
"""
# %% import

import UnicornPy
import numpy as np
from scipy.signal import butter, sosfilt, iirnotch, welch
import matplotlib.pyplot as plt
from scipy.signal import freqz

# %% Set up

# Specifications for the data acquisition.
TestsignaleEnabled = False;
FrameLength = 1;
AcquisitionDurationInSeconds = 120;

# Get available device serials.
deviceList = UnicornPy.GetAvailableDevices(True)

# Print available device serials.
print("Available devices:")
i = 0
for device in deviceList:
    print("#%i %s" % (i,device))
    i+=1

# Request device selection.
print()
deviceID = int(input("Select device by ID #"))
if deviceID < 0 or deviceID > len(deviceList):
    raise IndexError('The selected device ID is not valid.')

# Open selected device.
print()
print("Trying to connect to '%s'." %deviceList[deviceID])
device = UnicornPy.Unicorn(deviceList[deviceID])
print("Connected to '%s'." %deviceList[deviceID])
print()

# Initialize acquisition members.
numberOfAcquiredChannels= device.GetNumberOfAcquiredChannels()
configuration = device.GetConfiguration()

# Print acquisition configuration
print("Acquisition Configuration:");
print("Sampling Rate: %i Hz" %UnicornPy.SamplingRate);
print("Frame Length: %i" %FrameLength);
print("Number Of Acquired Channels: %i" %numberOfAcquiredChannels);
print("Data Acquisition Length: %i s" %AcquisitionDurationInSeconds);
print();

# %% Get data

# Allocate memory for the acquisition buffer.
receiveBufferBufferLength = FrameLength * numberOfAcquiredChannels * 4
receiveBuffer = bytearray(receiveBufferBufferLength)

# Start data acquisition.
device.StartAcquisition(TestsignaleEnabled)
print("Data acquisition started.")

# Calculate number of get data calls.
numberOfGetDataCalls = int(AcquisitionDurationInSeconds * UnicornPy.SamplingRate / FrameLength);

# Limit console update rate to max. 25Hz or slower to prevent acquisition timing issues.                   
consoleUpdateRate = int((UnicornPy.SamplingRate / FrameLength) / 25.0);
if consoleUpdateRate == 0:
    consoleUpdateRate = 1

# Acquisition loop.
bci_data = np.zeros((1,17))
for i in range (0,numberOfGetDataCalls):
    # Receives the configured number of samples from the Unicorn device and writes it to the acquisition buffer.
    device.GetData(FrameLength,receiveBuffer,receiveBufferBufferLength)

    # Convert receive buffer to numpy float array 
    data = np.frombuffer(receiveBuffer, dtype=np.float32, count=numberOfAcquiredChannels * FrameLength)
    data = np.reshape(data, (FrameLength, numberOfAcquiredChannels))
    bci_data = np.vstack([bci_data,data])
    
    # Update console to indicate that the data acquisition is running.
    if i % consoleUpdateRate == 0:
        print('.',end='',flush=True)

# Stop data acquisition.
bci_data = bci_data[1:,:]
device.StopAcquisition();
print()
print("Data acquisition stopped.");

# release receive allocated memory of receive buffer
del receiveBuffer

# Close device.
print("Disconnected from Unicorn")

# %% filtering
#%matplotlib qt
coi = np.arange(8)
lcoi = len(coi)
freq = UnicornPy.SamplingRate

EEG = bci_data[:,coi]

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    sos = butter(order, [low, high], btype='band',output='sos')
    return sos

lowcut = 4
highcut = 40
sos = butter_bandpass(lowcut, highcut, freq, order=15)
filteredEEG = EEG + 0.
for i in range(lcoi):
    filteredEEG[:,i] = sosfilt(sos, EEG[:,i])

# %% plot power spec
filteredEEG = filteredEEG[30*250-1:,:]    
for i in range(lcoi):
    freqs, psd = welch(filteredEEG[:,i], freq, nperseg=freq*4)
    plt.plot(freqs[:-1], psd[:-1], lw=2,label=str(coi[i]))
    plt.legend()
    
    
# %% soome tests
    
    
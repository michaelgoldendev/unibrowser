# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 14:52:14 2019

@author: Vilsnk
"""
# %% import

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import UnicornPy
import numpy as np
from scipy.signal import butter, sosfilt, iirnotch, welch
import matplotlib.pyplot as plt
from scipy.signal import freqz
import time
import collections

class UnicornStreamingAcquisition:
    
    def __init__(self, AcquisitionDurationInSeconds=10):
            # %% Set up
        self.AcquisitionDurationInSeconds = AcquisitionDurationInSeconds
        # Specifications for the data acquisition.
        self.TestsignaleEnabled = False
        self.FrameLength = 1
    
        # Get available device serials.
        deviceList = UnicornPy.GetAvailableDevices(True)
        deviceID = 0
    
        # Open selected device.
        print()
        print("Trying to connect to '%s'." %deviceList[deviceID])
        self.device = UnicornPy.Unicorn(deviceList[deviceID])
        print("Connected to '%s'." %deviceList[deviceID])
        print()
    
        # Initialize acquisition members.
        self.numberOfAcquiredChannels= self.device.GetNumberOfAcquiredChannels()
    
        # Print acquisition configuration
        print("Acquisition Configuration:")
        print("Sampling Rate: %i Hz" %UnicornPy.SamplingRate)
        print("Frame Length: %i" %self.FrameLength)
        print("Number Of Acquired Channels: %i" %self.numberOfAcquiredChannels)
        print("Data Acquisition Length: %i s" %AcquisitionDurationInSeconds)
        print()
    
        # %% Get data
    
        # Allocate memory for the acquisition buffer.
        self.receiveBufferBufferLength = self.FrameLength * self.numberOfAcquiredChannels * 4
        self.receiveBuffer = bytearray(self.receiveBufferBufferLength)
        
        self.maxseconds = 20 # store up to 20 seconds of data
        maxbufferlength = int(self.maxseconds * UnicornPy.SamplingRate / self.FrameLength)
        self.framebuffer = collections.deque(maxlen=maxbufferlength)
        
        
        
         # Start data acquisition.
        self.device.StartAcquisition(self.TestsignaleEnabled)
        print("Data acquisition started.")
    
        # Calculate number of get data calls.
        numberOfGetDataCalls = int(self.AcquisitionDurationInSeconds * UnicornPy.SamplingRate / self.FrameLength)
        numberOfGetDataCalls = 10000000000000000
    
        # Limit console update rate to max. 25Hz or slower to prevent acquisition timing issues.                   
        consoleUpdateRate = int((UnicornPy.SamplingRate / self.FrameLength) / 25.0)
        if consoleUpdateRate == 0:
            consoleUpdateRate = 1
    
        # Acquisition loop.
        #bci_data = np.zeros((1,17))
        for i in range (0,numberOfGetDataCalls):
            # Receives the configured number of samples from the Unicorn device and writes it to the acquisition buffer.
            self.device.GetData(self.FrameLength,self.receiveBuffer,self.receiveBufferBufferLength)
    
            # Convert receive buffer to numpy float array 
            data = np.frombuffer(self.receiveBuffer, dtype=np.float32, count=self.numberOfAcquiredChannels * self.FrameLength)
            data = np.reshape(data, (self.FrameLength, self.numberOfAcquiredChannels))
            timestampedframe = (time.time(), np.copy(data))
            self.framebuffer.append(timestampedframe)
            
            # Update console to indicate that the data acquisition is running.
            if i % consoleUpdateRate == 0:
                print('.',end='',flush=True)
                print(len(self.framebuffer))
    
    
    def getNseconds(self, numseconds):
        numberOfGetDataCalls = int(self.AcquisitionDurationInSeconds * UnicornPy.SamplingRate / self.FrameLength)
        
    
        # Stop data acquisition.
        #bci_data = bci_data[1:,:]
       
    
    def stopRecording(self):
        self.device.StopAcquisition()
        print()
        print("Data acquisition stopped.")
    
        # release receive allocated memory of receive buffer
        del self.receiveBuffer
    
if __name__ == '__main__':
    streamingacquisition = UnicornStreamingAcquisition()
    
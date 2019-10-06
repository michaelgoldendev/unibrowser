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
    
    def __init__(self):
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
        print()
    
        # %% Get data
    
        # Allocate memory for the acquisition buffer.
        self.receiveBufferBufferLength = self.FrameLength * self.numberOfAcquiredChannels * 4
        self.receiveBuffer = bytearray(self.receiveBufferBufferLength)
        
         # Start data acquisition.
        self.device.StartAcquisition(self.TestsignaleEnabled)
        print("Data acquisition started.")
    
    
    
    def getNseconds(self, numseconds):
        receiveBufferBufferLength = self.FrameLength * self.numberOfAcquiredChannels * 4
        receiveBuffer = bytearray(receiveBufferBufferLength)        
        numberOfGetDataCalls = int(numseconds * UnicornPy.SamplingRate / self.FrameLength)
        
        # Limit console update rate to max. 25Hz or slower to prevent acquisition timing issues.                   
        consoleUpdateRate = int((UnicornPy.SamplingRate / self.FrameLength) / 25.0)
        if consoleUpdateRate == 0:
            consoleUpdateRate = 1
    
        # Acquisition loop.
        big_data = np.zeros((1,17))
        for i in range (0,numberOfGetDataCalls):
            # Receives the configured number of samples from the Unicorn device and writes it to the acquisition buffer.
            self.device.GetData(self.FrameLength,receiveBuffer,receiveBufferBufferLength)
    
            # Convert receive buffer to numpy float array 
            data = np.frombuffer(receiveBuffer, dtype=np.float32, count=self.numberOfAcquiredChannels * self.FrameLength)
            data = np.reshape(data, (self.FrameLength, self.numberOfAcquiredChannels))
            big_data = np.vstack([big_data,data])
            # Update console to indicate that the data acquisition is running.
            if i % consoleUpdateRate == 0:
                print('.',end='',flush=True)
        return big_data
       
    
    def stopRecording(self):
        self.device.StopAcquisition()
        print()
        print("Data acquisition stopped.")
    
        # release receive allocated memory of receive buffer
        del self.receiveBuffer
    
if __name__ == '__main__':
    streamingacquisition = UnicornStreamingAcquisition()
    time.sleep(1.0)
    streamingacquisition.getNseconds(7.0)
    streamingacquisition.stopRecording()
    
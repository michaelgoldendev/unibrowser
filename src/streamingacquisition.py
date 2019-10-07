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
        self.captureframes = 0
        self.big_data = np.zeros((1,17))
    
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
        
        self.receiveBufferBufferLength = self.FrameLength * self.numberOfAcquiredChannels * 4
        
    
    def startAcquisition(self):
        i = 1
        while True:
            # Receives the configured number of samples from the Unicorn device and writes it to the acquisition buffer.
            self.device.GetData(self.FrameLength,self.receiveBuffer,self.receiveBufferBufferLength)
            if self.captureframes > 0:
                data = np.frombuffer(self.receiveBuffer, dtype=np.float32, count=self.numberOfAcquiredChannels * self.FrameLength)
                data = np.reshape(data, (self.FrameLength, self.numberOfAcquiredChannels))
                self.big_data = np.vstack([self.big_data,data])
                self.captureframes -= 1
            i += 1
            if i % 1000 == 0:
                print(i,self.captureframes)
            time.sleep(0.05)
    
    def cancelAcquisition(self):
        self.captureframes = 0
    
    
    def getNseconds(self, numseconds):
        numberOfGetDataCalls = int(numseconds * UnicornPy.SamplingRate / self.FrameLength)
        self.big_data = np.zeros((1,17))
        self.captureframes = numberOfGetDataCalls
        while self.captureframes > 0:
            time.sleep(0.05)
        return np.copy(self.big_data)
        
                
        
        """
        # Limit console update rate to max. 25Hz or slower to prevent acquisition timing issues.                   
        consoleUpdateRate = int((UnicornPy.SamplingRate / self.FrameLength) / 25.0)
        if consoleUpdateRate == 0:
            consoleUpdateRate = 1
    
        # Acquisition loop.
        big_data = np.zeros((1,17))
        for i in range (0,numberOfGetDataCalls):
            # Receives the configured number of samples from the Unicorn device and writes it to the acquisition buffer.
            self.device.GetData(self.FrameLength,self.receiveBuffer,self.receiveBufferBufferLength)
    
            # Convert receive buffer to numpy float array 
            data = np.frombuffer(self.receiveBuffer, dtype=np.float32, count=self.numberOfAcquiredChannels * self.FrameLength)
            data = np.reshape(data, (self.FrameLength, self.numberOfAcquiredChannels))
            big_data = np.vstack([big_data,data])
            # Update console to indicate that the data acquisition is running.
            
        return big_data
        """
       
    
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
    
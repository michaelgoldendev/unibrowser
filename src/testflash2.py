#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 22:33:48 2019

@author: mo
"""

import numpy as np
import cv2
import time

i=0
img=np.zeros((400,800,3),np.uint8)
img.fill(255)
while(i<=1):
    img[0:400,400:800]=(153,0,255)
    cv2.imshow('package',img)
    cv2.waitKey(5000)        
    img[0:400,400:800]=(255,255,255)
    cv2.imshow('package',img)
    cv2.waitKey(5000)
    img[0:400,400:800]=(153,0,255)
    cv2.imshow('package',img)
    cv2.waitKey(5000)
    i=i+1

cv2.destroyAllWindows()
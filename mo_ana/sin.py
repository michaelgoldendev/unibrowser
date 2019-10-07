#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 12:36:32 2019

@author: mo
"""

import matplotlib.pyplot
import numpy as np

x = np.linspace(0,14,1000)
fig = plt.figure()
plt.plot(x, np.sin(x))

plt.savefig("sin.png", dpi=120)
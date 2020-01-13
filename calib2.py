# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 15:03:45 2018

Fareez Sanif
Trying to Calibrate with File 488mV.wav
"""

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from scipy.io.wavfile import read

#### Define constants
fs = 44100  #Sampling frequency in Hz

Vcalib = 61.6 #in mV The expected voltage of the input
calibration_factor = 1#216.6529029461996 #Will leave things as mV
#####################

## Read File
a = read('616mV.wav') #Vrms = XX.XmV
b = np.array(a[1],dtype=float)*calibration_factor

#### Periodogram

f, Pxx_den = signal.welch(b, fs, nperseg=fs)
f1, Pxx_spec = signal.welch(b, fs, nperseg=fs, scaling='spectrum')

#### Graph Periodogram
plt.semilogy(f, Pxx_den)
#plt.xlim([0, 100])
#plt.ylim([10e-14, 10e2])
plt.xlabel('frequency [Hz]')
plt.ylabel('PSD [V**2/Hz]')
plt.show()

#plt.semilogy(f1, Pxx_spec)
#plt.show()

### Check somethings
if calibration_factor == 1 :
    print(f'Calibration Factor should be {Vcalib/np.sqrt(Pxx_spec.max())}')
else: 
    print(f'{np.sqrt(Pxx_spec.max())}mV should be equal to Vcalib = {Vcalib}mV')
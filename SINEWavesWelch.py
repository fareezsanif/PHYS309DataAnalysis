# -*- coding: utf-8 -*-
"""
Testing the periodagram function

Fareez Sanif
30 October 2018
"""

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

#### Define constants
fs = 48000  #Sampling frequency in Hz
t = 6 #time for sample sound wave in seconds
f = 6000 #Frequency of test sine wave in Hz
A = 20 #Amplitude of the test sine wave

noise_power = 0.001 * fs / 2
time = np.arange(fs*t) / fs
#####################

#### Create test sine wave
#Define sample domain from 0 to t with fs*t samples in between
x = np.linspace(0, t, fs*t)
#Create sine wave with amplitude A and frequency f
testWave = A*np.sin(2*np.pi*f*x)
testWave += np.random.normal(scale=np.sqrt(noise_power), size=time.shape)

#### Test the sine wave and check it's what is wanted
#plt.plot(x, testWave)
#plt.xlim([0, t])
#plt.show()

#### Periodogram

f, Pxx_den = signal.welch(testWave, fs, nperseg=fs)
f1, Pxx_spec = signal.welch(testWave, fs, nperseg=fs, scaling='spectrum')



#### Graph Periodogram
plt.semilogy(f, Pxx_den)
#plt.xlim([0, 100])
#plt.ylim([10e-14, 10e2])
plt.xlabel('frequency [Hz]')
plt.ylabel('PSD [V**2/Hz]')
plt.show()

plt.semilogy(f1, Pxx_spec)
plt.show()

### Check somethings.... Hmmmm
print(np.sqrt(Pxx_spec.max())) #This is an estimate only. Not very good to test
print(A*np.sqrt(2)/2) 

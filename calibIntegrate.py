from scipy.io.wavfile import read
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy import signal

# calib=0
files = ['244mV.wav', '488mV.wav','616mV.wav']
V_gens = [24.4, 48.8, 61.6]

for i in range(len(files)):
    a = read(files[i])

    V_gen = V_gens[i] #mV RMS, Input from the function generator
    V_in = V_gen * 0.3/(561+559+0.3) # mV RMS # Input Voltage to the pre-amp

    print(f'Input Voltage is {V_in} mV RMS')


    calibration_factor = 0.055350283120348995# Calibrated using average of calibration factors
    b = np.array(a[1],dtype=float)*calibration_factor
    fs = 44100 # Sampling frequency

    fsp, Pxx_spec = signal.periodogram(b, fs, scaling='spectrum') # Get power spectrum of data
    peak = np.argmax(Pxx_spec) # Index of the peak

    V_out = np.sqrt(sp.integrate.simps(Pxx_spec[peak-10: peak+10])) #Integrate over some frequency range to recover full signal
    Pxx_spec = np.sqrt(Pxx_spec) # Convert units from units^2 to units

    print(f'Integrating gives {V_out} mV RMS')

    xdata = np.linspace(0, len(b)/fs, len(b)) # Make x axis in seconds

    peakfind, _ = signal.find_peaks(b) # Get peaks of signal
    peakfind_b, _ = signal.find_peaks(-b) # Get Valleys of Signal
    peakfind_avg = (abs(np.average(b[peakfind]))+abs(np.average(b[peakfind_b])))/2 # Compute amplitude of signal (approx)
    amp_p = peakfind_avg/np.sqrt(2)
    print(f'peakfind gives {amp_p} mV RMS\n')

    print(f'Spectrum percent error is {np.abs(V_out-V_in)/V_in*100}%')
    print(f'Peakfind percent error is {np.abs(amp_p-V_in)/V_in*100}\n')

    print(f'Calibration factor should be {V_in/V_out}%\n')
    calib = V_in/V_out
    fig, ax = plt.subplots(1,1)
    ax.semilogy(fsp, Pxx_spec) # Plot the power spectrum of data
    plt.xlabel('frequency [Hz]')
    plt.ylabel('Power spectrum[uV]')
    plt.title("Power Spectrum")
    plt.xlim(fsp[peak-500], fsp[peak+500])
    plt.ylim(10**(-5),100)

#    ## Plot first 100 data points and fit
#    plt.figure()
#    plt.plot(xdata, b, label='data')
#    plt.plot(xdata[peakfind], b[peakfind], '.')
#    plt.plot(xdata[peakfind_b], b[peakfind_b], '.')
#    plt.xlabel('time [sec]')
#    #plt.ylabel('Magnitude [uV]')
#    #plt.title("Data + fit (first 100 points)")
#    plt.legend()
#    plt.xlim(0,100/fs)
#    plt.show()

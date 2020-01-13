from scipy.io.wavfile import read
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import signal
from scipy.signal import find_peaks

# for fname in ('Phys309/488mV.wav', 'Phys309/short.wav')
a = read('488mV.wav')
calibration_factor = 26.32/0.21776539485327695
#amp_factor = 1958
b = np.array(a[1],dtype=float)*calibration_factor
fs = 44100 # Sampling frequency

# Fitting function
def fit(x, a, b, phi):
    return a*np.cos(2*np.pi*b * x + phi)

fsp, Pxx_spec = signal.periodogram(b, fs, scaling='spectrum') # Get power spectrum of data
Pxx_spec = np.sqrt(Pxx_spec) # Convert units from units^2 to units
# fden, Pxx_den = signal.periodogram(b, fs, scaling='density') # Get power spectrum density of data

xdata = np.linspace(0, len(b)/fs, len(b)) # Make x axis in seconds

ran = slice(20349) # How many points to fit (fits first 20349 points)
popt, pcov = curve_fit(fit, xdata[:100], b[:100], p0=[39.153047034177014, 3858, 0]) # Fit first 100 data points (works)
popt1, pcov = curve_fit(fit, xdata[ran], b[ran], p0=[popt[0], popt[1], popt[2]]) # Fit first ran points (ran + 1 is bad!, why?? 
                                                                                 # refer to Figure 3 and 4 which plot first and last 100 points of data)

test = 40 * np.sin(2*np.pi*10000 * xdata) # test for periodogram
fsp_t, Pxx_spec_t = signal.periodogram(test, 44100, scaling='spectrum')
Pxx_spec_t = np.sqrt(Pxx_spec_t)

# print(popt)
print(popt1) # print fit parameters

peakfind = find_peaks(b)
print(np.average(b[peakfind[0]])) # Print an estimate of the amplitude of our data
print(f'Peak of power spectrum is at {np.max(Pxx_spec)} uV, {fsp[np.argmax(Pxx_spec)]}hz') # print the magnitude and frequency of peak
print(f'Peak of power spectrum (test data) is at {np.max(Pxx_spec_t)*np.sqrt(2)} uV, {fsp_t[np.argmax(Pxx_spec_t)]}hz') # print the magnitude and frequency of peak (test data)

fig, ax = plt.subplots(1,1)
ax.semilogy(fsp, Pxx_spec) # Plot the power spectrum of data
plt.xlabel('frequency [Hz]')
plt.ylabel('Power spectrum[uV]')
plt.title("Power Spectrum")
#plt.xlim(0,1000)
plt.ylim(10**(-5),100)

### Plot the power spectrum of test data, why not a sharp peak (still some width to it)
fig, ax = plt.subplots(1,1)
ax.semilogy(fsp_t, Pxx_spec_t) 
plt.xlabel('frequency [Hz]')
plt.ylabel('[uV]')
plt.title("Power Spectrum (test data)")
#plt.xlim(0,1000)
plt.ylim(10**(-5),100)

### Plot PSD of data
# fig1, ax1 = plt.subplots(1,1)
# ax1.semilogy(fden, Pxx_den) 
# plt.xlabel('frequency [Hz]')
# plt.ylabel('PSD [V**2/Hz]')
# plt.title("PSD")
# plt.xlim(0,500)
# plt.ylim(10**(-20),10**(-14))
# plt.show()

### Plot Welch PSD
# fig2, ax2 = plt.subplots(1,1)
# ax2.semilogy(fw, Pxx_den_w) 
# plt.xlabel('frequency [Hz]')
# plt.ylabel('PSD [mV**2/Hz]')
# plt.title("Welch psd")

### Plot first 100 data points and fit
plt.figure()
plt.plot(xdata, b, '.', label='data')
# plt.plot(xdata, fit(xdata, *popt), label='fit')
plt.plot(xdata, fit(xdata, *popt1), label='fit')
plt.xlabel('time [sec]')
plt.ylabel('Magnitude [uV]')
plt.title("Data + fit (first 100 points)")
plt.legend()
plt.xlim(0,100/fs)

### Plot last 100 data points and fit
plt.figure()
plt.plot(xdata, b, '.', label='data')
# plt.plot(xdata, fit(xdata, *popt), label='fit')
plt.plot(xdata, fit(xdata, *popt1), label='fit')
plt.xlabel('time [sec]')
plt.ylabel('Magnitude [uV]')
plt.title("Data + fit (last 100 points)")
plt.legend()
plt.xlim((len(b)-100)/fs,len(b)/fs)

plt.show()



"""Given the length of data, it's not possible to use the optimal number of tapers. Many more should be used.
Increasing num tapers can increase accuracy of estimation but with significant cost in computational time.
1,199,000 precisely. Num_tapers = [2TW] - 1. With TW referring to the time bandwidth product.
Calculated using TW = len(data)ΔFs/2
Increasing bandwidth also smooths the data at cost of computational effort.
BW = TW * fs / len(data). As per Chronux. Where TW equals 3.
However, GSP provides a calculate num tapers function which can do this for you.

How to smooth?
- Increase both num of tapers and NW together
"""

#OS Libs
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import time
import ghostipy as gsp

#Custom libs
from utils import reshape #Shapes the 1d array of mv into 2d array of [timepoints, channels]
from utils import helper #Converts psd to decibal scale

# Performance checks
start_time = time.time()

#Load and shape data
file = "/Users/freeman/Documents/saleem_lab/data/R21011_210915_CA1_1.dat"
data_object = reshape.Import_and_Shape_Data(file)
data = data_object.reshape_binary_data()

#Parameters #Real signal is 20hz but downsample to 2hz
original_fs = 20000 #Hzs
fs = 2000 #Hz
downsample_factor = 10 #If 10. This takes a 20khz signal to a 2khz signal
seconds_in_session = len(data[0:-1:downsample_factor, 0]) / 2000 #Number of seconds of the session
NW = 15 #Time bandwidth product chronux recommends 3 - INCREASE TO SMOOTH DATA as it increases bandwidth
numtapers = 25#Number of tapers to use. Chronux recommends 5 - INCREASE TO IMPROVE ACCURACY OF EST
# nfft = 1028 * 2 #The length of the signal I want to calcualte the fourier transform of.
#Has to be a power of 2 for computational efficiency. Helpful comparing signals of different sizes.
# Also related to padding of the FFT

#Channel selection
c1 = data[0:-1:downsample_factor, 0] #downsampled to speed up multi tapered estimation

#Bandpass Filter
sos = signal.butter(N = 5, Wn = 300, btype = 'lowpass', output ='sos', fs = fs)
filtered_signal = signal.sosfilt(sos, c1)

#Compute Bandwidth possible with hardcoded NW due to large data size.
#If increased too large I believe spectral leakage will occur
bandwidth = NW * fs / len(filtered_signal)

#Conduct PSD estimation using GhostiPy
psd, freqs = gsp.mtm_spectrum(data          = filtered_signal,
                              fs            = fs,
                              n_fft_threads = 8,
                              bandwidth     = bandwidth,
                              n_tapers      = numtapers)
#Convert psd to decibel
helper.dB(psd, psd)

#How long did the full script take?
print("")
print("--- %s seconds ---" % (time.time() - start_time))
print("")

#Plotting configurations
plt.title("Power spectral density analysis - 1 Channel at 2kHz")
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power - Db')
plt.xlim([0,80])
plt.ylim(0,80)
plt.plot(freqs, psd)
plt.show()

"""Given the length of data, it's not possible to use the optimal number of tapers. Many more should be used.
Increasing num tapers can increase accuracy of estimation but with significant cost in computational time.
1,199,000 precisely. Num_tapers = [2TW] - 1. With TW referring to the time bandwidth product.
Calculated using TW = len(data)ΔFs/2
Increasing bandwidth also smooths the data at cost of computational effort.
BW = TW * fs / len(data). As per Chronux. Where TW equals 3.
However, GSPi provides a calculate num tapers function which can do this for you.

How to smooth?
- Increase both num of tapers and NW together

Works on mac but not windows for some reason...
"""

#OS Libs
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import time
import ghostipy as gsp

#Custom libs
from utils import reshape #Shapes the 1d array of mv into 2d array of [timepoints, channels]
from utils import helper

#filtered signal is indexed by ripple range
def power_spectral_density(filtered_signal, fs):
    NW = 15 #Time bandwidth product chronux recommends 3 - INCREASE TO SMOOTH DATA as it increases bandwidth
    numtapers = 25 #Number of tapers to use. Chronux recommends 5 - INCREASE TO IMPROVE ACCURACY OF EST
    #Compute Bandwidth possible with hardcoded NW due to large data size.
    #If increased too large I believe spectral leakage will occur
    bandwidth = NW * fs / len(filtered_signal)
    if bandwidth > 5:
        print("Bandwidth currently sits at:", bandwidth)
        print("Consider lowering if required by altering NW")
    psd, freqs = gsp.mtm_spectrum(data          = filtered_signal,
                                  fs            = fs,
                                  n_fft_threads = 8,
                                  bandwidth     = bandwidth,
                                  n_tapers      = numtapers)
    helper.dB(psd, psd)
    return (freqs, psd)

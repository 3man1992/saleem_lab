"""In the context of time-frequency analysis, HeisenBerg's uncertainity
principal denotes that a function can't be both temporally and spatially localised.
Thus one can't achieve the perfect temporal and spatial resolution at the same time.
This is the flaw of the short-time Fourier transform. If one uses a wide window, a good
spatial frequency resolution at the cost of temporal resolution is caused. With a narrow
window one has the opporsite trade off. This happens in the short-time-fourier transform.

Thus the wavelet transform is used when transients are important.

I think this method uses the Inverse Fourier transform calc of CWT"""

#OS libaries
import ghostipy as gsp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import time
from scipy import signal
from ripple_detection import filter_ripple_band

#Custom libs
from utils import reshape #Shapes the 1d array of mv into 2d array of [timepoints, channels]
from utils import helper #Converts psd to decibal scale

# Performance checks
start_time = time.time()

#Load and shape data
file = "/Users/freeman/Documents/saleem_folder/data/tomazzo_data/R21011_210915_CA1_1.dat"
data_object = reshape.Import_and_Shape_Data(file)
data = data_object.reshape_binary_data()
ripple_times = np.load("ripple_times.npy")

#Parameters #Real signal is 20hz but downsample to 2hz
original_fs = 20000 #Hzs
fs = 1000 #Hz
downsample_factor = 20 #If 10. This takes a 20khz signal to a 2khz signal
seconds_in_session = len(data[0:-1:downsample_factor, 0]) / 2000 #Number of seconds of the session
# NW = 15 #Time bandwidth product chronux recommends 3 - INCREASE TO SMOOTH DATA as it increases bandwidth
numtapers = 2 #Number of tapers to use. Chronux recommends 5 - INCREASE TO IMPROVE ACCURACY OF EST
nperseg   = 256 * 10 #Number of samples to use for taper windowmHas to be a power of 2 for computational efficiency. Helpful comparing signals of different sizes.
# noverlap  = 0 Number of points to overlap between segments. Default is nperseg // 8.
# channel = 3

#Downsample and channel selection
data = data[0:-1:downsample_factor, :] #downsampled to speed up multi tapered estimation

#Bandpass Filter
sos = signal.butter(N = 5, Wn = 100, btype = 'lowpass', output ='sos', fs = fs)
# filtered_signal = signal.sosfilt(sos, channel_downsampled)
filtered_signal = filter_ripple_band(data)
print('Shape post filter', filtered_signal.shape)
# filtered_signal = filtered_signal[:, 3]

#CWT
coefs_cwt, _, f_cwt, t_cwt, _ = gsp.cwt(data        = filtered_signal[:, 3],
                                        fs          = fs,
                                        freq_limits = [1, 500],
                                        method      = 'full',
                                        n_workers   = 8,
                                        verbose     = True)

#SST
coefs_wsst, _, f_wsst, t_wsst, _ = gsp.wsst(data        = filtered_signal[:, 3],
                                            fs          = fs,
                                            freq_limits =[1, 500],
                                            voices_per_octave=32)

# will be normalized such that max is 1, so the
# sampling rate factor can be dropped
psd_cwt = coefs_cwt.real**2 + coefs_cwt.imag**2
psd_cwt /= np.max(psd_cwt)

psd_wsst = coefs_wsst.real**2 + coefs_wsst.imag**2
psd_wsst /= np.max(psd_wsst)

# Convert psd to decibel - For log conversion
# helper.dB(psd_cwt, psd_cwt)

# Plotting logic
kwargs_dict = {}
kwargs_dict['cmap'] = plt.cm.Spectral_r
kwargs_dict['linewidth'] = 0
kwargs_dict['vmin'] = 0
kwargs_dict['vmax'] = 1
kwargs_dict['rasterized'] = True
kwargs_dict['shading'] = 'auto'

#test one ripple against one lfp raw
print("time to plot")
for ripple_time in range(3):
    fig, axs = plt.subplots(2, sharex=True)
    axs[0].pcolormesh(t_cwt, f_cwt, psd_cwt, **kwargs_dict)
    axs[1].pcolormesh(t_wsst, f_wsst, psd_wsst, **kwargs_dict)
    axs[0].set_xlim(ripple_times[ripple_time][0], ripple_times[ripple_time][1])
    plt.ylim(0, 400)
    plt.xlabel('Time (Seconds)')
    plt.ylabel('Frequency (Hz)')
    plt.show()

# plt.pcolormesh(t_cwt, f_cwt, psd_cwt, **kwargs_dict)
# # plt.colorbar()
# plt.xlim(ripple_times[0][0], ripple_times[0][1])
# plt.ylim(0, 250)
# plt.xlabel('Time (Seconds)')
# plt.ylabel('Frequency (Hz)')
# plt.show()

#How long did the full script take?
print("")
print("--- %s seconds ---" % (time.time() - start_time))
print("")

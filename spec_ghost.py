#OS libaries
import ghostipy as gsp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import time
from scipy import signal

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
NW = 5 #Time bandwidth product chronux recommends 3 - INCREASE TO SMOOTH DATA as it increases bandwidth
numtapers = 25#Number of tapers to use. Chronux recommends 5 - INCREASE TO IMPROVE ACCURACY OF EST
# nfft = 1028 * 2 #The length of the signal I want to calcualte the fourier transform of.
#Has to be a power of 2 for computational efficiency. Helpful comparing signals of different sizes.
# Also related to padding of the FFT
nperseg   = 256 * 4
noverlap  = 0

#Downsample and channel selection
c1 = data[0:-1:downsample_factor, 0] #downsampled to speed up multi tapered estimation

#Bandpass Filter
sos = signal.butter(N = 5, Wn = 300, btype = 'lowpass', output ='sos', fs = fs)
filtered_signal = signal.sosfilt(sos, c1)
bandwidth = NW * fs / len(filtered_signal)

#Compute Bandwidth possible with hardcoded NW due to large data size.
#If increased too large I believe spectral leakage will occur
bandwidth = NW * fs / len(filtered_signal)


#Compute the cwt method for computing the spectrogram
# coefs_cwt, _, f_cwt, t_cwt, _ = gsp.cwt(data        = filtered_signal,
#                                         fs          = fs,
#                                         freq_limits = [1, 300],
#                                         method      = 'full',
#                                         n_workers   = 8,
#                                         verbose     = True)
# psd_cwt = coefs_cwt.real**2 + coefs_cwt.imag**2
# # psd_cwt /= np.max(psd_cwt)
# kwargs_dict = {}
# kwargs_dict['cmap'] = plt.cm.Spectral_r
# kwargs_dict['vmin'] = 0
# kwargs_dict['vmax'] = 1
# kwargs_dict['linewidth'] = 0
# kwargs_dict['rasterized'] = True
# kwargs_dict['shading'] = 'auto'
# plt.pcolormesh(t_cwt, f_cwt, psd_cwt, **kwargs_dict)
# plt.show()

#Compute the Thomson's Multitaper method for computing the spectrogram
psd_mtm, f_mtm, t_mtm = gsp.mtm_spectrogram(data          = filtered_signal,
                                            bandwidth     = bandwidth,
                                            fs            = fs,
                                            nperseg       = nperseg,
                                            noverlap      = noverlap,
                                            n_tapers      = numtapers,
                                            n_fft_threads = 8 )
# psd_mtm /= np.max(psd_mtm)
#Convert psd to decibel
# helper.dB(psd_mtm, psd_mtm)

# Plotting logic
kwargs_dict = {}
kwargs_dict['cmap'] = plt.cm.Spectral_r
kwargs_dict['vmin'] = 0
kwargs_dict['vmax'] = 1
kwargs_dict['linewidth'] = 0
kwargs_dict['rasterized'] = True
kwargs_dict['shading'] = 'auto'
plt.pcolormesh(t_mtm, f_mtm, psd_mtm, **kwargs_dict)
plt.ylim(0,400)
plt.show()

#How long did the full script take?
print("")
print("--- %s seconds ---" % (time.time() - start_time))
print("")


#Spectrogram using SIGNAL. Does't work
# f, t, Sxx = signal.spectrogram(filtered_signal,
#                                fs = fs)
# plt.imshow(10 * np.log10(Sxx), aspect = 'auto')
# # plt.pcolormesh(t, f, 10 * np.log10(Sxx))

#Spectrogram using MATPLOTLIB - Works but still not as good
# spectrum, freqs, t, im = plt.specgram(filtered_signal,
#                                       NFFT = NFFT,
#                                       Fs = fs,
#                                       window = signal.get_window(('dpss', 3), NFFT),
#                                       scale = 'dB')
# plt.colorbar()
# plt.xlabel('Time (Seconds)')
# plt.ylabel('Frequency (Hz)')
# plt.ylim(0, 80)
# plt.show()

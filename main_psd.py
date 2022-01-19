from utils import reshape
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from os.path import exists
from scipy.fftpack import fft, fftfreq, ifft
from elephant.spectral import welch_psd
from scipy.interpolate import interp1d

#Nitime lib
import nitime.algorithms as tsa
import nitime.utils as utils
from nitime.viz import winspect
from nitime.viz import plot_spectral_estimate
import scipy.signal as sig
import scipy.stats.distributions as dist
import time

# Performance checks
start_time = time.time()

#ghostpy
import ghostipy as gsp

#Load and shape data
file = "/Users/freeman/Documents/saleem_lab/data/R21011_210915_CA1_1.dat"
data_object = reshape.Import_and_Shape_Data(file)
data = data_object.reshape_binary_data()

#Parameters #Real signal is 20hz but downsample to 2hz
original_fs = 20000
fs = 2000
downsample_factor = 10
NW = 5 #Time bandwidth product chronux recommends 3
numtapers = 4 #Number of tapers to use. Chronux recommends 5
# NFFT = 1028 * 2 #The length of the signal I want to calcualte the fourier transform of. Has to be a power of 2 for computational efficiency. Helpful comparing signals of different sizes
#Note multi taper doesn't use fourier transforms

#Channel selection
c1 = data[0:-1:downsample_factor, 5] #downsampled to speed up multi tapered estimation

#Bandpass Filter
sos = signal.butter(N = 5, Wn = 300, btype = 'lowpass', output ='sos', fs = fs)
filtered_signal = signal.sosfilt(sos, c1)

def dB(x, out=None):
    if out is None:
        return 10 * np.log10(x)
    else:
        np.log10(x, out)
        np.multiply(out, 10, out) #Convert power into decibals which is a log scale

#Conduct PSD estimation using GhostiPy
bandwidth = NW * fs / len(filtered_signal)
psd, freqs = gsp.mtm_spectrum(filtered_signal, fs=fs, n_fft_threads=8, bandwidth=bandwidth, n_tapers = numtapers)
dB(psd, psd)

#Plotting configurations
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power - Db')
plt.xlim([0,80])
plt.ylim(0,80)
plt.plot(freqs, psd)
plt.show()

# for ii, bandwidth in enumerate(bandwidths):
#     psd, freqs = gsp.mtm_spectrum(
#         c1,
#         fs=fs,
#         n_fft_threads=8,
#         bandwidth=bandwidth)
#     row_idx, col_idx = np.unravel_index(ii, (2, 2))
#     axes[row_idx, col_idx].plot(freqs, psd, lw=4, color='#064175')
#
#     axes[row_idx, col_idx].set_xlim(50, 500)
#     axes[row_idx, col_idx].set_ylim(0, 2000)
#
#     axes[row_idx, col_idx].set_title(
#         "Bandwidth: {} Hz".format(bandwidths[ii]), fontsize=24)
#     axes[row_idx, col_idx].text(
#         -0.25, 1.1, labels[ii], transform=axes[row_idx, col_idx].transAxes,
#         size=27, weight='bold')
#
# plt.subplots_adjust(wspace=0.3, hspace=0.4)
# plt.show()

#Working code for PSD from niTime library
# ln2db = dB(np.e)
# freqs, d_psd = tsa.periodogram(c1, Fs=fs) #Use a basic peridoogram function to calculate the frequencies
# f, psd_mt, nu = tsa.multi_taper_psd(s = filtered_signal, Fs = fs, adaptive=False, jackknife=False, NW = 3)
# dB(psd_mt, psd_mt)
# Kmax = nu[0] / 2
# p975 = dist.chi2.ppf(.975, 2 * Kmax)
# p025 = dist.chi2.ppf(.025, 2 * Kmax)
# l1 = ln2db * np.log(2 * Kmax / p975)
# l2 = ln2db * np.log(2 * Kmax / p025)
# hyp_limits = (psd_mt + l1, psd_mt + l2)
# plt.plot(freqs, psd_mt, color = 'b', label = 'Multitaper psd estimation')
# plt.xlim([0,80])
# plt.ylim(0,80)
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Power - Db')
# plt.legend()
# plt.show()

#Remove spectrogram code below

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

#How long did the full script take?
print("")
print("--- %s seconds ---" % (time.time() - start_time))
print("")

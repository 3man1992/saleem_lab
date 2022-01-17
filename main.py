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

#Load and shape data
file = "/Users/freeman/Documents/saleem_lab/data/R21011_210915_CA1_1.dat"
data_object = reshape.Import_and_Shape_Data(file)
data = data_object.reshape_binary_data()

#Parameters
downsample = 20
fs = 20000 / downsample #Real signal is 20hz but downsample to 1hz
NFFT = 256 #The length of the signal I want to calcualte the fourier transform of. Has to be a power of 2 for computational efficiency. Helpful comparing signals of different sizes

#Channel selection
c1 = data[0:-1:downsample, 0] #downsampled to speed up multi tapered estimation

#Bandpass Filter
sos = signal.butter(N = 5, Wn = 300, btype = 'lowpass', output ='sos', fs = fs)
filtered_signal = signal.sosfilt(sos, c1)

#Working code for PSD
# def dB(x, out=None):
#     if out is None:
#         return 10 * np.log10(x)
#     else:
#         np.log10(x, out)
#         np.multiply(out, 10, out) #Convert power into decibals which is a log scale
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

#Spectrogram using SIGNAL. Does't work
# f, t, Sxx = signal.spectrogram(c1, fs = fs, window = ('dpss', 5))
# plt.pcolormesh(t, f, Sxx, shading='gouraud')
# plt.show()

#Spectrogram using MATPLOTLIB - Works but still not as good
# NFFT = min(512, len(data))
# spectrum, freqs, t, im = plt.specgram(c1, Fs = fs, window = signal.get_window(('dpss', 3), 256), scale = 'dB') #Spectrogram
# # plt.imshow(im)
# # plt.title("Spectrogram of synthetic multiplexed signal 5hz + 50hz with a fs of 1hz")
# # plt.xlabel('Time (Seconds)')
# # plt.ylabel('Frequency (Hz)')
# plt.ylim(0, 80)
# plt.show()


#
# # #Plots
# fig, (psd) = plt.subplots(1, 1)
# # fig.suptitle("Channel 1, PSD + Spectrogram. Bandpass filter range {} Hz".format(band_pass_range))
#
# # #PSD
# # Pxx, freqs = psd.psd(filtered, scale_by_freq = False) #Power spectrum
#
# Pxx, freqs = psd.psd(filtered) #Power spectrum
# plt.show()

# freqs, psd = signal.welch(filtered)
# plt.figure(figsize=(5, 4))
# plt.plot(freqs, psd)
# plt.title('PSD: power spectral density')
# plt.xlabel('Frequency')
# plt.ylabel('Power')
# plt.tight_layout()
# plt.show()
#
# freqs, times, spectrogram = signal.spectrogram(filtered)
# plt.figure(figsize=(5, 4))
# plt.imshow(spectrogram, aspect='auto', cmap='hot_r', origin='lower')
# plt.title('Spectrogram')
# plt.ylabel('Frequency band')
# plt.xlabel('Time window')
# plt.tight_layout()
# plt.show()
#
# # psd.set_ylim([0, 80])
# # psd.set_ylim([0,30])
# # psd.set_xlim([0,300])
#
# #Specgram
# spectrum, freqs, t, im = spectrogram.specgram(filtered, Fs = fs, scale_by_freq = False) #Spectrogram
# spectrogram.set_ylim(band_pass_range)
# spectrogram.set_xlabel('Time (Seconds)')
# spectrogram.set_ylabel('Frequency (Hz)')
# plt.show()

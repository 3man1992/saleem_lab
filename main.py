from utils import reshape
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

#Load and shape data
file = "/Users/freeman/Documents/saleem_lab/data/R21011_210915_CA1_1.dat"
data_object = reshape.Import_and_Shape_Data(file)
data = data_object.reshape_data()

#Parameters
fs = 20000
block_size = len(data[0])
frame_size = block_size / fs
c1 = data[0]
band_pass_range = [1,300]

#Bandpass Filter
#How to choose the best order / N?
#What does SOS truely mean?
sos = signal.butter(N = 10, Wn = band_pass_range, btype = 'bandpass', output = 'sos', fs = fs)
filtered = signal.sosfilt(sos, c1)

#Plots
fig, (psd, spectrogram) = plt.subplots(2, 1)
fig.suptitle("Channel 1, PSD + Spectrogram. Bandpass filter range {} Hz".format(band_pass_range))
Pxx, freqs = psd.psd(filtered, Fs = fs, scale_by_freq = False) #Power spectrum
psd.set_ylim([0, 80])
psd.set_xlim(band_pass_range)
spectrum, freqs, t, im = spectrogram.specgram(filtered, Fs = fs, scale_by_freq = False) #Spectrogram
spectrogram.set_ylim(band_pass_range)
spectrogram.set_xlabel('Time (Seconds)')
spectrogram.set_ylabel('Frequency (Hz)')
plt.show()

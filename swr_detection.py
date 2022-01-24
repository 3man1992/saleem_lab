#Custom libs
from utils import reshape #Shapes the 1d array of mv into 2d array of [timepoints, channels]

#OS libaries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import time
from scipy import signal

#Core Lib
from ripple_detection import Karlsson_ripple_detector, Kay_ripple_detector
from ripple_detection.simulate import simulate_time
from ripple_detection import filter_ripple_band

#Load and shape data
file = "/Users/freeman/Documents/saleem_folder/data/R21011_210915_CA1_1.dat"
data_object = reshape.Import_and_Shape_Data(file)
data = data_object.reshape_binary_data()

#Paramters
orginal_fs = 20000
fs = 2000
n_samples = len(data[0:-1:10, 0])

#Downsample and channel selection - channel 1
data = data[0:-1:10, 0]

#Bandpass Filter
sos = signal.butter(N = 5, Wn = [150, 250], btype = 'bandpass', output ='sos', fs = fs)
filtered_signal = signal.sosfilt(sos, data)
filtered_signal = np.reshape(filtered_signal, [n_samples, 1])

#Speed of the animal
speed = np.zeros(n_samples) #Assume 0 for now

#Time in 20hz
time = simulate_time(n_samples, fs)

#Detect ripples
Karlsson_ripple_times = Kay_ripple_detector(time, filtered_signal, speed, fs, zscore_threshold=2.0)

#Investigate ripple data
# print("Shape of ripple data", Karlsson_ripple_times.shape)
ripple_list = Karlsson_ripple_times.iloc[0:9].values
figs, axs = plt.subplots(3,3)
figs.suptitle('9 ripples from channel 1')
figs.supxlabel('Seconds')
figs.supylabel('mV')
ripple_index = 0
for i in range(3):
    for x in range(3):
        axs[i, x].plot(time, filtered_signal[:, 0])
        axs[i, x].set_xlim(ripple_list[ripple_index][0], ripple_list[ripple_index][1])
        ripple_index += 1

# print(Karlsson_ripple_times)
# ripple1 = Karlsson_ripple_times.iloc[0].values
# plt.plot(time, filtered_signal[:, 0])
# plt.xlim(ripple1[0], ripple1[1])
plt.show()

#Plt WHOLE ripple detection + LFP signals
# fig, ax = plt.subplots(figsize=(15, 3))
# ax.plot(time, filtered_signal)
# for ripple in Karlsson_ripple_times.itertuples():
#     ax.axvspan(ripple.start_time, ripple.end_time, alpha=0.3, color='red', zorder=10)
# plt.title("Kay ripple detection - Channel 1")
# plt.xlabel('Time in seconds')
# plt.ylabel('Mv')
# plt.show()

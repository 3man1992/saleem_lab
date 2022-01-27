#Custom libs
from utils import reshape #Shapes the 1d array of mv into 2d array of [timepoints, channels]

#OS libaries
import numpy as np
import matplotlib.pyplot as plt
import time
from scipy import signal
from ripple_detection import Karlsson_ripple_detector, Kay_ripple_detector
from ripple_detection.simulate import simulate_time
from ripple_detection import filter_ripple_band

#Load and shape data
file = "/Users/freeman/Documents/saleem_folder/data/tomazzo_data/R21011_210915_CA1_1.dat"
data_object = reshape.Import_and_Shape_Data(file)
data = data_object.reshape_binary_data()

#channels
channel_num = [48,49,18,1,0,50,34,36,3,2,51,32,28,16,4,52] #A single shank from Tomazzo Top to bottom

#Parameters
orginal_fs = 20000
fs = 2000
down_sampling_factor = int(orginal_fs / fs)
n_samples = len(data[0:-1:down_sampling_factor, 0]) #Selecting first channel irrelvant to sample length

#Downsample
data = data[0:-1:down_sampling_factor, :] #Down sample across all channels
print("len of data:", len(data))

#Bandpass Filter for SWRs
sos = signal.butter(N = 5, Wn = 600, btype = 'lowpass', output ='sos', fs = fs)
raw_data = signal.sosfilt(sos, data)
filtered_signal = filter_ripple_band(data)
print("len of filtered signal:", len(filtered_signal))

# #Remove noise from LFP signals to plot raw traces
# sos_1 = signal.butter(N = 5, Wn = [1, 600], btype = 'bandpass', output ='sos', fs = fs)
# raw_LFP_filtered = signal.sosfilt(sos_1, data)

#Speed of the animal
speed = np.zeros(n_samples) #Assume 0 for now

#Time of session
time = simulate_time(n_samples, fs)
print("Time of session in seconds:", time[-1])

#Detect SWRs
Karlsson_ripple_times = Kay_ripple_detector(time, filtered_signal, speed, fs, zscore_threshold=3.0)
ripple_list = Karlsson_ripple_times.values
print()
print("Ripple window times:\n")
print(Karlsson_ripple_times.values)
print()
print("Number of ripples detected:\n", len(Karlsson_ripple_times.values))

#test one ripple against one lfp raw
# fig, axs = plt.subplots(2, sharex=True)
# axs[0].plot(time, filtered_signal[:, channel_num[8]])
# axs[1].plot(time, raw_data[:, channel_num[8]])
# axs[0].set_xlim(ripple_list[0][0], ripple_list[0][1])
# plt.show()

#Plot every ripple that was detected using Kay's method - plot first 20 ripples
for ripple_id in range(20):
    fig, axs = plt.subplots(nrows = 16, ncols = 2, sharex=True)
    #Plot 16 channels
    for channel_id in range(16):
        axs[channel_id][1].plot(time, filtered_signal[:, channel_num[channel_id]], 'k')
        axs[channel_id][1].set_xlim(ripple_list[ripple_id][0] - 0.2, ripple_list[ripple_id][1] + 0.2) #Limit the x axis to the ripple_id window + adding 0.6 seconds to increase viz window
        axs[channel_id][0].plot(time, raw_data[:, channel_num[channel_id]], 'k')
    fig.suptitle('Predicted ripple number:{} across 16 channels from a signle shank. \n Column 1: Raw low pass 600hz LFP - \n Column 2: Bandpass of 150-250hz, detected using Kay et al 2016'.format(ripple_id))
    fig.supxlabel('Seconds')
    fig.supylabel('mV')
    fig.set_size_inches(10, 17) #width and height of image
    plt.savefig("/Users/freeman/Documents/saleem_folder/viz/ripple_num_{}".format(ripple_id), dpi=100)
    # plt.show()
    plt.close(fig)
    print("Single ripple file completed")
print("Program finished")

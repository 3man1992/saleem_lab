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
fs = 5000
down_sampling_factor = int(orginal_fs / fs)
n_samples = len(data[0:-1:down_sampling_factor, 0]) #Selecting first channel irrelvant to sample length

#Downsample
data = data[0:-1:down_sampling_factor, :] #Down sample across all channels
print("len of data:", len(data))

#Bandpass Filter for SWRs
sos = signal.butter(N = 5, Wn = [150, 250], btype = 'bandpass', output ='sos', fs = fs)
filtered_signal = signal.sosfilt(sos, data)
print("len of filtered signal:", len(filtered_signal))

#Remove noise from LFP signals to plot raw traces
sos_1 = signal.butter(N = 5, Wn = [1, 600], btype = 'bandpass', output ='sos', fs = fs)
raw_LFP_filtered = signal.sosfilt(sos_1, data)

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

#Plot every ripple that was detected using Kay's method
for ripple_id in range(len(Karlsson_ripple_times.values)):
    fig, axs = plt.subplots(16, sharex=True)
    #Plot 16 channels
    for channel_id in range(16):
        axs[ripple_id].plot(time, raw_LFP_filtered[:, channel_num[channel_id]])
        axs[channel_id].set_xlim(ripple_list[ripple_id][0], ripple_list[ripple_id][1]) #Limit the x axis to the ripple_id window
    fig.suptitle('Predicted ripple #:{} window, 16 raw traces from single shank'.format(ripple_id))
    fig.supxlabel('Seconds')
    fig.supylabel('mV')
    fig.set_size_inches(10, 17) #width and height of image
    plt.savefig("/Users/freeman/Documents/saleem_folder/viz/ripple_num_{}".format(ripple_id), dpi=100)
    plt.close()
    print("Single ripple file completed")
print("Program finished")

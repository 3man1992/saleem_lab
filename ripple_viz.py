#Libaries
import numpy as np
import matplotlib.pyplot as plt
from ripple_detection.simulate import simulate_time
from ripple_detection import filter_ripple_band
from utils import helper

#Parameters
org_fs = 30000
fs = 2000

#Load pre-saved data
ripple_times = np.load("/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/Dark_day6_2507_19_ripple_times.npy")
matrix = np.load("/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/Dark_day6_2507_19.npy")
matrix = matrix[:, 8:] #select channels
raw_data, n_samples = helper.downsample(matrix, org_fs, fs)
print("The shape of the raw data", raw_data.shape)
num_of_channels = matrix.shape[1]
print("Number of channels: ", num_of_channels)
filtered_signal = filter_ripple_band(raw_data)
print("Signal loaded and filtered")
print("Shape of filtered signal", filtered_signal.shape)

#create time
time = simulate_time(n_samples, fs)
print("Lenght of time array", len(time))

padding = 1000 #Adds 0.5 seconds to index either side

#Plot every ripple that was detected using Kay's method - plot first 20 ripples
for ripple_id in range(50):
    fig, axs = plt.subplots(nrows = num_of_channels, ncols = 2, sharex=True)
    ripple_start_index = int(ripple_times[ripple_id][0] * fs) - padding
    ripple_end_index = int(ripple_times[ripple_id][1] * fs) + padding
    seg_time = time[ripple_start_index :ripple_end_index] #Produces an array of times

    #Plot each channel
    for channel_id in range(num_of_channels):
        signal = filtered_signal[ripple_start_index:ripple_end_index,channel_id]
        raw_signal = raw_data[ripple_start_index:ripple_end_index, channel_id]
        axs[channel_id][0].plot(seg_time, raw_signal, 'k')
        axs[channel_id][1].plot(seg_time, signal, 'k')

    fig.suptitle('Predicted ripple number:{} \n Column 1: Raw LFP - \n Column 2: Bandpass of 150-250hz, detected using Kay et al 2016'.format(ripple_id))
    fig.supxlabel('Seconds')
    fig.supylabel('mV')
    fig.set_size_inches(10, 17) #width and height of image
    plt.savefig("/Users/freeman/Documents/saleem_folder/viz/marta_dark_day_6/ripple_num_{}".format(ripple_id), dpi=100)
    plt.close(fig)
    print("Single ripple file completed")

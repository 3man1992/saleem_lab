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
raw_data, n_samples = helper.downsample(matrix, org_fs, fs)
num_of_channels = matrix.shape[1]
filtered_signal = filter_ripple_band(raw_data)

#create time
time = simulate_time(n_samples, fs)

#Plot every ripple that was detected using Kay's method - plot first 20 ripples
for ripple_id in range(5):
    fig, axs = plt.subplots(nrows = num_of_channels, ncols = 2, sharex=True)
    #Plot each channel
    for channel_id in range(num_of_channels):
        axs[channel_id][1].plot(time, filtered_signal[:, channel_id], 'k')
        axs[channel_id][1].set_xlim(ripple_times[ripple_id][0] - 0.2, ripple_times[ripple_id][1] + 0.2) #Limit the x axis to the ripple_id window + adding 0.6 seconds to increase viz window
        axs[channel_id][0].plot(time, raw_data[:, channel_id], 'k')
    fig.suptitle('Predicted ripple number:{} \n Column 1: Raw LFP - \n Column 2: Bandpass of 150-250hz, detected using Kay et al 2016'.format(ripple_id))
    fig.supxlabel('Seconds')
    fig.supylabel('mV')
    fig.set_size_inches(10, 17) #width and height of image
    plt.savefig("/Users/freeman/Documents/saleem_folder/viz/marta_dark_day_6/ripple_num_{}".format(ripple_id), dpi=100)
    # plt.show() #Show file
    plt.close(fig)
    print("Single ripple file completed")

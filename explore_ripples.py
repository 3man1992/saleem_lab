"""A script that runs through ripple times and plots raw trace vs filtered ripple Band
per channel"""

# OS Libaries
import matplotlib.pyplot as plt
import numpy as np
from ripple_detection.simulate import simulate_time
from ripple_detection import filter_ripple_band

# Custome libaries
from meta_data import Meta
from utils import helper


# Hyperparameters
org_fs = 30000
fs = 6000
padding = 500

# Load data
obj = Meta()
session = "Day_6_Dark"
pre_sleep_ripple_times = np.load(obj.dictionary[session]["pre"])
post_sleep_ripple_times = np.load(obj.dictionary[session]["post"])
lfp = np.load(obj.dictionary[session]["lfp"])
mat_file = obj.dictionary[session]["mat"]

# Downsample LFP data to make it faster to process
downsampled_lfp_matrix, n_samples = helper.downsample(lfp, org_fs, desired_fs=fs)

hippocampus_lfp = downsampled_lfp_matrix[:, slice(obj.dictionary[session]["hpc_chans"][0],
                                                  obj.dictionary[session]["hpc_chans"][-1] + 1,
                                                  1)]

# Filter data for ripple visulisation
swr_hippocampus = filter_ripple_band(hippocampus_lfp)

# Create time
time = simulate_time(n_samples, fs)

# For each ripple plot raw and ripple trace, each column is a channel
for ripple_id in range(10):
    fig, axs = plt.subplots(nrows=2, ncols=4, sharex=True)

    # Outline indexs
    ripple_start_index = int(pre_sleep_ripple_times[ripple_id][0] * fs) - padding
    ripple_end_index = int(pre_sleep_ripple_times[ripple_id][1] * fs) + padding
    seg_time = time[ripple_start_index:ripple_end_index]

    # Plot each of the four channels
    for channel_index in range(4):
        ripple_signal = swr_hippocampus[ripple_start_index:ripple_end_index, channel_index]
        raw_signal = hippocampus_lfp[ripple_start_index:ripple_end_index, channel_index]
        axs[0][channel_index].plot(seg_time, raw_signal, 'k')
        axs[0][channel_index].axvspan(pre_sleep_ripple_times[ripple_id][0],
                                      pre_sleep_ripple_times[ripple_id][1],
                                      alpha=0.3,
                                      color='red',
                                      zorder=10)
        axs[0][channel_index].set_xlabel('Seconds')
        axs[0][channel_index].margins(x=0)
        axs[1][channel_index].plot(seg_time, ripple_signal, 'k')
        axs[1][channel_index].set_xlabel('Seconds')
        axs[1][channel_index].axvspan(pre_sleep_ripple_times[ripple_id][0],
                                      pre_sleep_ripple_times[ripple_id][1],
                                      alpha=0.3,
                                      color='red',
                                      zorder=10)
        axs[1][channel_index].margins(x=0)
    fig.suptitle('Predicted ripple window using Kay et al 2016 algorithm \n Predicted ripple number:{}'.format(ripple_id), fontweight='bold')
    plt.show()

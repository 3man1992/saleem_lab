from mt_power_spec import power_spectral_density
import numpy as np
import matplotlib.pyplot as plt
from utils import helper
from ripple_detection.simulate import simulate_time
from ripple_detection import filter_ripple_band
import ghostipy as gsp
from visulisations.spectrogram_funcs import cwt, wsst

#Parameters
org_fs = 30000
fs = 2000
padding = 2000 #Adds 0.5 seconds to index either side

#Load data and preprocess
ripple_times = np.load("/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/Dark_day6_2507_19_ripple_times.npy")
matrix = np.load("/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/Dark_day6_2507_19.npy")
hpc_data = matrix[:, 8:] #select channels
visual_data = matrix[:, :4] #select channels
num_of_channels = hpc_data.shape[1]
raw_data, n_samples = helper.downsample(hpc_data, org_fs, fs)
raw_visual_data, visual_n_samples = helper.downsample(visual_data, org_fs, fs)
filtered_signal = filter_ripple_band(raw_data)
filtered_visual = filter_ripple_band(raw_visual_data)

#create time
time = simulate_time(n_samples, fs)

for ripple_id in range(50):
    fig, axs = plt.subplots(nrows = num_of_channels, ncols = 4)
    ripple_start_index = int(ripple_times[ripple_id][0] * fs)
    ripple_end_index = int(ripple_times[ripple_id][1] * fs)
    seg_time = time[ripple_start_index :ripple_end_index] #Produces an array of times

    #Plot each channel
    for channel_id in range(num_of_channels):
        #hPC data
        signal = filtered_signal[ripple_start_index:ripple_end_index,channel_id]
        raw_signal = raw_data[ripple_start_index:ripple_end_index, channel_id]

        #vc data
        visual_signal = filtered_visual[ripple_start_index:ripple_end_index,channel_id]
        raw_signal = raw_visual_data[ripple_start_index:ripple_end_index, channel_id]

        #Plot raw trace
        axs[channel_id][0].plot(seg_time, raw_signal, 'k')
        axs[0][0].set_title('Raw LFP - HPC - ripple window')

        #Plot ripple
        axs[channel_id][1].plot(seg_time, signal, 'k')
        axs[0][1].set_title('150-250hz bp ripple window - hpc')

        #Spectrogram for hpc
        t_wsst, f_wsst, psd_wsst, kwargs_dict = cwt(signal, fs)
        axs[channel_id][2].pcolormesh(t_wsst, f_wsst, psd_wsst, **kwargs_dict)
        axs[0][2].set_title('WSST for hpc - ripple window')

        #spectrogram for vc
        t_wsst, f_wsst, psd_wsst, kwargs_dict = cwt(raw_visual_data[ripple_start_index - padding:ripple_end_index + padding, channel_id], fs)
        axs[channel_id][3].pcolormesh(t_wsst, f_wsst, psd_wsst, **kwargs_dict)
        axs[0][3].set_title('WSST for visual cortex +1/-1s across ripple window')

    #Set labels
    fig.supylabel('Hz')
    fig.supxlabel('Time (s)')
    fig.set_size_inches(14, 17) #width and height of image
    fig.suptitle('Predicted ripple number:{} - HPC vs VC'.format(ripple_id))
    plt.savefig("/Users/freeman/Documents/saleem_folder/viz/marta_dark_day_6/vc_VS_HPC_ripple_num_{}".format(ripple_id), dpi=100)
    plt.show()
    # plt.close(fig)
    print("Single spectorgram file completed")

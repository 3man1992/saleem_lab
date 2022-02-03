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
padding = 1000 #Adds 0.5 seconds to index either side

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
    fig, axs = plt.subplots(nrows = 3, ncols = 2)
    ripple_start_index = int(ripple_times[ripple_id][0] * fs) - padding
    ripple_end_index = int(ripple_times[ripple_id][1] * fs) + padding
    seg_time = time[ripple_start_index :ripple_end_index] #Produces an array of times

    #hPC data
    hpc_signal = filtered_signal[ripple_start_index:ripple_end_index, 0]
    raw__HPC_signal = raw_data[ripple_start_index:ripple_end_index, 0]

    #vc data
    visual_signal = filtered_visual[ripple_start_index:ripple_end_index, 0]
    raw_viz_signal = raw_visual_data[ripple_start_index:ripple_end_index, 0]

    #Hippocampus plots----------------------
    #Plot the raw LFP trace for the HPC
    axs[0][0].plot(seg_time, raw__HPC_signal, 'k')
    axs[0][0].set_title('raw LFP trace for the HPC')
    axs[0][0].margins(x=0)
    axs[0][0].get_xaxis().set_visible(False)

    #Plot the CWT on the filtered HPC LFP signal
    t_wsst, f_wsst, psd_wsst, kwargs_dict = cwt(hpc_signal,
                                                fs,
                                                freq_range = [1, 500])
    axs[1][0].pcolormesh(t_wsst, f_wsst, psd_wsst, **kwargs_dict)
    axs[1][0].set_title('CWT on the 150-250hz bandpass HPC LFP signal')
    axs[1][0].get_xaxis().set_visible(False)

    #PLot the filtered LFP on the ripple
    axs[2][0].plot(seg_time, hpc_signal, 'k')
    axs[2][0].margins(x=0)
    axs[2][0].set_title('Ripple trace - HPC - LFP - Bandpass 150-250hz')

    #VC plots -------------------------------
    #Plot raw trace on the vc
    axs[0][1].plot(seg_time, raw_viz_signal, 'k')
    axs[0][1].set_title('raw LFP trace for the VC')
    axs[0][1].margins(x=0)


    #CWT plot the unfiltered visual LFP
    t_wsst, f_wsst, psd_wsst, kwargs_dict = cwt(raw_viz_signal,
                                                fs,
                                                freq_range = [1, 500])
    axs[1][1].pcolormesh(t_wsst, f_wsst, psd_wsst, **kwargs_dict)
    axs[1][1].set_title('CWT on the raw VC LFP signal')

    #Hide blank plot
    axs[2][1].axis('off')

    #Set labels
    fig.supylabel('Hz')
    fig.supxlabel('Time (s)')
    # fig.set_size_inches(14, 17) #width and height of image
    fig.suptitle('Predicted ripple number:{} - HPC vs VC'.format(ripple_id))
    plt.savefig("/Users/freeman/Documents/saleem_folder/viz/marta_dark_day_6/vc_VS_HPC_ripple_num_{}".format(ripple_id), dpi=100)
    plt.show()
    # plt.close(fig)
    print("Single spectorgram file completed")

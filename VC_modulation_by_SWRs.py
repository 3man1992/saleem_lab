# from mt_power_spec import power_spectral_density
# import ghostipy as gsp
# from visulisations.mua import filt_mua, gaussian_smooth, threshold

#Custom Libaries
from utils import helper
from utils.meta_data import Meta
from visulisations.spectrogram_funcs import cwt, wsst

#OS Libaries
from ripple_detection.simulate import simulate_time
import numpy as np
import matplotlib.pyplot as plt
from ripple_detection import filter_ripple_band

#Load data
obj   = Meta()
base_path = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/"
pre_sleep_ripple_times = np.load(base_path + obj.light["Day_7_Light"]["pre"])
pre_sleep_LFP = np.load(base_path + obj.light["Day_7_Light"]["lfp"])

#Parameters
org_fs = 30000 #What is the original fs of the ephys recording device
fs = 6000 #What do you want to downsample the data to
padding = 1500 #What extra time do you want on ripple window - If fs is 3000 then 1500 is half a second either side

#Downsample LFP data to make it faster to process
downsampled_lfp_matrix, n_samples = helper.downsample(pre_sleep_LFP,
                                                      org_fs,
                                                      desired_fs = fs)

#Select Visual Cortex and Hippocampal channels
visual_lfp = downsampled_lfp_matrix[:,
                                    slice(obj.light["Day_7_Light"]["vc_chans"][0],
                                          obj.light["Day_7_Light"]["vc_chans"][-1] + 1,
                                          1)]
hippocampus_lfp = downsampled_lfp_matrix[:,
                                         slice(obj.light["Day_7_Light"]["hpc_chans"][0],
                                               obj.light["Day_7_Light"]["hpc_chans"][-1] + 1,
                                               1)]

#Filter data for ripple visulisation
swr_visual = filter_ripple_band(visual_lfp)
swr_hippocampus = filter_ripple_band(hippocampus_lfp)

#Simulate time
time = simulate_time(n_samples, fs)

#Plot per ripple
for ripple_id in range(1):
    #Define a 4 by 4 grid
    fig, axs = plt.subplots(nrows = 4, ncols = 4, sharey = 'row')

    #Create ripple windows and padding for x axis
    ripple_start_index = int(pre_sleep_ripple_times[ripple_id][0] * fs) - padding
    ripple_end_index = int(pre_sleep_ripple_times[ripple_id][1] * fs) + padding
    seg_time = time[ripple_start_index : ripple_end_index]

    #Raw data for one channel
    raw_hpc_lfp = hippocampus_lfp[ripple_start_index:ripple_end_index, 0]
    raw_vc_lfp  = visual_lfp[ripple_start_index:ripple_end_index, 0]

    #SWRs for one cahnnel
    swr_visual = swr_visual[ripple_start_index:ripple_end_index, 0]
    swr_hippocampus = swr_hippocampus[ripple_start_index:ripple_end_index, 0]

    #Plot the first row of raw LFP data
    axs[0][0].plot(seg_time, raw_hpc_lfp, 'k')
    axs[0][0].set_title('raw LFP : HPC')
    axs[0][0].margins(x=0)
    axs[0][0].set_ylabel('mV')
    axs[0][0].get_xaxis().set_visible(False)

    axs[0][1].plot(seg_time, raw_vc_lfp, 'k')
    axs[0][1].set_title('raw LFP : VC')
    axs[0][1].margins(x=0)
    axs[0][1].get_yaxis().set_visible(False)
    axs[0][1].get_xaxis().set_visible(False)

    #Plot the second row containing CWT within the MUA range
    t_cwt, f_cwt, psd_cwt, kwargs_dict = cwt(raw_hpc_lfp,
                                             fs,
                                             freq_range = [500, 3000])
    axs[1][0].pcolormesh(t_cwt, f_cwt, psd_cwt, **kwargs_dict)
    axs[1][0].set_title('CWT 500-3000hz : HPC')
    axs[1][0].get_xaxis().set_visible(False)
    axs[1][0].set_ylabel('hZ')

    t_cwt, f_cwt, psd_cwt, kwargs_dict = cwt(raw_vc_lfp,
                                             fs,
                                             freq_range = [500, 3000])
    axs[1][1].pcolormesh(t_cwt, f_cwt, psd_cwt, **kwargs_dict)
    axs[1][1].set_title('CWT 500-3000hz : VC')
    axs[1][1].get_xaxis().set_visible(False)

    #Plot the third row containing the filtered ripple band
    axs[2][0].plot(seg_time, swr_hippocampus, 'k')
    axs[2][0].margins(x=0)
    axs[2][0].set_title('Ripple 150-250hz : HPC')
    axs[2][0].set_ylabel('mV')
    axs[2][0].get_xaxis().set_visible(False)

    axs[2][1].plot(seg_time, swr_visual, 'k')
    axs[2][1].margins(x=0)
    axs[2][1].set_title('Ripple 150-250hz : VC')
    axs[2][1].get_xaxis().set_visible(False)

    #Plot the graphs
    plt.show()

# #Mua code
# filtered_data = filt_mua(lfp_data = downsampled_lfp_matrix,
#                          fs = mua_fs)
# mua_activity  = threshold(filtered_data)
# smoothed_mua = gaussian_smooth(mua_activity)
#
# # smoothed_data = gaussian_smooth(data = filtered_data,
# #                                 sampling_frequency = mua_fs)
#
# #PLotting
# mua_time = simulate_time(n_samples, mua_fs)
# plt.plot(mua_time, smoothed_mua[:,0])
# plt.xlabel("Seconds")
# plt.title("MUA activity, smoothed to 50ms, threshold 4SD, fs = 6kHz")
# plt.show()
#
# hpc_data = lfp_matrix[:, 8:] #select channels
# visual_data = lfp_matrix[:, :4] #select channels
# num_of_channels = hpc_data.shape[1]
# raw_data, n_samples = helper.downsample(hpc_data, org_fs, fs)
# raw_visual_data, visual_n_samples = helper.downsample(visual_data, org_fs, fs)
# filtered_signal = filter_ripple_band(raw_data)
# filtered_visual = filter_ripple_band(raw_visual_data)
#
# #create time
# time = simulate_time(n_samples, fs)
#
# for ripple_id in range(50):
#     fig, axs = plt.subplots(nrows = 3, ncols = 2)
#     ripple_start_index = int(ripple_times[ripple_id][0] * fs) - padding
#     ripple_end_index = int(ripple_times[ripple_id][1] * fs) + padding
#     seg_time = time[ripple_start_index :ripple_end_index] #Produces an array of times
#
#     #hPC data
#     hpc_signal = filtered_signal[ripple_start_index:ripple_end_index, 0]
#     raw__HPC_signal = raw_data[ripple_start_index:ripple_end_index, 0]
#
#     #vc data
#     visual_signal = filtered_visual[ripple_start_index:ripple_end_index, 0]
#     raw_viz_signal = raw_visual_data[ripple_start_index:ripple_end_index, 0]
#
#     #Hippocampus plots----------------------
#     #Plot the raw LFP trace for the HPC
#     axs[0][0].plot(seg_time, raw__HPC_signal, 'k')
#     axs[0][0].set_title('raw LFP trace for the HPC')
#     axs[0][0].margins(x=0)
#     axs[0][0].get_xaxis().set_visible(False)
#
#     #Plot the CWT on the filtered HPC LFP signal
#     t_wsst, f_wsst, psd_wsst, kwargs_dict = cwt(hpc_signal,
#                                                 fs,
#                                                 freq_range = [1, 500])
#     axs[1][0].pcolormesh(t_wsst, f_wsst, psd_wsst, **kwargs_dict)
#     axs[1][0].set_title('CWT on the 150-250hz bandpass HPC LFP signal')
#     axs[1][0].get_xaxis().set_visible(False)
#
#     #PLot the filtered LFP on the ripple
#     axs[2][0].plot(seg_time, hpc_signal, 'k')
#     axs[2][0].margins(x=0)
#     axs[2][0].set_title('Ripple trace - HPC - LFP - Bandpass 150-250hz')
#
#     #VC plots -------------------------------
#     #Plot raw trace on the vc
#     axs[0][1].plot(seg_time, raw_viz_signal, 'k')
#     axs[0][1].set_title('raw LFP trace for the VC')
#     axs[0][1].margins(x=0)
#
#
#     #CWT plot the unfiltered visual LFP
#     t_wsst, f_wsst, psd_wsst, kwargs_dict = cwt(raw_viz_signal,
#                                                 fs,
#                                                 freq_range = [1, 500])
#     axs[1][1].pcolormesh(t_wsst, f_wsst, psd_wsst, **kwargs_dict)
#     axs[1][1].set_title('CWT on the raw VC LFP signal')
#
#     #Hide blank plot
#     axs[2][1].axis('off')
#
#     #Set labels
#     fig.supylabel('Hz')
#     fig.supxlabel('Time (s)')
#     # fig.set_size_inches(14, 17) #width and height of image
#     fig.suptitle('Predicted ripple number:{} - HPC vs VC'.format(ripple_id))
#     plt.savefig("/Users/freeman/Documents/saleem_folder/viz/marta_dark_day_6/vc_VS_HPC_ripple_num_{}".format(ripple_id), dpi=100)
#     plt.show()
#     # plt.close(fig)
#     print("Single spectorgram file completed")

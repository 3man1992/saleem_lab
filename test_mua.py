#Custom Libaries
from utils import helper
from utils.meta_data import Meta
from visulisations.mua import filt_mua, threshold, calculate_mua

#OS Libaries
from ripple_detection.simulate import simulate_time
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

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

#Select HPC data
hippocampus_lfp = downsampled_lfp_matrix[:,
                                         slice(obj.light["Day_7_Light"]["hpc_chans"][0],
                                               obj.light["Day_7_Light"]["hpc_chans"][-1] + 1,
                                               1)]
#Simulate time
time = simulate_time(n_samples, fs)

#Mua calculations
hippocampus_mua = calculate_mua(hippocampus_lfp[:, 0], fs)

#Plot per ripple
for ripple_id in range(1):
    #Create ripple windows and padding for x axis
    ripple_start_index = int(pre_sleep_ripple_times[ripple_id][0] * fs) - padding
    ripple_end_index = int(pre_sleep_ripple_times[ripple_id][1] * fs) + padding
    seg_time = time[ripple_start_index : ripple_end_index]

    #Segment mua activity
    mua = hippocampus_mua[ripple_start_index:ripple_end_index]

    #Plot
    plt.plot(seg_time, mua)
    plt.show()

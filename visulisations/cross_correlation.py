"""Select two channels to get around zsh: killedw
use pandas"""

from visulisations.mua import calculate_mua, bin_mua
from visulisations.temporal_lag import scatter_temp_coeff, whole_session_plot
import numpy as np
from utils import helper
import collections
from ripple_detection.simulate import simulate_time
import pandas as pd
import matplotlib.pyplot as plt

#Hyperparamters
org_fs = 30000
new_fs = 6000

#Dark Data files
M_BLU_DARK_day_10_v2 = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/MBLU_Dark_Day10_090119.npy"
Q_blu_dark_day_6_v1 = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/Dark_day6_2507_19.npy"
Q_blu_dark_day_9_v1 = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/QBLU_Dark_Day9_290719.npy"

#Light data files
O_BLU_LIGHT_day_9_v2 = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/OBLU_YMaze_Day9_170519.npy"
Q_BLU_light_day_3_v1 = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/Ymaze_Day3_220719.npy"
Q_blue_light_day_8_v1 = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/QBLU_YMaze_Day8_280719.npy"

#Load data
dark_data_lfp_matrix = np.load(M_BLU_DARK_day_10_v2)
light_data_lfp_matrix = np.load(O_BLU_LIGHT_day_9_v2)

#Read out
print("------")
print("Length of dark data", len(dark_data_lfp_matrix[:, 0]))
print("Length of ligth data", len(light_data_lfp_matrix[:, 0]))
print("------")

#Downsample
print("Downsampling your data")
down_dark_data_lfp_matrix, dark_n_samples  = helper.downsample(dark_data_lfp_matrix, org_fs, new_fs)
down_light_data_lfp_matrix, n_samples = helper.downsample(light_data_lfp_matrix, org_fs, new_fs)

#Calculate mua
print("Calculating mua activity for dark and light sessions")
dark_mua  = calculate_mua(down_dark_data_lfp_matrix, new_fs)
light_mua = calculate_mua(down_light_data_lfp_matrix, new_fs)

#Compute values for scatter
light_lag_values, light_lag_max, dark_lag_values, dark_lag_max = whole_session_plot(dark_mua, light_mua)

#Plot session
# plt.scatter(light_lag_values, light_lag_max, color='r', label='light conditions')
# plt.scatter(dark_lag_values, dark_lag_max, color='b', label='dark conditions')
# plt.legend()
# plt.xlabel('Time lag in 10ms')
# plt.ylabel('Argmax coeff')
# plt.axvline(x=0, color='k', linestyle ='--')
# plt.show()

#Segment Analysis
#Select sessions from Martha data - Use this logic below to segment time by task structure
# pre_sleep = slice(0, 60 * 6000 * 45)
# task = slice(60 * 6000 * 50, (60 * 6000 * 50) + (60 * 6000 * 40))
# post_sleep = slice((60 * 6000 * 50) + (60 * 6000 * 40) + 60 * 6000 * 10, -1)
# task_structures = [pre_sleep, task, post_sleep]
#
# print("Split data then compute temp lag")
# fig, axs = plt.subplots(nrows = 3, sharex = True)
# index = 0
# segments = ['presleep', 'task', 'postsleep']
# for segment in task_structures:
#     print("\nSegment: {} \n".format(segments[index]))
#     #Binning mua activity into frames of 10ms as per Ji and Wilson
#     #60 samples = 10ms
#     binned_dark_data =  bin_mua(dark_mua[segment, :], 60).to_numpy() #change second param for different bin size
#     binned_light_data = bin_mua(light_mua[segment, :], 60).to_numpy() #change second param for different bin size
#
#     print("Binned dark data has shape: {} and length {}". format(binned_dark_data .shape, len(binned_dark_data)))
#     print("Binned light data has shape: {} and length {}". format(binned_light_data .shape, len(binned_light_data)))
#
#     #Create scatter by inputting binned data from two conditions and number of channels for comparison
#     light_lag_values, light_lag_max, dark_lag_values, dark_lag_max = scatter_temp_coeff(binned_dark_data,
#                                                                                         binned_light_data,
#                                                                                         8)
#     #Plotting logic
#     axs[index].scatter(light_lag_values, light_lag_max, color='r', label='light conditions')
#     axs[index].scatter(dark_lag_values, dark_lag_max, color='b', label='dark conditions')
#     axs[index].axvline(x=0, color='k', linestyle ='--')
#     axs[0].set_title('Pre-sleep')
#     axs[1].set_title('Task')
#     axs[2].set_title('Post-sleep')
#     axs[2].set_xlabel('Time lag in 10ms')
#     axs[1].set_ylabel('Max temporal coefficient')
#     index += 1
#
# plt.legend()
# plt.show()

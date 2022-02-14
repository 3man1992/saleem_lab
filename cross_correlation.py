"""Select two channels to get around zsh: killedw
use pandas"""

from visulisations.mua import calculate_mua, bin_mua
import numpy as np
from utils import helper
import collections
from ripple_detection.simulate import simulate_time
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

#Hyperparamters
org_fs = 30000
new_fs = 6000

#Load data
dark_data_lfp_matrix = np.load("/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/Dark_day6_2507_19.npy")
light_data_lfp_matrix = np.load("/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/Ymaze_Day3_220719.npy")

#Downsample
print("Downsampling your data")
down_dark_data_lfp_matrix, dark_n_samples  = helper.downsample(dark_data_lfp_matrix, org_fs, new_fs)
down_light_data_lfp_matrix, n_samples = helper.downsample(light_data_lfp_matrix, org_fs, new_fs)

#Calculate mua
print("Calculating mua activity for dark and light sessions")
dark_mua  = calculate_mua(down_dark_data_lfp_matrix, new_fs)
light_mua = calculate_mua(down_light_data_lfp_matrix, new_fs)

#Select sessions from Martha data
# pre_sleep = [0 : 60 * 6000 * 45]
# task = [60 * 6000 * 50 : (60 * 6000 * 50) + (60 * 6000 * 40)]
# post_sleep = [(60 * 6000 * 50) + (60 * 6000 * 40) + 60 * 6000 * 10:]

#Binning mua activity into frames of 10ms as per Ji and Wilson
#60 samples = 10ms
binned_dark_data =  bin_mua(dark_mua [(60 * 6000 * 50) + (60 * 6000 * 40) + 60 * 6000 * 10:, :], 60).to_numpy() #change second param for different bin size
binned_light_data = bin_mua(light_mua[(60 * 6000 * 50) + (60 * 6000 * 40) + 60 * 6000 * 10:, :], 60).to_numpy() #change second param for different bin size

#Set channel indexs for plotting
visual_channels = [0, 1, 2, 3, 4, 5, 6, 7]
hippocampal_channels = [8, 9, 10, 11]

print("###Commence tag lag calculations###")

#Define tag lag calc func
bin_window = 1000 #This sets window to -500ms either side of 0 lag. 100 sets 1 second either side
def time_lag_coords(binned_data, channel):
    #Assume highest coord is within 50ms range
    #Also return index of max arg for plotting vertical line
    dark_corrcoeffs_forward = sm.tsa.stattools.ccf(binned_data[:,visual_channels[channel]],
                                                   binned_data[:,hippocampal_channels[channel]])
    dark_corrcoeffs_back =    sm.tsa.stattools.ccf(binned_data[:,hippocampal_channels[channel]],
                                                   binned_data[:,visual_channels[channel]])
    x = np.arange(-bin_window, bin_window, 1) #Creates a window from -1s to 1s
    first_component = dark_corrcoeffs_back[1:bin_window]
    reversed_first_component = first_component[::-1]
    y = list(reversed_first_component) + list(dark_corrcoeffs_forward[0:bin_window + 1])
    argmax = np.argmax(np.asarray(y))
    arg_max_plot_x = x[argmax]
    return(x, y, arg_max_plot_x)

def bar_chart_comp():
    light = {}
    dark  = {}
    for channel in range(3):
        dark_x, dark_y, arg_max_plot_x    = time_lag_coords(binned_dark_data, channel)
        light_x, light_y, arg_max_plot_xx = time_lag_coords(binned_light_data, channel)
        light[channel] = arg_max_plot_xx
        dark[channel]  = arg_max_plot_x
    x = list(light.values())
    y = list(dark.values())
    print(y)
    print(x)
    x = np.average(x)
    y = np.average(y)
    print(x)
    print(y)
    conditions = ["light", "dark"]
    avg_temp_coord = [x, y]
    print(avg_temp_coord)
    fig = plt.figure()
    plt.bar(conditions, avg_temp_coord)
    plt.margins(x=0)
    fig.supylabel('Temporal delay (10ms)')
    fig.suptitle("Post-Sleep: Temporal lag max coefficient between HPC and VC across channels \n Positive lag is hpc preceding vc \n Negative lag is vc preceding hpc")
    plt.show()

bar_chart_comp()

#Plotting four channel comparisons
fig, axs = plt.subplots(nrows = 2, ncols = 3, sharey = True)
for channel in range(3):
    #Dark conditions
    dark_x, dark_y, arg_max_plot_x = time_lag_coords(binned_dark_data, channel)
    axs[0][channel].plot(dark_x, dark_y, 'k')
    axs[0][channel].axvline(0, color = 'k', linestyle ='--')
    axs[0][channel].axvline(arg_max_plot_x, color = 'r')
    axs[0][channel].margins(x=0)
    axs[0][channel].set_title('Channel: {}'.format(channel))
    axs[0][0].set_ylabel("Dark Conditions", size = 'large')

    #Light conditions
    light_x, light_y, arg_max_plot_xx = time_lag_coords(binned_light_data, channel)
    axs[1][channel].plot(light_x, light_y, 'k')
    axs[1][channel].axvline(0, color = 'k', linestyle ='--')
    axs[1][channel].axvline(arg_max_plot_xx, color = 'r')
    axs[1][channel].margins(x=0)
    axs[1][0].set_ylabel("Light Conditions", size = 'large')
fig.tight_layout()
fig.supylabel('Coeff')
fig.supxlabel('Time (bins of 10mS)')
fig.suptitle("Pre-Sleep: Temporal lag coefficients between HPC and VC across channels \n Positive lag is hpc preceding vc")
plt.show()
plt.savefig("/Users/freeman/Documents/saleem_folder/viz/temporal_coordination")

# #Cross correleation functions
# #time lag
# dark_corrcoeffs = sm.tsa.stattools.ccf(binned_dark_data[:,0], binned_dark_data[:,1])
# dark_positive_lag = np.argmax(dark_corrcoeffs)
# print("Best time lag for dark coeff", dark_positive_lag)
# print('Value of dark coeff', dark_corrcoeffs[dark_positive_lag])
#
# light_corrcoeffs = sm.tsa.stattools.ccf(binned_light_data[:,0], binned_light_data[:,1])
# light_positive_lag = np.argmax(light_corrcoeffs)
# print("Best time lag for light coeff", light_positive_lag)
# print('Value of light coeff', light_corrcoeffs[light_positive_lag])

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

#Binning mua activity into frames of 10ms as per Ji and Wilson
#60 samples = 10ms
binned_dark_data = bin_mua(dark_mua, 60).to_numpy() #change second param for different bin size
binned_light_data = bin_mua(light_mua, 60).to_numpy() #change second param for different bin size

#Set channel indexs for plotting
visual_channels = [0, 1, 2, 3, 4, 5, 6, 7]
hippocampal_channels = [8, 9, 10, 11]

print("###Commence tag lag calculations###")

#Define tag lag calc func
def time_lag_coords(binned_data, channel):
    #Assume highest coord is within 50ms range
    #Also return index of max arg for plotting vertical line
    dark_corrcoeffs_forward = sm.tsa.stattools.ccf(binned_data[:,visual_channels[channel]],
                                                   binned_data[:,hippocampal_channels[channel]])
    dark_corrcoeffs_back =    sm.tsa.stattools.ccf(binned_data[:,hippocampal_channels[channel]],
                                                   binned_data[:,visual_channels[channel]])
    x = [-10, -9, -8, -7, -6, -5,-4,-3,-3,-2,-1,0,1,2,3,4,5, 6,7,8,9,10]
    first_component = dark_corrcoeffs_back[1:12]
    reversed_first_component = first_component[::-1]
    y = list(reversed_first_component) + list(dark_corrcoeffs_forward[0:11])
    y = [float(i)/sum(y) for i in y] #Normalise y
    argmax = np.argmax(np.asarray(y))
    arg_max_plot_x = y[argmax]
    return(x, y, arg_max_plot_x)

#Plotting four channel comparisons
fig, axs = plt.subplots(nrows = 4, ncols = 2, sharex = True, sharey = True)
for channel in range(4):
    dark_x, dark_y, arg_max_plot_x = time_lag_coords(binned_dark_data, channel)
    axs[channel][0].plot(dark_x, dark_y, 'k')
    axs[channel][0].axvline(0, color = 'k', linestyle ='--')
    axs[channel][0].axvline(arg_max_plot_x, color = 'r')
    axs[0][0].margins(x=0)
    axs[0][0].set_title('Dark conditions')
    light_x, light_y, arg_max_plot_x = time_lag_coords(binned_light_data, channel)
    axs[channel][1].plot(light_x, light_y, 'k')
    axs[channel][1].axvline(0, color = 'k', linestyle ='--')
    axs[channel][1].axvline(arg_max_plot_x, color = 'r')
    axs[0][1].margins(x=0)
    axs[0][1].set_title('Light conditions')
fig.supylabel('Coeff')
fig.supxlabel('Time (bins of 10mS)')
fig.suptitle("Temporal lag coefficients between HPC and VC across channels")
plt.show()
plt.savefig("/Users/freeman/Documents/saleem_folder/viz/temporal_coordination")

#Cross correleation functions
#time lag
dark_corrcoeffs = sm.tsa.stattools.ccf(binned_dark_data[:,0], binned_dark_data[:,1])
dark_positive_lag = np.argmax(dark_corrcoeffs)
print("Best time lag for dark coeff", dark_positive_lag)
print('Value of dark coeff', dark_corrcoeffs[dark_positive_lag])

light_corrcoeffs = sm.tsa.stattools.ccf(binned_light_data[:,0], binned_light_data[:,1])
light_positive_lag = np.argmax(light_corrcoeffs)
print("Best time lag for light coeff", light_positive_lag)
print('Value of light coeff', light_corrcoeffs[light_positive_lag])

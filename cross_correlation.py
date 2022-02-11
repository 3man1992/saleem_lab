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
# visual_channel = 0
# hpc_channel = 8
# visual_channel = 1
# # hpc_channel = 9
# visual_channel = 2
# hpc_channel = 10
# visual_channel = 7
# hpc_channel = 10

dark_mua  = calculate_mua(down_dark_data_lfp_matrix, new_fs)
light_mua = calculate_mua(down_light_data_lfp_matrix, new_fs)

print("mua finished")

#Binning mua activity into frames of 10ms as per Ji and Wilson
#60 samples = 10ms
binned_dark_data = bin_mua(dark_mua, 60).to_numpy() #change second param for different bin size
binned_light_data = bin_mua(light_mua, 60).to_numpy() #change second param for different bin size



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

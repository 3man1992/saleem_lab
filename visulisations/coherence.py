from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
from utils import helper

#Load data
lfp_matrix = np.load("/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/Dark_day6_2507_19.npy")

#hyperparameters
org_fs = 30000
fs = 6000

#downsample data
downsampled_lfp_matrix, n_samples = helper.downsample(lfp_matrix,
                                                      org_fs,
                                                      desired_fs = fs)

print("hello")

hpc_data = downsampled_lfp_matrix[:, 8:] #select last four channels of data which is one tetrode in hpc
visual_data = downsampled_lfp_matrix[:, 0:4] #select first 4 channels which is one tetrode in VC

#Plot the coherence
f, Cxy = signal.coherence(hpc_data[:, 0], visual_data[:, 0], fs, nperseg=1024) #set axis to 0 for across channels
plt.semilogy(f, Cxy)
plt.xlim([0, 100])
plt.xlabel('frequency [Hz]')
plt.ylabel('Coherence')
plt.show()

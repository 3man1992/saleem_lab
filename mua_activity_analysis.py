# Custom Libaries
from meta_data import Meta
from visulisations.mua import calculate_mua
from utils import helper

# OS Libraries
import numpy as np
import matplotlib.pyplot as plt

# Hyper parameters
org_fs = 30000  # What is the original fs of the ephys recording device
fs = 6000

# Load data
obj = Meta()
session = "Day_6_Dark"
lfp = np.load(obj.dictionary[session]["lfp"])
mat_file = obj.dictionary[session]["mat"]
vc_chans = obj.dictionary[session]["vc_chans"]
hpc_chans = obj.dictionary[session]["hpc_chans"]

# Downsample LFP data to make it faster to process
downsampled_lfp_matrix, n_samples = helper.downsample(lfp,
                                                      org_fs,
                                                      desired_fs=fs)


# Select Visual Cortex and Hippocampal channels
visual_lfp = downsampled_lfp_matrix[:, slice(obj.dictionary[session]["vc_chans"][0],
                                             obj.dictionary[session]["vc_chans"][-1] + 1, 1)]
hippocampus_lfp = downsampled_lfp_matrix[:, slice(obj.dictionary[session]["hpc_chans"][0],
                                                  obj.dictionary[session]["hpc_chans"][-1] + 1, 1)]


def calc_time(mua_activity):
    """A func that takes in an array of 50ms bins and converts it to minutes"""
    time_in_minutes = ((len(mua_activity) * 50) / 1000) / 60
    print('Time generated', time_in_minutes)
    step = time_in_minutes / len(mua_activity)
    print('Step generated', step)
    time = np.arange(0, time_in_minutes, step)
    assert len(time) == len(mua_activity), "Lengths don't match"
    return (time)


fig, axs = plt.subplots(ncols=4, nrows=2)
for channel in range(4):
    # Calculate Mua
    visual_mua = calculate_mua(visual_lfp[:, channel], fs)
    hpc_mua = calculate_mua(hippocampus_lfp[:, channel], fs)

    # Create time - Convert 50ms bins into seconds
    time_visual = calc_time(visual_mua)
    time_hpc = calc_time(hpc_mua)

    axs[0][channel].set_title("Visual Cortex")
    axs[0][channel].set_ylabel("50ms binned counts")
    axs[0][channel].plot(time_visual, visual_mua, color='k')
    axs[0][channel].margins(x=0)
    axs[0][channel].margins(y=0)
    axs[1][channel].set_title("Hippocampus")
    axs[1][channel].set_ylabel("50ms binned counts")
    axs[1][channel].plot(time_hpc, hpc_mua, color='k')
    axs[1][channel].margins(x=0)
    axs[1][channel].margins(y=0)
    fig.suptitle("MUA Activity across one session and different channels for VC vs HPC", fontsize=16)
plt.show()

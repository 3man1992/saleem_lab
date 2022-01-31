import numpy as np

def dB(x, out=None):
    if out is None:
        return 10 * np.log10(x)
    else:
        np.log10(x, out)
        np.multiply(out, 10, out) #Convert power into decibals which is a log scale

def downsample(data, original_fs, desired_fs):
    down_sampling_factor = int(original_fs/ desired_fs)
    down_sampled_data    = data[0:-1:down_sampling_factor, :]
    return down_sampled_data

# #Convert 64 channels into 16 tetrodes - convert into function - unfinished code not needed for tomazzo data as silicon probes have a different geometry to normal tetrodes
# tetrode_data = {}
# counter = 1
# for i in range(16):
#     if i == 0:
#         tetrode_data[i] = np.mean(data[:,    0:4], axis = 1)
#     else:
#         tetrode_data[i] = np.mean(data[:,    4*counter:4* (counter+1)], axis = 1)
#         counter += 1
# # print(tetrode_data.shape)
# print('Length of averaged channels', len(tetrode_data[0]))

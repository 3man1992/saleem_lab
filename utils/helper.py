import numpy as np

def dB(x, out=None):
    if out is None:
        return 10 * np.log10(x)
    else:
        np.log10(x, out)
        np.multiply(out, 10, out) #Convert power into decibals which is a log scale

def downsample(data, original_fs, desired_fs):
    down_sampling_factor = int(original_fs / desired_fs)
    down_sampled_data    = data[0:-1:down_sampling_factor, :]
    num_of_samples = len(data[0:-1:down_sampling_factor, 0])
    return down_sampled_data, num_of_samples

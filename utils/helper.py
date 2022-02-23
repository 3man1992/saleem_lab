import numpy as np
import sys
from utils.matlab_to_pythonDict import convert_matlab_struct

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

def extract_variables_to_determine_sleep(matlab_file_path):
    obj = convert_matlab_struct(matlab_file_path)
    linear_time, time, velocity = obj.extract_structs_within_structs()
    return(velocity, time, linear_time)

def determine_sleep_times(time, linear_time):
    pre_task_sleep_time = list(filter(lambda x: x < linear_time[0], time))
    post_task_sleep_time = list(filter(lambda x: x > linear_time[-1], time))
    return(pre_task_sleep_time, post_task_sleep_time)

import numpy as np
# from utils.matlab_to_pythonDict import convert_matlab_struct
from matlab_to_pythonDict import convert_matlab_struct


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
    velocity = obj.dictionary['v_cm']
    time = obj.dictionary['t']
    linear_time = obj.extract_structs_within_structs()
    return(velocity, time, linear)

def determine_sleep(time, linear):
    print(linear)

velocity, time, linear = extract_variables_to_determine_sleep("/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/Dark_Day6_250719/extracted_position.mat")
determine_sleep(time, linear)

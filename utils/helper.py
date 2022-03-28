# OS Libaries
import numpy as np
import resampy
from scipy.ndimage.filters import gaussian_filter

# Custom Libaries
from utils.convert_and_ingest_data_types.auto_mat_to_python import convert_matlab_struct


def interpolate(variable, current_fs, desired_fs):
    """Converts a lower sampled variable to match a higher sampled varible"""
    interpolated_variable = resampy.resample(np.asarray(variable),
                                             current_fs,
                                             desired_fs)
    return(interpolated_variable)


def dB(x, out=None):
    """Convert power into decibals which is a log scale"""
    if out is None:
        return 10 * np.log10(x)
    else:
        np.log10(x, out)
        np.multiply(out, 10, out)


def downsample(data, original_fs, desired_fs):
    """Down samples mV data to make it easier to process"""
    down_sampling_factor = int(original_fs / desired_fs)
    down_sampled_data = data[0:-1:down_sampling_factor, :]
    num_of_samples = len(data[0:-1:down_sampling_factor, 0])
    return down_sampled_data, num_of_samples


def extract_variables_to_determine_sleep(matlab_file_path):
    """Extract requied variables from mat file to determine sleep times"""
    obj = convert_matlab_struct(matlab_file_path)
    linear_time, time, velocity = obj.extract_structs_within_structs()
    return(velocity, time, linear_time)


def determine_sleep_times(time, linear_time):
    print("Start of task time {}, end of task time {}, total time {} \n".format(time[0], time[-1], time[-1] - time[0]))
    pre_task_sleep_time = list(filter(lambda x: x < linear_time[0], time))  # Accept time less than the end of task time
    print("Length of time for pre_task_sleep", len(pre_task_sleep_time))
    post_task_sleep_time = list(filter(lambda x: x > linear_time[-1], time))  # Accept time bigger than the end of task time
    print("Length of time for post_task_sleep", len(post_task_sleep_time))
    print("Post_task_sleeping starts at", post_task_sleep_time[0])
    return(pre_task_sleep_time, post_task_sleep_time)


def smooth(signal, sigma):
    # Smooth the filtered data with gaussian
    """Uses a guassian filter from scipy the window is calculated using int(truncate * sigma + 0.5)
    This was taken from the scipy source code. Thus to obtain a window of 60ms. You need 10 samples. Given 6000hz.
    As 6 samples per milisecond. So a 60ms window would be a 10 sample window. Which can be achieved with sigma 7"""

    truncate = 8  # Truncate the filter at this many standard deviations. Default is 4.0.
    # sigma = 1000 #Chosen from truncate * sigma + 0.5
    smooth_signal = gaussian_filter(input=signal,
                                    sigma=sigma,
                                    truncate=truncate,
                                    mode='constant')
    return(smooth_signal)

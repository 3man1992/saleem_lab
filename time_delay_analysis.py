# OS Libaries
import numpy as np
import matplotlib.pyplot as plt

# Custom libs
from utils.convert_and_ingest_data_types.auto_mat_to_python import convert_matlab_struct
from visulisations.mua import calculate_mua
from utils import helper
from meta_data import Meta
from visulisations.temporal_lag import return_forward_and_backward_correlation_coeffs, create_x_axis_for_coeff_plot, extract_arg_max

# Paramters
org_fs = 30000
fs = 6000

# Load data
obj = Meta()
session = "Day_6_Dark"
LFP = np.load(obj.dictionary[session]["lfp"])
mat_file = obj.dictionary[session]["mat"]

# Downsample data
downsampled_lfp_matrix, n_samples = helper.downsample(LFP,
                                                      org_fs,
                                                      desired_fs=fs)


# A function to plot channels comparions across entire session
def whole_session_plot():
    """Plot four channel comparisons across session without splitting by session type"""
    # Plotting logic
    colours = ['k', 'b', 'g', 'r']
    plt.figure()
    # For each channel index, calculate coefficients
    for channel_index in range(4):
        visual_channel = obj.dictionary[session]["vc_chans"][channel_index]
        hpc_channel = obj.dictionary[session]["hpc_chans"][channel_index]
        visual_mua = calculate_mua(downsampled_lfp_matrix[:, visual_channel], 6000)
        hpc_mua = calculate_mua(downsampled_lfp_matrix[:, hpc_channel], 6000)
        corrcoeffs_forward, corrcoeffs_backward = return_forward_and_backward_correlation_coeffs(visual_mua, hpc_mua)
        temporal_coeffs, x_axis = create_x_axis_for_coeff_plot(corrcoeffs_forward, corrcoeffs_backward)
        plt.plot(x_axis / 10, temporal_coeffs, color=colours[channel_index])
    plt.margins(x=0)
    plt.ylabel('Correlation Coeffs')
    plt.xlabel('Seconds')
    plt.title('Temporal coefficients across four channels comparisons')
    plt.legend()
    plt.show()


# A function to plot channels comparions across sleep segments
def temporal_lag_divided_by_sleep():
    # Pull out times
    matlab_object = convert_matlab_struct(mat_file)
    time_mat = matlab_object.dic['t']
    linear_time = matlab_object.dic['linear']['timestamps']
    pre_task_sleep_time, post_task_sleep_time = helper.determine_sleep_times(time_mat, linear_time)

    """Plot four channel comparisons across session AND splitting by session type"""
    # Plotting logic
    colours = ['k', 'b', 'g', 'r']
    fig, axs = plt.subplots(nrows=2)
    # For each channel index, calculate coefficients
    for channel_index in range(4):
        visual_channel = obj.dictionary[session]["vc_chans"][channel_index]
        hpc_channel = obj.dictionary[session]["hpc_chans"][channel_index]
        pre_task_sleep_index = int(pre_task_sleep_time[0] * fs)
        post_task_sleep_index = int((post_task_sleep_time[0] - pre_task_sleep_time[0]) * fs)

        # Pre_task
        visual_mua = calculate_mua(downsampled_lfp_matrix[:pre_task_sleep_index, visual_channel], 6000)
        hpc_mua = calculate_mua(downsampled_lfp_matrix[:pre_task_sleep_index, hpc_channel], 6000)
        corrcoeffs_forward, corrcoeffs_backward = return_forward_and_backward_correlation_coeffs(visual_mua, hpc_mua)
        temporal_coeffs, x_axis = create_x_axis_for_coeff_plot(corrcoeffs_forward, corrcoeffs_backward)
        axs[0].plot(x_axis / 10, temporal_coeffs, color=colours[channel_index])
        axs[0].set_title('Pre-Task sleep')
        axs[0].set_xlabel('Time lag in seconds')
        axs[0].set_ylabel('Temporal coefficient')
        axs[0].axvline(x=0, color='k', linestyle='--')
        axs[0].margins(x=0)
        axs[0].set_xlim(-0.5, 0.5)

        # Post task
        visual_mua = calculate_mua(downsampled_lfp_matrix[post_task_sleep_index:, visual_channel], 6000)
        hpc_mua = calculate_mua(downsampled_lfp_matrix[post_task_sleep_index:, hpc_channel], 6000)
        corrcoeffs_forward, corrcoeffs_backward = return_forward_and_backward_correlation_coeffs(visual_mua, hpc_mua)
        temporal_coeffs, x_axis = create_x_axis_for_coeff_plot(corrcoeffs_forward, corrcoeffs_backward)
        axs[1].plot(x_axis / 10, temporal_coeffs, color=colours[channel_index])
        axs[1].set_title('Post-Task sleep')
        axs[1].set_xlabel('Time lag in seconds')
        axs[1].set_ylabel('Temporal coefficient')
        axs[1].axvline(x=0, color='k', linestyle='--')
        axs[1].margins(x=0)
        axs[1].set_xlim(-0.5, 0.5)

    plt.show()

# A function to plot channels comparions across sleep segments
def arg_max_comparison():
    # Pull out times
    matlab_object = convert_matlab_struct(mat_file)
    time_mat = matlab_object.dic['t']
    linear_time = matlab_object.dic['linear']['timestamps']
    pre_task_sleep_time, post_task_sleep_time = helper.determine_sleep_times(time_mat, linear_time)

    """Plot four channel comparisons across session AND splitting by session type"""
    # Plotting logic
    colours = ['k', 'b', 'g', 'r']
    fig, axs = plt.subplots(nrows=2)
    # For each channel index, calculate coefficients
    for channel_index in range(4):
        visual_channel = obj.dictionary[session]["vc_chans"][channel_index]
        hpc_channel = obj.dictionary[session]["hpc_chans"][channel_index]
        pre_task_sleep_index = int(pre_task_sleep_time[0] * fs)
        post_task_sleep_index = int((post_task_sleep_time[0] - pre_task_sleep_time[0]) * fs)

        # Pre_task
        visual_mua = calculate_mua(downsampled_lfp_matrix[:pre_task_sleep_index, visual_channel], 6000, 30)
        hpc_mua = calculate_mua(downsampled_lfp_matrix[:pre_task_sleep_index, hpc_channel], 6000, 30)
        corrcoeffs_forward, corrcoeffs_backward = return_forward_and_backward_correlation_coeffs(visual_mua, hpc_mua)
        temporal_coeffs, x_axis = create_x_axis_for_coeff_plot(corrcoeffs_forward, corrcoeffs_backward)
        arg_max_temporal_index, arg_max_value = extract_arg_max(temporal_coeffs, x_axis)
        axs[0].scatter(arg_max_temporal_index, arg_max_value, color=colours[channel_index])
        axs[0].set_title('Pre-Task sleep')
        axs[0].set_xlabel('Time lag in mS')
        axs[0].set_ylabel('Temporal coefficient')
        axs[0].axvline(x=0, color='k', linestyle='--')
        axs[0].margins(x=0)

        # Post task
        visual_mua = calculate_mua(downsampled_lfp_matrix[post_task_sleep_index:, visual_channel], 6000, 30)
        hpc_mua = calculate_mua(downsampled_lfp_matrix[post_task_sleep_index:, hpc_channel], 6000, 30)
        corrcoeffs_forward, corrcoeffs_backward = return_forward_and_backward_correlation_coeffs(visual_mua, hpc_mua)
        temporal_coeffs, x_axis = create_x_axis_for_coeff_plot(corrcoeffs_forward, corrcoeffs_backward)
        arg_max_temporal_index, arg_max_value = extract_arg_max(temporal_coeffs, x_axis)
        axs[1].scatter(arg_max_temporal_index, arg_max_value, color=colours[channel_index])
        axs[1].set_title('Post-Task sleep')
        axs[1].set_xlabel('Time lag in mS')
        axs[1].set_ylabel('Temporal coefficient')
        axs[1].axvline(x=0, color='k', linestyle='--')
        axs[1].margins(x=0)

    plt.show()


# Run functions
# whole_session_plot() # Comment out and in when you want to use
# temporal_lag_divided_by_sleep()
arg_max_comparison()

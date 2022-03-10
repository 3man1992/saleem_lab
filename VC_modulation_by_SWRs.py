# Custom Libaries
from utils import helper
from utils.meta_data import Meta
from visulisations.generate_spectograms import cwt
from visulisations.mua import calculate_mua
from utils.convert_and_ingest_data_types.auto_mat_to_python import convert_matlab_struct

# OS Libaries
from ripple_detection.simulate import simulate_time
import numpy as np
import matplotlib.pyplot as plt
from ripple_detection import filter_ripple_band

# Load data
obj = Meta()
base_path = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/"
pre_sleep_ripple_times = np.load(base_path + obj.light["Day_7_Light"]["pre"])
post_sleep_ripple_times = np.load(base_path + obj.light["Day_7_Light"]["post"])
LFP = np.load(base_path + obj.light["Day_7_Light"]["lfp"])
mat_file = obj.light["Day_7_Light"]["mat"]

# Parameters
org_fs = 30000  # What is the original fs of the ephys recording device
fs = 6000  # What do you want to downsample the data to
padding = 3000  # What extra time do you want on ripple window - If fs is 3000 then 1500 is half a second either side

# Downsample LFP data to make it faster to process
downsampled_lfp_matrix, n_samples = helper.downsample(LFP,
                                                      org_fs,
                                                      desired_fs=fs)

# Select Visual Cortex and Hippocampal channels
visual_lfp = downsampled_lfp_matrix[:, slice(obj.light["Day_7_Light"]["vc_chans"][0], obj.light["Day_7_Light"]["vc_chans"][-1] + 1, 1)]
hippocampus_lfp = downsampled_lfp_matrix[:, slice(obj.light["Day_7_Light"]["hpc_chans"][0], obj.light["Day_7_Light"]["hpc_chans"][-1] + 1, 1)]

# Filter data for ripple visulisation
swr_visual = filter_ripple_band(visual_lfp)
swr_hippocampus = filter_ripple_band(hippocampus_lfp)

# Simulate time
time = simulate_time(n_samples, fs)

# Calculate buffer for post task ripple analysis
matlab_object = convert_matlab_struct(mat_file)
time_mat = matlab_object.dic['t']
linear_time = matlab_object.dic['linear']['timestamps']
pre_task_sleep_time, post_task_sleep_time = helper.determine_sleep_times(time_mat, linear_time)
buffer = (post_task_sleep_time[0] - pre_task_sleep_time[0]) * fs


# Define a func to output differences for pre task sleep and post task sleep
def plot_pre_or_post_ripples(ripple_times, ripple_id, post_task_buffer):
    """Takes in pre or post sleep ripples and returns:
    the relevant indexed data. Post task buffer is used to ensure index is correct
    considering post task occurs midway lfp signal and time starts from 0.
    Set post_task_buffer to 0 if calculating pre-sleep-ripples"""

    # Create indexes per ripple data
    ripple_start_index = int(ripple_times[ripple_id][0] * fs + post_task_buffer) - padding
    ripple_end_index = int(ripple_times[ripple_id][1] * fs + post_task_buffer) + padding
    seg_time = time[ripple_start_index:ripple_end_index]

    # Raw data for one channel
    raw_hpc_lfp = hippocampus_lfp[ripple_start_index:ripple_end_index, 0]
    raw_vc_lfp = visual_lfp[ripple_start_index:ripple_end_index, 0]

    # SWRs for one cahnnel
    swr_vis = swr_visual[ripple_start_index:ripple_end_index, 0]
    swr_hipp = swr_hippocampus[ripple_start_index:ripple_end_index, 0]

    # Mua activity calculations
    vis_mua = calculate_mua(raw_vc_lfp, fs)
    hippo_mua = calculate_mua(raw_hpc_lfp, fs)

    return(seg_time,
           raw_hpc_lfp,
           raw_vc_lfp,
           swr_vis,
           swr_hipp,
           vis_mua,
           hippo_mua)


# Plot per ripple
for ripple_id in range(6):

    # Define a 4 by 4 grid
    fig, axs = plt.subplots(nrows=5, ncols=4, sharey='row')

    # Return variables
    pre_seg_time, pre_raw_hpc_lfp, pre_raw_vc_lfp, pre_swr_visual, pre_swr_hippocampus, pre_visual_mua, pre_hippocampus_mua = plot_pre_or_post_ripples(pre_sleep_ripple_times, ripple_id, 0)
    post_seg_time, post_raw_hpc_lfp, post_raw_vc_lfp, post_swr_visual, post_swr_hippocampus, post_visual_mua, post_hippocampus_mua = plot_pre_or_post_ripples(post_sleep_ripple_times, ripple_id, buffer)

    # POST TASK SLEEP

    # Plot the first row of raw LFP data
    axs[0][2].plot(post_seg_time, post_raw_hpc_lfp, 'k')
    axs[0][2].set_title("Post_Task_Sleep \n raw LFP : HPC")
    axs[0][2].margins(x=0)
    axs[0][2].get_xaxis().set_visible(False)

    axs[0][3].plot(post_seg_time, post_raw_vc_lfp, 'k')
    axs[0][3].set_title('Post_Task_Sleep \n raw LFP : VC')
    axs[0][3].margins(x=0)
    axs[0][3].get_yaxis().set_visible(False)
    axs[0][3].get_xaxis().set_visible(False)

    # Plot the second row containing CWT within the MUA range
    post_hpc_t_cwt, post_hpc_f_cwt, post_hpc_psd_cwt, kwargs_dict = cwt(post_raw_hpc_lfp, fs, freq_range=[500, 3000])
    axs[2][2].pcolormesh(post_hpc_t_cwt, post_hpc_f_cwt, post_hpc_psd_cwt, **kwargs_dict)
    axs[2][2].set_title('CWT 500-3000hz : HPC')
    axs[2][2].get_xaxis().set_visible(False)

    post_vc_t_cwt, post_vc_f_cwt, post_vc_psd_cwt, kwargs_dict = cwt(post_raw_vc_lfp, fs, freq_range=[500, 3000])
    axs[2][3].pcolormesh(post_vc_t_cwt, post_vc_f_cwt, post_vc_psd_cwt, **kwargs_dict)
    axs[2][3].set_title('CWT 500-3000hz : VC')
    axs[2][3].get_xaxis().set_visible(False)

    # Plot the third row containing the filtered ripple band
    axs[1][2].plot(post_seg_time, post_swr_hippocampus, 'k')
    axs[1][2].margins(x=0)
    axs[1][2].set_title('Ripple 150-250hz : HPC')
    axs[1][2].get_xaxis().set_visible(False)

    axs[1][3].plot(post_seg_time, post_swr_visual, 'k')
    axs[1][3].margins(x=0)
    axs[1][3].set_title('Ripple 150-250hz : VC')
    axs[1][3].get_xaxis().set_visible(False)

    # Plot the MUA activity on the final row
    axs[3][2].plot(post_hippocampus_mua, 'k')
    axs[3][2].margins(x=0)
    axs[3][2].set_title('MUA Activity >500hz : HPC')
    axs[3][2].set_xlabel('Time (Seconds)')

    axs[3][3].plot(post_visual_mua, 'k')
    axs[3][3].margins(x=0)
    axs[3][3].set_title('MUA Activity >500hz : VC')

    # Plot average power across time
    post_hpc_avg_psd = np.average(post_hpc_psd_cwt, axis=0)
    post_seg_time = post_seg_time - post_seg_time[0]
    axs[4][2].plot(post_seg_time, post_hpc_avg_psd)
    axs[4][2].set_xlabel('Time (Seconds)')

    post_vc_avg_psd = np.average(post_vc_psd_cwt, axis=0)
    axs[4][3].plot(post_seg_time, post_vc_avg_psd)
    axs[4][3].set_xlabel('Time (Seconds)')

    # PRE TASK SLEEP----------------------------

    # Plot the first row of raw LFP data
    axs[0][0].plot(pre_seg_time, pre_raw_hpc_lfp, 'k')
    axs[0][0].set_title('Pre_Task_Sleep \n raw LFP : HPC')
    axs[0][0].margins(x=0)
    axs[0][0].set_ylabel('mV')
    axs[0][0].get_xaxis().set_visible(False)

    axs[0][1].plot(pre_seg_time, pre_raw_vc_lfp, 'k')
    axs[0][1].set_title('Pre_Task_Sleep \n raw LFP : VC')
    axs[0][1].margins(x=0)
    axs[0][1].get_yaxis().set_visible(False)
    axs[0][1].get_xaxis().set_visible(False)

    # Plot the second row containing CWT within the MUA range
    pre_hpc_t_cwt, pre_hpc_f_cwt, pre_hpc_psd_cwt, kwargs_dict = cwt(pre_raw_hpc_lfp, fs, freq_range=[500, 3000])
    axs[2][0].pcolormesh(pre_hpc_t_cwt, pre_hpc_f_cwt, pre_hpc_psd_cwt, **kwargs_dict)
    axs[2][0].set_title('CWT 500-3000hz : HPC')
    axs[2][0].get_xaxis().set_visible(False)
    axs[2][0].set_ylabel('hZ')

    pre_vc_t_cwt, pre_vc_f_cwt, pre_vc_psd_cwt, kwargs_dict = cwt(pre_raw_vc_lfp, fs, freq_range=[500, 3000])
    axs[2][1].pcolormesh(pre_vc_t_cwt, pre_vc_f_cwt, pre_vc_psd_cwt, **kwargs_dict)
    axs[2][1].set_title('CWT 500-3000hz : VC')
    axs[2][1].get_xaxis().set_visible(False)

    # Plot the third row containing the filtered ripple band
    axs[1][0].plot(pre_seg_time, pre_swr_hippocampus, 'k')
    axs[1][0].margins(x=0)
    axs[1][0].set_title('Ripple 150-250hz : HPC')
    axs[1][0].set_ylabel('SWR signal')
    axs[1][0].get_xaxis().set_visible(False)

    axs[1][1].plot(pre_seg_time, pre_swr_visual, 'k')
    axs[1][1].margins(x=0)
    axs[1][1].set_title('Ripple 150-250hz : VC')
    axs[1][1].get_xaxis().set_visible(False)

    # Plot the MUA activity on the final row
    axs[3][0].plot(pre_hippocampus_mua, 'k')
    axs[3][0].margins(x=0)
    axs[3][0].set_title('MUA Activity >500hz : HPC')
    axs[3][0].set_xlabel('Time (Seconds)')
    axs[3][0].set_ylabel('50ms counts > 2SD')

    axs[3][1].plot(pre_visual_mua, 'k')
    axs[3][1].margins(x=0)
    axs[3][1].set_title('MUA Activity >500hz : VC')
    axs[3][1].set_xlabel('Time (Seconds)')

    # Plot average power across time
    pre_hpc_avg_psd = np.average(pre_hpc_psd_cwt, axis=0)
    pre_seg_time = pre_seg_time - pre_seg_time[0]
    axs[4][0].plot(pre_seg_time, pre_hpc_avg_psd)
    axs[4][0].set_xlabel('Time (Seconds)')
    axs[4][0].set_ylabel('Avg normalised power')

    pre_vc_avg_psd = np.average(pre_vc_psd_cwt, axis=0)
    axs[4][1].plot(pre_seg_time, pre_vc_avg_psd)
    axs[4][1].set_xlabel('Time (Seconds)')

    # Super title
    fig.suptitle('Predicted ripple number:{} - HPC vs VC'.format(ripple_id), fontweight='bold')

    # Save graphs
    # plt.savefig("/Users/freeman/Documents/saleem_folder/viz/marta_dark_day_6/vc_VS_HPC_ripple_num_{}".format(ripple_id), dpi=100)

    # Plot the graphs
    plt.show()
    # plt.close(fig)

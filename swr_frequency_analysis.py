# Custom Libaries
from utils.meta_data import Meta
from sharp_wave_ripple_analysis import ripple_frequency_analysis_scatter as freq

# Os Libaries
import matplotlib.pyplot as plt

# Load data
sessions = list(Meta().dictionary.keys())

# Scatter plot Analysis
# Loop over sessions
# pre_frequency_counts = []
# post_frequency_counts = []
#
# for session in sessions:
#     pre_ripples_path = Meta().dictionary[session]['pre']
#     post_ripples_path = Meta().dictionary[session]['post']
#     pre_centers = freq.find_center_ripple(pre_ripples_path)
#     post_centers = freq.find_center_ripple(post_ripples_path)
#     pre_frequency_counts.append(freq.avg_calc_ripples_per_minute(pre_centers))
#     post_frequency_counts.append(freq.avg_calc_ripples_per_minute(post_centers))
#
# # Plot scatter
# # Done a hack here to split dark and light sessions. Keep dark session end of metadata keys
# # To keep hack working
# plt.scatter(pre_frequency_counts[:-2], post_frequency_counts[:-2], label='Light conditions')
# plt.scatter(pre_frequency_counts[-2:], post_frequency_counts[-2:], label='Dark conditions')
# plt.plot([0, 30], [0, 30], color='k', linestyle='dashed')
# plt.title('Average number of SWRs per minute', fontsize=20)
# plt.legend()
# plt.xlabel('Sleep Session \n Pre-Task')
# plt.ylabel('Sleep Session \n Post-Task')
# plt.xlim(0, 10)
# plt.ylim(0, 10)
# plt.show()

# Define a 4 by 4 grid
fig, axs = plt.subplots(nrows=5, sharex='col')
counter = 0

# Line plot Analysis
for session in sessions:
    pre_ripples_path = Meta().dictionary[session]['pre']
    post_ripples_path = Meta().dictionary[session]['post']
    pre_centers = freq.find_center_ripple(pre_ripples_path)
    post_centers = freq.find_center_ripple(post_ripples_path)
    pre_frequency_counts = freq.hist_calc_ripples_per_minute(pre_centers)
    post_frequency_counts = freq.hist_calc_ripples_per_minute(post_centers)

    # Plot scatter
    # Done a hack here to split dark and light sessions. Keep dark session end of metadata keys
    # To keep hack working
    axs[counter].plot(pre_frequency_counts, label='Pre_Task_Sleep')
    axs[counter].plot(post_frequency_counts, label='Post_Task_Sleep')
    axs[counter].margins(x=0)
    # plt.title('Average number of SWRs per minute', fontsize=20)
    axs[0].legend(loc = "upper right")
    axs[0].set_title("SWR Frequency across time and sessions")
    plt.xlabel('Minutes')
    axs[2].set_ylabel('SWR frequency per minute')
    counter += 1

plt.show()

#Add dark sessions
#Make axis go to zero

import numpy as np
import matplotlib.pyplot as plt

#Outline data to run analysis across sessions
#[0] - Presleep ripples
#[1] - Postsleep ripples
#[2] - LFP data

data = {

"Day_7_Light" : ["pre_sleep_Ripples_for_QBLU_YMaze_Day7_270719.npy",
                 "post_sleep_Ripples_for_QBLU_YMaze_Day7_270719.npy",
                 "QBLU_YMaze_Day7_270719.npy"],

"Day_3_Light" : ["pre_sleep_Ripples_for_Ymaze_Day3_220719.npy",
                 "post_sleep_Ripples_for_Ymaze_Day3_220719.npy",
                 "Ymaze_Day3_220719.npy"],

"Day_8_Light" : ["pre_sleep_Ripples_for_QBLU_YMaze_Day8_280719.npy",
                 "post_sleep_Ripples_for_QBLU_YMaze_Day8_280719.npy",
                 "QBLU_YMaze_Day8_280719.npy"],

"Day_9_Light" : ["pre_sleep_Ripples_for_OBLU_YMaze_Day9_170519.npy",
                 "post_sleep_Ripples_for_OBLU_YMaze_Day9_170519.npy",
                 "OBLU_YMaze_Day9_170519.npy"]

}

dark = {

"Day_9_Dark" : ["pre_sleep_Ripples_for_QBLU_Dark_Day9_290719.npy",
                "post_sleep_Ripples_for_QBLU_Dark_Day9_290719.npy",
                "QBLU_Dark_Day9_290719.npy"],

"Day_5_Dark" : ["pre_sleep_Ripples_for_QBLU_Dark_Day5_250719.npy",
                "post_sleep_Ripples_for_QBLU_Dark_Day5_250719.npy",
                "QBLU_Dark_Day5_250719.npy"],

"Day_6_Dark" : ["pre_sleep_Ripples_for_Dark_day6.npy",
                "post_sleep_Ripples_for_Dark_day6.npy",
                "Dark_day6_2507_19.npy"]

}

#A function that takes in a list of ripple windows, and finds the centre of that window
def find_center_ripple(ripple_times_path):
    ripple_times_path = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/" + ripple_times_path
    ripple_times = np.load(ripple_times_path)
    ripple_centres = []
    for ripple_window in ripple_times:
        ripple_centres.append(np.median(ripple_window))
    assert len(ripple_centres) == len(ripple_times), 'Number of ripple centres does not match numer of ripple windows'
    if len(ripple_centres) == 0:
        print("ERROR - List of centres is empty, check why.")
    return(ripple_centres)
#A function that takes in a list of ripple centers and calcs avg ripples per minute
def avg_calc_ripples_per_minute(ripple_centres):
        bins = list(range(0, 3600, 60)) #Create bins per minute up to a total time in seconds. 3600 seconds is one hour
        counts, bin_edges = np.histogram(ripple_centres,
                                         bins = bins)
        return(np.average(counts))

sessions = list(data.keys())
pre = []
post = []
for index in range(len(data)):
    pre_ripples_path = data[sessions[index]][0]
    post_ripples_path = data[sessions[index]][1]
    pre_centers =  find_center_ripple(pre_ripples_path)
    post_centers = find_center_ripple(post_ripples_path)
    pre.append(avg_calc_ripples_per_minute(pre_centers))
    post.append(avg_calc_ripples_per_minute(post_centers))

plt.scatter(pre, post, label = 'Light Condition')

sessions = list(dark.keys())
pre = []
post = []
for index in range(len(dark)):
    pre_ripples_path = dark[sessions[index]][0]
    post_ripples_path = dark[sessions[index]][1]
    pre_centers =  find_center_ripple(pre_ripples_path)
    post_centers = find_center_ripple(post_ripples_path)
    pre.append(avg_calc_ripples_per_minute(pre_centers))
    post.append(avg_calc_ripples_per_minute(post_centers))
plt.scatter(pre, post, label = 'Dark Condition')

plt.plot([0, 30], [0, 30], color = 'k', linestyle='dashed')
plt.legend()
plt.title('Average number of SWRs per minute')
plt.xlabel('Pre_sleep')
plt.ylabel('Post_sleep')
plt.xlim(0, 30)
plt.ylim(0, 30)
plt.show()

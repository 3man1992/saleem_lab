#Libaries
import numpy as np
from ripple_detection.simulate import simulate_time
from ripple_detection import filter_ripple_band
from utils import helper
import matplotlib.pyplot as plt

class RippleDetails:
    def __init__(self,
                 original_fs,
                 new_fs,
                 ripple_times,
                 lfp_data,
                 hippocampus_channels):

        print("\nAggregating details about ripples into Python Object")

        #Assign namespaces
        self.lfp_data = np.load(lfp_data)
        self.ripple_times = np.load(ripple_times)
        self.fs = new_fs
        self.old_fs = original_fs
        self.hippo_channels = hippocampus_channels
        self.time = 0
        self.filtered_signal = 0
        self.raw_data = 0
        self.ripple_centres = 0

        print("-- Data loaded")

        #Preprocess data
        self.select_hpc_lfp_channels()

        #Filter lfp to ripple frequency of 150-250hz
        self.filter_lfp_data()

        #Create time given fs and number of samples
        self.create_time()

        print("-- Ripple object created")

    #Select hippocampal channels and then downsample
    def select_hpc_lfp_channels(self):
        print("-- Selecting HPC channels and removing VC channels for ripple prediction analysis")

        #Create a slice to index lfp matrix by
        desired_channels = slice(self.hippo_channels[0],
                                 self.hippo_channels[-1] + 1,
                                 1)
        #Down_sample
        self.raw_data, self.samples = helper.downsample(self.lfp_data[:, desired_channels],
                                                        self.old_fs,
                                                        self.fs)

        assert self.raw_data.shape[1] == len(self.hippo_channels), "Shape doesn't match number of channels inputted"

    #Filter raw data to lfp signal
    def filter_lfp_data(self):
        print("-- Bandpass filtering HPC lfp data to 150-250hz as per Frank lab")
        self.filtered_signal = filter_ripple_band(self.raw_data)

    #Def create time from nsamples and fs
    def create_time(self):
        self.time = simulate_time(self.samples, self.fs)

    #Calculate ripple centres
    def find_center_ripple(self):
        self.ripple_centres = []
        for ripple_window in self.ripple_times:
            self.ripple_centres.append(np.median(ripple_window))
        assert len(self.ripple_centres) == len(self.ripple_times), 'Number of ripple centres does not match numer of ripple windows'
        if len(self.ripple_centres) == 0:
            print("ERROR - List of centres is empty, check why.")
        return(self.ripple_centres)

#Hyperparameters
org_fs = 30000
fs = 2000
hpc_channels = [8,9,10]
pre_sleep_ripple_file_path  = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/pre_sleep_Ripples_for_QBLU_Dark_Day9_290719.npy"
post_sleep_ripple_file_path = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/post_sleep_Ripples_for_QBLU_Dark_Day9_290719.npy"
lfp = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/QBLU_Dark_Day9_290719.npy"

#Pre sleep details obj created
pre_sleep = RippleDetails(original_fs = org_fs,
                          new_fs = fs,
                          ripple_times = pre_sleep_ripple_file_path,
                          lfp_data = lfp,
                          hippocampus_channels = hpc_channels)

#post sleep details obj created
post_sleep = RippleDetails(original_fs = org_fs,
                          new_fs = fs,
                          ripple_times = post_sleep_ripple_file_path,
                          lfp_data = lfp,
                          hippocampus_channels = hpc_channels)

#Call ripple centre arrays
pre_sleep_ripple_centers = pre_sleep.find_center_ripple()
post_sleep_ripple_centers = post_sleep.find_center_ripple()

def calc_ripples_per_minute(total_time_in_seconds, ripple_centres):
        bins = list(range(0, total_time_in_seconds, 60)) #Create bins per minute up to a total time in seconds. Use 7200 for 2 hours
        counts, bin_edges = np.histogram(ripple_centres,
                                         bins = bins)
        return(counts)

pre_counts  = calc_ripples_per_minute(7200, pre_sleep_ripple_centers)
post_counts = calc_ripples_per_minute(7200, post_sleep_ripple_centers)

plt.plot(pre_counts, color='k')
plt.plot(post_counts, color ='r')
plt.show()

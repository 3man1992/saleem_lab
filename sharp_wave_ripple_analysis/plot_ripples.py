#Libaries
import numpy as np
import matplotlib.pyplot as plt
from ripple_detection.simulate import simulate_time
from ripple_detection import filter_ripple_band
from utils import helper
from utils.matlab_to_pythonDict import convert_matlab_struct
from scipy.ndimage.filters import gaussian_filter
from scipy.signal import savgol_filter

class RippleAnalysis:
    def __init__(self,
                 original_fs,
                 new_fs,
                 ripple_times,
                 lfp_data,
                 hippocampus_channels):

        print('\n#################')

        #Assign namespaces
        self.lfp_data = np.load(lfp_data)
        self.ripple_times = np.load(ripple_times)
        self.fs = new_fs
        self.old_fs = original_fs
        self.hippo_channels = hippocampus_channels
        print("-- Data loaded")

        #Preprocess data
        self.prep_data()

        #Filter lfp to ripple frequency of 150-250hz
        self.filter_lfp_data()

        #Create time given fs and number of samples
        self.create_time()

        print("-- Ripple object created")
        print('#################\n')

    #Select hippocampal channels and then downsample
    def prep_data(self):
        print("-- Preprocessing data")

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
        print("-- Bandpass filtering lfp data")
        self.filtered_signal = filter_ripple_band(self.raw_data)

    #Def create time from nsamples and fs
    def create_time(self):
        self.time = simulate_time(self.samples, self.fs)

    #Smooth ripples
    def smooth(self, signal):
        #Smooth the filtered data with gaussian
        """Uses a guassian filter from scipy the window is calculated using int(truncate * sigma + 0.5)
        This was taken from the scipy source code. Thus to obtain a window of 60ms. You need 10 samples. Given 6000hz.
        As 6 samples per milisecond. So a 60ms window would be a 10 sample window. Which can be achieved with sigma 7"""

        truncate = 8 #Truncate the filter at this many standard deviations. Default is 4.0.
        sigma = 1000 #Chosen from truncate * sigma + 0.5
        self.smoothedF_lfp = gaussian_filter(input = signal,
                                             sigma = sigma,
                                             truncate = truncate,
                                             mode = 'constant')
        return(self.smoothedF_lfp)

#Parameters
org_fs = 30000
fs = 2000
ripple_array = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/Dark_day6_2507_19_ripple_times.npy"
lfp_array    = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/Dark_day6_2507_19.npy"
mat_file     = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/Dark_Day6_250719/extracted_position.mat"
hippocampal_channels = [8, 9, 10] #Removed 11 as picking up noise
padding = 250 #Adds 0.5 seconds to index either side

#Calculate pre and post sleep times
velocity, time, linear_time = helper.extract_variables_to_determine_sleep(mat_file)
pre_task_sleep_time, post_task_sleep_time = helper.determine_sleep_times(time, linear_time)

print(pre_task_sleep_time)

#Create the ripple object with the above parrameters
obj = RippleAnalysis(original_fs  = org_fs,
                               new_fs       = fs,
                               ripple_times = ripple_array,
                               lfp_data     = lfp_array,
                               hippocampus_channels = hippocampal_channels)

#Create velocity object
velocity_data = helper.sleep_indexing("/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/Dark_Day6_250719/extracted_position.mat")

# def plot_each_ripple():
#     #Plot every ripple that was detected using Kay's method - plot first 50 ripples as a test
#     for ripple_id in range(5):
#         fig, axs = plt.subplots(nrows = len(obj.hippo_channels),
#                                 ncols = 2,
#                                 sharex=True)
#         ripple_start_index = int(obj.ripple_times[ripple_id][0] * obj.fs) - padding
#         ripple_end_index =   int(obj.ripple_times[ripple_id][1] * obj.fs) + padding
#         seg_time = obj.time[ripple_start_index :ripple_end_index] #Produces an array of times
#
#         #Plot each channel
#         for channel_id in range(len(obj.hippo_channels)):
#             signal     = obj.filtered_signal[ripple_start_index : ripple_end_index , channel_id]
#             raw_signal = obj.raw_data[ripple_start_index : ripple_end_index , channel_id]
#             axs[channel_id][0].plot(seg_time, raw_signal, 'k')
#             axs[channel_id][0].margins(x=0)
#             y = savgol_filter(signal, 71, 9) #Need to play around with the params still, but visually looks ok
#             axs[channel_id][1].plot(seg_time, y, 'k')
#             axs[channel_id][1].margins(x=0)
#         fig.suptitle('Predicted ripple number:{} \n Column 1: Raw LFP - \n Column 2: Bandpass of 150-250hz, detected using Kay et al 2016'.format(ripple_id))
#         fig.supxlabel('Seconds')
#         fig.supylabel('mV')
#         plt.show()
#     fig.set_size_inches(10, 17) #width and height of image
#     plt.savefig("/Users/freeman/Documents/saleem_folder/viz/marta_dark_day_6/ripple_num_{}".format(ripple_id), dpi=100)
#     plt.close(fig)
#     return None

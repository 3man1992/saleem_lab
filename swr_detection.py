#Custom libs
from utils import reshape #Shapes the 1d array of mv into 2d array of [timepoints, channels]
from utils import helper

#OS libaries
import numpy as np
import matplotlib.pyplot as plt
import time
from scipy import signal
from ripple_detection import Karlsson_ripple_detector, Kay_ripple_detector
from ripple_detection.simulate import simulate_time
from ripple_detection import filter_ripple_band

#A function to detect sharp wave ripples
def detect_SWRs(orgignal_fs,
                new_fs,
                lfp_data,
                hippocampal_channels,
                velocity_data,
                saved_file_string):
    matrix = np.load(lfp_data) #Load the data into a numpy array
    raw_data, n_samples = helper.downsample(matrix, orgignal_fs, new_fs) #Downsample the data
    filtered_signal = filter_ripple_band(raw_data) #Bandpass filter lfp signal to 15-250hz
    desired_channels = slice(hippo_channels[0],
                             hippo_channels[-1] + 1,
                             1) #Create a slice to index lfp matrix by
    filtered_signal = filtered_signal[:, desired_channels] #Select hippocampal channels
    time = simulate_time(n_samples, new_fs) #Calculate the time of each sample in seconds
    speed = np.load(velocity_data) #The ripple algo needs speed to determine ripples
    speed = speed[:len(filtered_signal)] #The ncs conversion file looses some data so have to remove end of velocity
    assert len(speed) == len(filtered_signal), "The two don't match, caused by error from ncs import and indexing hasn't rectified len error"
    kay_ripples = Kay_ripple_detector(time,
                                      filtered_signal,
                                      speed,
                                      new_fs,
                                      zscore_threshold=3.0) #Alter zscore threshold to make more or less sensitive
    ripple_list = kay_ripples.values
    np.save("/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/"
            +
            "{}".format(saved_file_string), ripple_list)
    print("The number of ripples detected: {}".format(len(kay_ripples.values)))

#If multiple ripple files are needed to be created, copy the func
#Lfp data should be in the format [mv, channel]
if __name__ == "__main__":
    detect_SWRs(orgignal_fs = 30000,
                new_fs = 2000,
                lfp_data = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/Dark_day6_2507_19.npy",
                hippocampal_channels = [8, 9, 10],
                velocity_data = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/Dark_day6_velocity.npy",
                saved_file_string = "Ripples_for_Dark_day6_velocity.npy")

# #Parameters
# org_fs = 30000 #The FS the device recorded at
# fs = 2000 #The FS you wish the data to become
#
# #Load, downsample and filter data
# matrix = np.load("/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/Dark_day6_2507_19.npy")
# raw_data, n_samples = helper.downsample(matrix, org_fs, fs) #Downsample the data
# filtered_signal = filter_ripple_band(raw_data)
#
# #Select channels if required to select ripples from
# filtered_signal = filtered_signal[:, 8:]
# print('Number of channels: ', filtered_signal.shape[1])
#
# #Calculate speed of animal and time
# # speed = np.zeros(n_samples) #Assume 0 for now but need to calc - for tomoazzos data
# time = simulate_time(n_samples, fs)
# speed = np.load("/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/Dark_day6_velocity.npy")
# speed = speed[:len(filtered_signal)] #The ncs conversion file looses some data so have to remove end of velocity
# print("Len of velocity", len(speed))
# print("Len of signal", len(filtered_signal))
# print("Time of session in seconds:", time[-1])
# print("len of time", len(time))
# assert len(speed) == len(filtered_signal), "The two don't match, caused by error from ncs import and indexing hasn't rectified len error"
#
# #Detect SWRs
# kay_ripples = Kay_ripple_detector(time, filtered_signal, speed, fs, zscore_threshold=3.0)
# ripple_list = kay_ripples.values
# np.save("/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/Dark_day6_2507_19_ripple_times.npy", ripple_list)
# print("Number of ripples detected:\n", len(kay_ripples.values))

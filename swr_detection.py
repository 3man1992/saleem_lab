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

#Parameters
org_fs = 30000
fs = 2000

#Load, downsample and filter data
matrix = np.load("/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/Dark_day6_2507_19.npy")
raw_data, n_samples = helper.downsample(matrix, org_fs, fs)
filtered_signal = filter_ripple_band(raw_data)

#Select channels if required to select ripples from
# channel_num = [48,49,18,1,0,50,34,36,3,2,51,32,28,16,4,52] #A single shank from Tomazzo Top to bottom
filtered_signal = filtered_signal[:, 8:]
print('Number of channels: ', filtered_signal.shape[1])

#Calculate speed of animal and time
# speed = np.zeros(n_samples) #Assume 0 for now but need to calc - for tomoazzos data
time = simulate_time(n_samples, fs)
speed = np.load("/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/Dark_day6_velocity.npy")
speed = speed[:len(filtered_signal)] #The ncs conversion file looses some data so have to remove end of velocity
print("Len of velocity", len(speed))
print("Len of signal", len(filtered_signal))
print("Time of session in seconds:", time[-1])
assert len(speed) == len(filtered_signal), "The two don't match, caused by error from ncs import and indexing hasn't rectified len error"

#Detect SWRs
kay_ripples = Kay_ripple_detector(time, filtered_signal, speed, fs, zscore_threshold=3.0)
ripple_list = kay_ripples.values
np.save("/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/Dark_day6_2507_19_ripple_times.npy", ripple_list)
print("Number of ripples detected:\n", len(kay_ripples.values))

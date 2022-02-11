"""mua = mutli unit activity"""

#Libraries requried
from utils.filters import butter_bandpass_filter
import time
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter
from scipy.stats import zscore
import numpy as np
from memory_profiler import profile
import sys
import pandas as pd
import multiprocessing as mp

#Function to calculate multiunit activity
def filt_mua(lfp_data, fs):
    print("Commencing filtering of multi unit activity")
    start_time = time.time()  #Performance checks
    filtered_data = butter_bandpass_filter(lfp_data,
                                           lowcut = 500,
                                           highcut = 3000,
                                           fs = fs)
    print("FiltFilt took: %s seconds to compute" % (time.time() - start_time)) #How long did filt filt take
    return(filtered_data)

#Smooth the filtered data with gaussian
def gaussian_smooth(data):
    """Uses a guassian filter from scipy
    the window is calculated using int(truncate * sigma + 0.5)
    this was taken from the scipy source code
    Thus with a truncate of 8 and a sigma of 25, 200 samples are chosen
    Which is approx 3ms as 60 samples per ms
    Window is in millseconds if you want 500ms type 500"""

    print("\nCommencing guassian smoothing of multi unit activity")
    start_time = time.time()  #Performance checks
    truncate = 8 #Truncate the filter at this many standard deviations. Default is 4.0.
    sigma = 38
    # sigma = 25 #Smoothing sigma - Tune - Is sigma the variance of the guassian
    smoothed_lfp = gaussian_filter(input = data,
                           sigma = sigma,
                           truncate = truncate,
                           mode = 'constant')
    print("Smoothing took: %s seconds to compute" % (time.time() - start_time)) #How long did filt filt take
    return smoothed_lfp

#Threshold to binary
def threshold_binary(filtered_lfp):
    print("nCommencing thresholding of multi unit activity")
    start_time = time.time()  #Time this function
    zscore_threshold = 4.0 #What sd above mean should be considered multi unit activity
    zscored_data = zscore(filtered_lfp) #Calculate z scores for smoothed lfp
    is_above_threshold = abs(zscored_data) >= zscore_threshold #Only consider data above threshold take absolute values
    is_below_threshold = abs(zscored_data) < zscore_threshold #Only consider data above threshold take absolute values
    shape_of_lfps = is_above_threshold.shape
    none_mua_zero = np.where(is_above_threshold,
                    filtered_lfp,
                    0) #If above threshold pass through, else set mv to zero
    binary_mua =    np.where(is_below_threshold,
                    none_mua_zero,
                    1) #If above threshold set to 1
    print("Thresholding took: %s seconds to compute" % (time.time() - start_time)) #How long did filt filt take
    assert binary_mua.shape == shape_of_lfps, "Error in shape of output"
    return(binary_mua)

#Threshold to binary
def threshold(filtered_lfp):
    print("nCommencing thresholding of multi unit activity")
    start_time = time.time()  #Time this function
    zscore_threshold = 3.0 #What sd above mean should be considered multi unit activity
    zscored_data = zscore(filtered_lfp) #Calculate z scores for smoothed lfp
    is_above_threshold = abs(zscored_data) >= zscore_threshold #Only consider data above threshold take absolute values
    is_below_threshold = abs(zscored_data) < zscore_threshold #Only consider data above threshold take absolute values
    shape_of_lfps = is_above_threshold.shape
    accepted_mua =  np.where(is_above_threshold,
                    filtered_lfp,
                    0) #If above threshold pass through, else set mili volts to zero
    print("Thresholding took: %s seconds to compute" % (time.time() - start_time)) #How long did filt filt take
    assert accepted_mua.shape == shape_of_lfps, "Error in shape of output"
    return(accepted_mua)

#Return mua activity
def calculate_mua(lfp_data, fs):
    """Takes in lfp_data, filters it with a bandpass
    and then applys zscore thresholding whilst setting samples below threshold
    to zero"""
    pool = mp.Pool(mp.cpu_count())
    filtered_lfp = filt_mua(lfp_data, fs)
    mua = pool.apply(threshold(filtered_lfp))
    return mua

#Takes x number of samples, averages them and returns a binned version
#so numrow2avg = 5 will take every 5 rows avg and then return
def bin_mua(mua, numrows_2_avg):
    """Takes in a matrix, an averages the rows as per your input into bins"""
    len_of_sample = len(mua[:, 0])
    if len_of_sample % numrows_2_avg != 0:
        remainder = len_of_sample % numrows_2_avg
        print("Removing {} samples to make divisible by requested bin window".format(remainder))
        mua = mua[:-remainder, :]
    data = pd.DataFrame(mua)
    return (pd.DataFrame(data.values.reshape(-1, numrows_2_avg, data.shape[1]).mean(1)))

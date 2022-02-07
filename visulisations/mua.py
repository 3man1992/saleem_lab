"""mua = mutli unit activity"""

#Libraries requried
from utils.filters import butter_bandpass_filter
import time
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter
from scipy.stats import zscore
import numpy as np
import sys

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
def gaussian_smooth(data, sampling_frequency):
    print("\nCommencing guassian smoothing of multi unit activity")
    start_time = time.time()  #Performance checks
    sigma = 0.004 #Smoothing sigma - Tune - Is sigma the variance of the guassian
    # in time seconds. Such that if the window is 50ms I should make it so
    truncate = 8 #Truncate the filter at this many standard deviations. Default is 4.0.
    smoothed_lfp = gaussian_filter(input = data,
                           sigma = sigma * sampling_frequency,
                           truncate = truncate,
                           mode = 'constant')
    print("Smoothing took: %s seconds to compute" % (time.time() - start_time)) #How long did filt filt take
    return smoothed_lfp

#Threshold
def threshold(smoothed_lfps):
    np.set_printoptions(threshold=sys.maxsize)
    print("\nCommencing thresholding of multi unit activity")
    start_time = time.time()  #Performance checks
    zscore_threshold = 2.0 #What sd above mean should be considered multi unit activity
    minimum_duration = 0.005 #50ms in units of time sample
    zscored_data = zscore(smoothed_lfps) #Calculate z scores for smoothed lfp
    is_above_threshold = abs(zscored_data) >= zscore_threshold #Only consider data above threshold take absolute values
    shape_of_lfps = is_above_threshold.shape
    mua = np.where(is_above_threshold,
                   smoothed_lfps,
                   0) #If above threshold pass through, else set mv to zero
    print("Thresholding took: %s seconds to compute" % (time.time() - start_time)) #How long did filt filt take
    assert mua.shape == shape_of_lfps, "Error in shape of output"
    return(mua)

#Libraries requried
from utils.filters import butter_bandpass_filter
import time
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter

#Function to calculate multiunit activity
def filt_mua(lfp_data, fs):
    print("Commencing calculation of multi unit activity")
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
    sigma = 0.004 #Smoothing sigma
    truncate = 8 #Truncate the filter at this many standard deviations. Default is 4.0.
    smoothed_lfp = gaussian_filter(input = data,
                           sigma = sigma * sampling_frequency,
                           truncate = truncate,
                           mode = 'constant')
    print("Smoothing took: %s seconds to compute" % (time.time() - start_time)) #How long did filt filt take
    return smoothed_lfp

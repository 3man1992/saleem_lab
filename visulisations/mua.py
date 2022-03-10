# Custom Libraries requried
from utils.digital_filters import highpass_filtfilt

#OS libraries
from scipy.stats import zscore
import numpy as np

# #Function to calculate multiunit activity
# def filt_mua(lfp_data, fs):
#     print("Commencing filtering of multi unit activity")
#     start_time = time.time()  #Performance checks
#     filtered_data = butter_bandpass_filter(lfp_data,
#                                            lowcut = 500,
#                                            highcut = 3000,
#                                            fs = fs)
#     print("FiltFilt took: %s seconds to compute" % (time.time() - start_time)) #How long did filt filt take
#     return(filtered_data)

# #Smooth the filtered data with gaussian
# def gaussian_smooth(data):
#     """Uses a guassian filter from scipy
#     the window is calculated using int(truncate * sigma + 0.5)
#     this was taken from the scipy source code
#     Thus with a truncate of 8 and a sigma of 25, 200 samples are chosen
#     Which is approx 3ms as 60 samples per ms
#     6 samples per milisecond. So a 3ms window would be 18 sample window
#     Window is in millseconds if you want 500ms type 500"""
#
#     print("\nCommencing guassian smoothing of multi unit activity")
#     start_time = time.time()  #Performance checks
#     truncate = 8 #Truncate the filter at this many standard deviations. Default is 4.0.
#     sigma = 38
#     # sigma = 25 #Smoothing sigma - Tune - Is sigma the variance of the guassian
#     smoothed_lfp = gaussian_filter(input = data,
#                            sigma = sigma,
#                            truncate = truncate,
#                            mode = 'constant')
#     print("Smoothing took: %s seconds to compute" % (time.time() - start_time)) #How long did filt filt take
#     return smoothed_lfp

# #Threshold to binary
# def threshold_binary(filtered_lfp):
#     print("nCommencing thresholding of multi unit activity")
#     start_time = time.time()  #Time this function
#     zscore_threshold = 4.0 #What sd above mean should be considered multi unit activity
#     zscored_data = zscore(filtered_lfp) #Calculate z scores for smoothed lfp
#     print(zscored_data)
#     is_above_threshold = abs(zscored_data) >= zscore_threshold #Only consider data above threshold take absolute values
#     is_below_threshold = abs(zscored_data) < zscore_threshold #Only consider data above threshold take absolute values
#     shape_of_lfps = is_above_threshold.shape
#     none_mua_zero = np.where(is_above_threshold,
#                     filtered_lfp,
#                     0) #If above threshold pass through, else set mv to zero
#     binary_mua =    np.where(is_below_threshold,
#                     none_mua_zero,
#                     1) #If above threshold set to 1
#     print("Thresholding took: %s seconds to compute" % (time.time() - start_time)) #How long did filt filt take
#     assert binary_mua.shape == shape_of_lfps, "Error in shape of output"
#     return(binary_mua)

# #Threshold to binary
# def threshold(filtered_lfp):
#     """Take the whole filtered signal, zscore the whole array, return
#     mV that are more than 3sd away from mean. Else set to zero"""
#     print("nCommencing thresholding of multi unit activity")
#     start_time = time.time()  #Time this function
#     zscore_threshold = 3.0 #What sd above mean should be considered multi unit activity
#     zscored_data = zscore(filtered_lfp, axis=None) #Calculate z scores along whole array
#     is_above_threshold = abs(zscored_data) >= zscore_threshold #Only consider data above threshold take absolute values
#     is_below_threshold = abs(zscored_data) < zscore_threshold #Only consider data above threshold take absolute values
#     accepted_mua =  np.where(is_above_threshold,
#                     filtered_lfp,
#                     0) #If above threshold pass through, else set mili volts to zero
#     print("Thresholding took: %s seconds to compute" % (time.time() - start_time)) #How long did filt filt take
#     #Tests
#     shape_of_lfps = is_above_threshold.shape
#     assert accepted_mua.shape == shape_of_lfps, "Error in shape of output"
#     return(accepted_mua)


def z_score_signal(signal):
    """Takes in a signal and outputs the zscore"""
    assert len(signal) == len(zscore(signal, axis=None)), "Length of zscore array should match length of input array"
    return(zscore(signal, axis=None))  # Calculate z scores along whole array


def threshold_zcore(zcore_array, standard_deviation):
    """Takes in a zscore array and returns a boolean array which match threshold"""
    assert len(zcore_array) == len(abs(zcore_array) >= standard_deviation), "Length of zscore array should match length of boolean array"
    return(abs(zcore_array) >= standard_deviation)  # Only consider data above threshold take absolute values


def bin_and_count_activty_above_zthreshold(boolean_array, rows_to_count):
    """Takes in a boolean_array and counts the number of Trues in a bin.
    By reshaping into a higher dimensional array"""
    len_of_sample = len(boolean_array)
    if len_of_sample % rows_to_count != 0:
        remainder = len_of_sample % rows_to_count
        print("Removing {} samples to make divisible by requested bin window".format(remainder))
        boolean_array = boolean_array[:-int(remainder)]
    return(np.count_nonzero(boolean_array.reshape(-1, rows_to_count), axis=1))


def calculate_mua(signal, fs):
    """Takes in mV signal recordings, filters it with a highpass filt filt
    and then applys zscore thresholding and counts into defined bins of time"""
    mua_signal = highpass_filtfilt(signal, fs, 500)  # Highpass above 500hz
    zscored_signal = z_score_signal(mua_signal)  # What are the zscore values for the data
    threshold_zscore_boolean = threshold_zcore(zscored_signal, 2)  # Which mV recordings are above the threshold
    counted_binned_mua_activty = bin_and_count_activty_above_zthreshold(threshold_zscore_boolean, 300)  # 300 samples assumes a fs of 6000, and defines a 50ms bin
    return counted_binned_mua_activty

# # Takes x number of samples, averages them and returns a binned version
# # so numrow2avg = 5 will take every 5 rows avg and then return
# # Calculate samplign rate and then input that number of rows to average
# def average_and_bin_mua(mua, numrows_2_avg):
#     """Takes in a matrix, an averages the rows as per your input into bins"""
#     len_of_sample = len(mua[:, 0])
#     if len_of_sample % numrows_2_avg != 0:
#         remainder = len_of_sample % numrows_2_avg
#         print("Removing {} samples to make divisible by requested bin window".format(remainder))
#         mua = mua[:-remainder, :]
#     data = pd.DataFrame(mua)
#     return (pd.DataFrame(data.values.reshape(-1, numrows_2_avg, data.shape[1]).mean(1)))

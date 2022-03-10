#Custom Library
from sharp_wave_ripple_analysis import swr_detection

"""---------------"""

#Define paths
lfp = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/QBLU_Dark_Day5_250719.npy"
mat = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/QBLU_Dark_Day5_250719/extracted_position.mat"
file_save_name = "_test.npy"
channels = [8,9,10]

# lfp = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/QBLU_Dark_Day5_250719.npy"
# mat = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/QBLU_Dark_Day5_250719/extracted_position.mat"
# file_save_name = "_sleep_Ripples_for_QBLU_Dark_Day5_250719.npy"
# channels = [8,9,10]

# lfp = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/MBLU_Dark_Day10_090119.npy.npy"
# mat = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/MBLU_Dark_Day10_090119.npy/extracted_position.mat"
# file_save_name = "_sleep_Ripples_for_MBLU_Dark_Day10_090119.npy"
# # channels = [8,9,10]

# lfp = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/QBLU_YMaze_Day8_280719.npy"
# mat = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/QBLU_YMaze_Day8_280719/extracted_position.mat"
# file_save_name = "_sleep_Ripples_for_QBLU_YMaze_Day8_280719"
# channels = [8,9,10]

# lfp = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/Ymaze_Day3_220719.npy"
# mat = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/Ymaze_Day3_220719/extracted_position.mat"
# file_save_name = "_sleep_Ripples_for_Ymaze_Day3_220719"
# channels = [8,9,10]

# lfp = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/QBLU_YMaze_Day8_280719.npy"
# mat = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/QBLU_YMaze_Day8_280719/extracted_position.mat"
# file_save_name = '_sleep_Ripples_for_QBLU_YMaze_Day8_280719.npy'
# channels = [8,9,10]

# mat = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/QBLU_YMaze_Day7_270719/extracted_position.mat"
# lfp = '/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/QBLU_YMaze_Day7_270719.npy'
# file_save_name = '_sleep_Ripples_for_QBLU_YMaze_Day7_270719.npy'
# channels = [8,9,10]

# lfp = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/OBLU_YMaze_Day9_170519.npy"
# file_save_name = '_sleep_Ripples_for_OBLU_YMaze_Day9_170519.npy'
# mat = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/OBLU_YMaze_Day9_170519/extracted_position.mat"
# channels = [0,1,2,3]

# lfp = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/QBLU_Dark_Day9_290719.npy"
# mat = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/QBLU_Dark_Day9_290719/extracted_position.mat"
# file_save_name = '_sleep_Ripples_for_QBLU_Dark_Day9_290719.npy'
# channels = [8,9,10]

"""---------------"""
swr_detection.detect_SWRs(orgignal_fs = 30000,
                          new_fs = 2000,
                          lfp_data = lfp,
                          hippocampal_channels = channels,
                          saved_file_string = file_save_name,
                          mat_file = mat,
                          flag = "pre")

swr_detection.detect_SWRs(orgignal_fs = 30000,
                          new_fs = 2000,
                          lfp_data = lfp,
                          hippocampal_channels = channels,
                          saved_file_string = file_save_name,
                          mat_file = mat,
                          flag = "post")

#  Custom Library
from sharp_wave_ripple_analysis import swr_detection
from utils.meta_data import Meta

# Loop through every session and produce pre and post sleep ripple times
sessions = list(Meta().dictionary.keys())
for session in sessions:
    channels = Meta().dictionary[session]["hpc_chans"]
    mat = Meta().dictionary[session]["mat"]
    lfp = Meta().dictionary[session]["lfp"]
    file_save_name = "sleep_ripples_for" + "_" + session

    swr_detection.detect_SWRs(orgignal_fs=30000,
                              new_fs=6000,
                              lfp_data=lfp,
                              hippocampal_channels=channels,
                              saved_file_string=file_save_name,
                              mat_file=mat,
                              flag="pre")

    swr_detection.detect_SWRs(orgignal_fs=30000,
                              new_fs=6000,
                              lfp_data=lfp,
                              hippocampal_channels=channels,
                              saved_file_string=file_save_name,
                              mat_file=mat,
                              flag="post")

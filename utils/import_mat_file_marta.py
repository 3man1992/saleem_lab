from scipy.io import loadmat
from scipy import interpolate
import mat73
import numpy as np
import resampy

#Retreive additional behavioural data
event_dict = mat73.loadmat("/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/Dark_Day6_250719/extracted_events.mat")
pos_dict = loadmat("/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/Dark_Day6_250719/extracted_position.mat")
pos = pos_dict['position']['v_cm'].flatten()[0][0]
print("Position data loaded")

#hyper parameters
fs_of_cam = 25 #hz
fs_desired = 2000 #khz

#interpolate the rat velocity from 25Hz to 30kHz - v_cm
interp_vel = resampy.resample(pos, 25, 2000)
np.save("/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/Dark_day6_velocity.npy", interp_vel)
print("Lenght of interpolated velocity", len(interp_vel))

#Function to call from main processing script
def extract_velocities(file_path_of_position_data, file_location_to_save_velocity, file_name):
    pos_dict = loadmat(file_path_of_position_data)
    pos = pos_dict['position']['v_cm'].flatten()[0][0]
    interp_vel = resampy.resample(pos, 25, 30000) #Only change if sample rate changes but it shouldn't
    np.save(file_location_to_save_velocity + "/" + file_name)
    return None

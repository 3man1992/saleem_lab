"""Note this function seems to loose 200 + samples compared to
Tomazo's matlab implementation. Assuming this doesn't matter"""

#Custom libs
import neo as neo
import numpy as np

#A function to convert a list of ncs files to a numpy array of shape [num samples, channels]
def convert_ncs2_np(directory_path, save_to_path, saved_file_name):
    reader = neo.NeuralynxIO(dirname= directory_path)
    seg = reader.read_segment()
    anasig = seg.analogsignals[0]
    numpy_sig = anasig.rescale('uV').magnitude
    print("The shape of the saved array is: ", numpy_sig.shape)
    np.save(save_to_path + saved_file_name, numpy_sig)
    return None #saving the array is the function

#Insert strings to retrieve and save data as required
dir_path = '/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/Dark_Day6_250719/Raw_CSC'
save_to_path = '/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/' #Change this to where you want the data stored
saved_file_name = 'Dark_day6_2507_19.npy' #Change this to what you want the thing to be called
convert_ncs2_np(dir_path, save_to_path, saved_file_name)

#Load the pre-saved numpy array
# data = np.load("neo_array.npy")
# print(data.shape)

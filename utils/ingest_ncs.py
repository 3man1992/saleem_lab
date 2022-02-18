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
    print('ncs files have succesfully been converted into npy array')
    return None #saving the array is the function

"""Change the dir_path to the new directory containing your data, change the save to path to a preferred place on
your computer and name the file name. Remember that Raw CSC file as produced by martha has a space in it so you
have to replace the space with a underscore"""

#Insert strings to retrieve and save data as required
dir_path = '/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/QBLU_YMaze_Day8_280719'
save_to_path = '/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/np_arrays/' #Change this to where you want the data stored
saved_file_name = 'QBLU_YMaze_Day8_280719.npy' #Change this to what you want the thing to be called
convert_ncs2_np(dir_path, save_to_path, saved_file_name)

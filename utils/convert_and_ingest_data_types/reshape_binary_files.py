"""This scripts reshapes Tomaso's binary data into [timestamps / mv], channels"""

#Libaries
import pandas as pd
import numpy as np

#Import the binary file, and convert it from a 1d array to a 2d array with an index relating to channel number
class Import_and_Shape_Data():
    def __init__(self, binary_file_name, num_of_channels, sampling_frequency):
        self.num_of_channels = num_of_channels
        self.file = binary_file_name
        self.import_binary()
        self.reshape_binary_data()
        self.fs = sampling_frequency
        self.n = len(self.data[:, 0]) #selecting length of first channel to represent n samples

    #Convert binary file to numpy array
    def import_binary(self):
        self.raw_array = np.fromfile(self.file, dtype= 'int16', count=-1)
        self.length = len(self.raw_array)

    #Reshape binary file
    def reshape_binary_data(self):
        recordings = int(self.length / self.num_of_channels)
        data = np.reshape(self.raw_array, (recordings, self.num_of_channels))
        self.data = data
        return(data.astype(float))
        assert ((self.length % self.num_of_channels) == 0), "Modulo error, there is a remainder"
        assert data.shape[0] == self.length, "Shape is wrong"
        assert data.shape[1] == self.num_of_channels, "Shape is wrong"


#tests
#Load and shape data
# file = "/Users/freeman/Documents/saleem_lab/data/R21011_210915_CA1_1.csv"
# data_object = Import_and_Shape_Data(file)
# data = data_object.reshape_data()
# print(data)

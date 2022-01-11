#Libaries
import pandas as pd
import numpy as np

#Import the binary file, and convert it from a 1d array to a 2d array with an index relating to channel number
class Import_and_Shape_Data():
    def __init__(self, binary_file_name, num_of_channels = 64):
        self.num_of_channels = num_of_channels
        self.file = binary_file_name
        self.import_binary()
        self.reshape_data()

    #Convert binary file to numpy array
    def import_binary(self):
        self.raw_array = np.fromfile(self.file, dtype= 'uint16', count=- 1)
        self.length = len(self.raw_array) #for tests

    def reshape_data(self):
        recordings = int(self.length / self.num_of_channels)
        data = np.reshape(self.raw_array, (self.num_of_channels, recordings))
        self.data = data
        return(data)
        assert ((self.length % self.num_of_channels) == 0), "Modulo error, there is a remainder"

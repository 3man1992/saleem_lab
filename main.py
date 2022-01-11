from utils import reshape
import numpy as np
import matplotlib.pyplot as plt

#Load and shape data
file = "/Users/freeman/Documents/saleem_lab/data/R21011_210915_CA1_1.dat"
data_object = reshape.Import_and_Shape_Data(file)
data = data_object.reshape_data()

#Parameters
sample_rate = 20000
block_size = len(data[0])
frame_size = block_size / sample_rate

#Fourier trasnform
transform = np.fft.fft(data[0])
plt.plot(transform)
plt.show()

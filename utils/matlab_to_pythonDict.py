"""Often fellow lab members will work in MatLab and save their output in MatLab Structs.
This script is to help convert that struct away from nasty MatLab into Python

Input: file path of .mat file which is a struct
Returns: A python dictionary

Update - I had to do it mannually as there were structs within structs."""

from scipy.io import loadmat

class convert_matlab_struct:
    def __init__(self, file_path_of_struct):
        self.file = file_path_of_struct
        self.handle_keys()
        self.pull_out_field_names()

    #Convert matlab struct to an array and choose main key variable
    #Only works if struct doesn't contain more structs
    def handle_keys(self):
        self.dict = loadmat(self.file, squeeze_me = True, struct_as_record = True)
        print('\n####################################')
        print("\n-- The keys for this dictionary are: {}".format(self.dict.keys()))
        self.last_key = list(self.dict.keys())[-1]
        print("-- Selecting the last key | {} | assuming it contains all the data".format(self.last_key))
        self.array = self.dict[str(list(self.dict.keys())[-1])]
        print("-- Check the provided variables match the matlab struct: \n - {}".format(self.array.dtype.names))
        print('\n####################################\n')

    #Def pull out field names
    def pull_out_field_names(self):
        self.fields = self.array.dtype.names
        self.num_fields = len(self.fields)

    #Speific for application to handle structs within structs
    #Returns linear time stamps - Haven't figured out a way to do this automatically
    def extract_structs_within_structs(self):
        self.struct = loadmat(self.file, squeeze_me = True, struct_as_record = False)
        linear_time = self.struct[self.last_key].linear.timestamps
        time = self.struct[self.last_key].t
        velocity = self.struct[self.last_key].v_cm
        return (linear_time, time, velocity)

# file = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/Dark_Day6_250719/extracted_position.mat"
# x = convert_matlab_struct(file)
# linear_time = x.extract_structs_within_structs()
# print(len(linear_time))

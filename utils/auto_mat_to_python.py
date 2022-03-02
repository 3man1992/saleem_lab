"""Often fellow lab members will work in MatLab and save their output in MatLab Structs.
This script is to help convert that struct away from nasty MatLab into Python

Input: file path of .mat file which is a struct
Returns: A python dictionary"""

from scipy.io import loadmat
import scipy

class convert_matlab_struct:
    def __init__(self, file_path_of_mat):
        print("\nConverting your .mat into a Python Dictionary..")
        self.dictionary = self.convert_mat_file(file_path_of_mat)
        print("--Level 0 keys:", self.dictionary.keys())
        last_key = list(self.dictionary.keys())[-1]
        print("--Entering | {} | key and returning level 1 keys:\n\n".format(last_key), self.dictionary[last_key].keys())

        #Assigning level 1 keys to object - Level 2 keys will not be assigned to object
        #Thus if you have a struct with a struct. The keys for layer 2 struct will need to be
        #Accessed manually
        self.dic = {}
        for key in self.dictionary[last_key].keys():
            self.dic[key] = self.dictionary[last_key][key]

        print("""\nYour .mat file has now been uploaded into a python dictionary, Any structs within structs are now nested dictionaries. To access your L1 Dictionary keys. First create the object with the class. And then do obj.dic[key]. The keys for your level 2 dictionarys will need be created by you.\n""")

    def _todict(self, matobj):
        '''
        A recursive function which constructs from matobjects nested dictionaries
        '''
        dict = {}
        for strg in matobj._fieldnames:
            elem = matobj.__dict__[strg]
            if isinstance(elem, scipy.io.matlab.mat_struct):
                dict[strg] = self._todict(elem)
            else:
                dict[strg] = elem
        return dict

    def _check_keys(self, dict):
        '''
        checks if entries in dictionary are mat-objects. If yes
        todict is called to change them to nested dictionaries
        '''
        for key in dict:
            if isinstance(dict[key], scipy.io.matlab.mat_struct):
                dict[key] = self._todict(dict[key])
        return dict

    def convert_mat_file(self, filename):
        '''
        this function should be called instead of direct spio.loadmat
        as it cures the problem of not properly recovering python dictionaries
        from mat files. It calls the function check keys to cure all entries
        which are still mat-objects
        '''
        data = loadmat(filename, struct_as_record=False, squeeze_me=True)
        return self._check_keys(data)

#Test function works
# if __name__ == "__main__":
#     file = "/Users/freeman/Documents/saleem_folder/data/VC_Data_Marta/Dark_Day6_250719/extracted_position.mat"
#     obj = convert_matlab_struct(file)

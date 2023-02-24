from pathlib import Path
import pickle
import json
import pandas as pd

DATA_PATH = Path('/Users/francescopapaleo/Dropbox/Mac/Documents/git-box/streamlit/data/')
DATA_FILE = 'extended_descriptors_output.pickle'
OUTPUT_FILE ='ext_desc_converted.json'


# Open the pickle file in binary mode
with open(DATA_PATH / DATA_FILE, 'rb') as in_file:
    print('Iterate over all objects in the pickle file')
    while True:
        try:
            # Load the next object
            data = pickle.load(in_file)
            # Do something with the object (print it, process it, etc.)
            print(data)
        except EOFError:
            print('End of file reached')
            break

print('--------> Lenght :', len(data))

print('--------> Type :', type(data))

print('--------> Keys :', data.keys())

# print('--------> Values :', data.values())

print('--------> Items :', data.items())


### MAKE A DATAFRAME ###
df = pd.DataFrame(data, orient='index')
data.head(15)
data.shape
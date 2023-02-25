import pandas as pd
import pickle
import numpy as np

# load the pickle file
with open(DATA_PATH / DATA_FILE, 'rb') as handle:
    data = pickle.load(handle)

# create a list of dictionaries
dict_container = []
for file_path, features in data.items():
    # create a dictionary for each file_path and features
    feature_dict = {"file_path": file_path}
    for i, val in enumerate(features):
        if pd.isnull(val):
            val = "N/A"  # replace missing or NaN values with "N/A"
        feature_dict[f"feature_{i}"] = val
    dict_container.append(feature_dict)

# create a DataFrame
df = pd.DataFrame(dict_container)
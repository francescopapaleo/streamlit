import json
from pathlib import Path

#### FIX FILES PATH IN JSON ####

def fix_file_path(d):
    # Get the original file path
    orig_path = d['file']
    # Split the path into a directory and filename
    path_parts = orig_path.split('/')
    filename = path_parts[-1]
    directory = '/'.join(path_parts[:-1])
    # Replace any backslashes with forward slashes
    directory = directory.replace('\\', '/')
    # Combine the corrected directory and filename into a new path
    new_path = f'{directory}/{filename}'
    # Update the dictionary with the new file path
    d['file'] = new_path


DATA_DIR = Path('data')

# Open the input file for reading
with open(DATA_DIR / 'descriptors_rel_path.json', 'r') as f:
    # Parse the input data into a list of dictionaries
    data = json.load(f)

# Loop over each dictionary in the data list and correct the file path
for d in data:
    fix_file_path(d)

# Write the corrected data to a new file
with open(DATA_DIR / 'descriptors_dict_fix.json', 'w') as f:
    json.dump(data, f, indent=2)
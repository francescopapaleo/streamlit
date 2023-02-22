import os
import json
from pathlib import Path
import tqdm

from audio_descr_ext_class import AudioDescriptorsExtended

# Instantiate the class and compute the descriptors using a list as container for the results

DATA_DIR = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))) / 'data'

# MODIFY THIS LIST TO CONTAIN THE PATHS TO YOUR AUDIO FILES
# files_to_process = LIST_PATHS_TO_YOUR_AUDIO_FILES_HERE

# Instantiate the class
extended_descriptors = AudioDescriptorsExtended()

# Compute the descriptors and save them to a JSON list
all_features = []
for file_path in tqdm(files_to_process):
    features = extended_descriptors.compute_descriptors(file_path)
    all_features.append(features)

# Write the JSON list to a file with pretty-printing
with open(DATA_DIR / "extended_descriptors_output.json", "w") as f:
    json.dump(all_features, f, indent=4)

import os
import json
from pathlib import Path
import tqdm

from audio_descr_ext_class import AudioDescriptorsExtended

# instantiate the class
extended_descriptors = AudioDescriptorsExtended()
files_to_process = all_files_list[:100]

# compute the descriptors and save them to a json file at each iteration, one dict per line
with open("extended_descriptors_output.json", "w") as f:
    f.write("[")                # add opening bracket
    for i, file_path in enumerate(tqdm(files_to_process)):
        if i != 0:
            f.write(",")        # add comma between dicts
        features = extended_descriptors.compute_descriptors(file_path)
        json.dump(features, f, indent=0)
    f.write("]")                # add closing bracket
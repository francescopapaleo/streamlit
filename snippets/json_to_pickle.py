import json
import pickle
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / 'data'

### CONVERT JSON TO PICKLE ###

source = DATA_DIR / 'extended_descriptors_output_processed.json'
destination = DATA_DIR / 'converted_pickle.pickle'

with open(source, 'r') as f:
    tmp_data = json.load(f)

with open(destination, 'wb') as f:
    pickle.dump(tmp_data, f)
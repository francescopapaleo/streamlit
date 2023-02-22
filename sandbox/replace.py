import os
import json
from pathlib import Path
import re

DATA_DIR = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))) / 'data'

input = DATA_DIR / 'extended_descriptors_output.json'
output = DATA_DIR / 'extended_descriptors_output_processed.json'

# Open the file, read it, and then write it back out with the replacement

with open(input) as input_file:
    file_contents = input_file.read()

repl_contents = re.sub(r'\}(\s+)\{', r'},\1{', file_contents)   # replace }{ with },{

with open(output, 'w') as output_file:
    output_file.write(repl_contents)

# Load the file and check the length of the list

with open(output) as f:
    data = json.load(f)
    print(len(data))
    
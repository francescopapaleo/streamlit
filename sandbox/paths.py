import os
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve()
WORKING_DIR = Path(os.pardir).resolve()
DATASET_PATH = Path(WORKING_DIR, 'essentia-playlist')
EXAMPLES_PATH = Path(WORKING_DIR, 'examples')
AUDIO_PATH = Path(WORKING_DIR, 'audio')

print(CURRENT_DIR)
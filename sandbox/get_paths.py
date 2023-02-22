import os

AUDIO_PATH = '/home/username/Downloads/audios'

def get_files_absolute(path):
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list

audio_files_absolute = get_files_absolute(AUDIO_PATH)
len(audio_files_absolute)


def get_files_relative(path):
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_list.append(os.path.relpath(os.path.join(root, file), start=WORKING_DIR))
    return file_list

audio_files_relative = get_files_absolute(AUDIO_PATH)
len(audio_files_relative)
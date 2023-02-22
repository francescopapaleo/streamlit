# function to get a list of all audio files to be analysed under a folder 

def file_walker(dir_to_analyse, list_type):

    def get_files_abspath(dir_to_analyse):
        names_abs_list = []
        for (dirpath, dirnames, filenames) in os.walk(dir_to_analyse):
            for f in filenames:
                tmp_abs_path = os.path.join(dirpath, f)
                names_abs_list.append(tmp_abs_path)
        return names_abs_list

    def get_files_relpath(dir_to_analyse):
        names_rel_list = []
        for (dirpath, dirnames, filenames) in os.walk(dir_to_analyse):
            for f in filenames:
                tmp_rel_path = os.path.relpath(dirpath, dir_to_analyse)
                tmp_file_path = os.path.join(tmp_rel_path, f)
                names_rel_list.append(tmp_file_path)
        return names_rel_list

    def names_only(dir_to_analyse):
        names_list = []
        for (dirpath, dirnames, filenames) in os.walk(dir_to_analyse):
            for f in filenames:
                names_list.append(f)
        return names_list

    if list_type == 'abs':
        return get_files_abspath(dir_to_analyse)
    elif list_type == 'rel':
        return get_files_relpath(dir_to_analyse)
    elif list_type == 'names':
        return names_only(dir_to_analyse)
    else:
        print('Error: list_type must be either "abs" or "rel" or "names"')
        return None
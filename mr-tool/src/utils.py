import os
from constants import DB_RELATIVE_PATH


###
# Reads all the nested folders from the database
# and creates a dictionary of the form { 'Class': ['obj1', 'obj2'] }
#
def get_database_map() -> (dict[str, list[str]], int):
    folders = os.listdir(DB_RELATIVE_PATH)
    database_map: dict[str, list[str]] = dict()

    total_count = 0
    for folder in folders:
        if os.path.isdir(os.path.join(DB_RELATIVE_PATH, folder)):
            objects_list = []
            for file in os.listdir(os.path.join(DB_RELATIVE_PATH, folder)):
                objects_list.append(file)
                total_count += 1
            database_map[folder] = objects_list

    return database_map, total_count

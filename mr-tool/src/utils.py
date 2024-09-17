import os
import csv

from constants import OUTPUT_DIR_RELATIVE_PATH, STATS_FILE_NAME, STATS_FILE_HEADERS
from Mesh import MeshStats


###
# Reads all the nested folders from the database
# and creates a dictionary of the form { 'Class': ['obj1', 'obj2'] }
#
def get_database_map(db_path: str) -> (dict[str, list[str]], int):
    folders = os.listdir(db_path)
    database_map: dict[str, list[str]] = dict()

    total_count = 0
    for folder in folders:
        if os.path.isdir(os.path.join(db_path, folder)):
            objects_list = []
            for file in os.listdir(os.path.join(db_path, folder)):
                objects_list.append(file)
                total_count += 1
            database_map[folder] = objects_list

    return database_map, total_count


def save_output_stats(db_name: str, obj_stats: list[any]) -> str:
    if not os.path.exists(os.path.join(OUTPUT_DIR_RELATIVE_PATH, db_name)):
        os.makedirs(os.path.join(OUTPUT_DIR_RELATIVE_PATH, db_name))

    stats_file_path = os.path.join(OUTPUT_DIR_RELATIVE_PATH, db_name,
                                   STATS_FILE_NAME)
    with open(stats_file_path, mode='w') as stat_file:
        stat_writer = csv.writer(stat_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        stat_writer.writerow(STATS_FILE_HEADERS.split(","))

        for stat_row in obj_stats:
            stat_writer.writerow(stat_row)

    return str(stats_file_path)


def get_output_stats(db_name: str) -> list[MeshStats]:
    if not os.path.exists(os.path.join(OUTPUT_DIR_RELATIVE_PATH, db_name)):
        return []

    stats_file_path = os.path.join(OUTPUT_DIR_RELATIVE_PATH, db_name,
                                   STATS_FILE_NAME)

    statistics: list[MeshStats] = []
    with open(stats_file_path) as stat_file:
        stat_reader = csv.reader(stat_file, delimiter=',', quotechar='"')

        for idx, row in enumerate(stat_reader):
            if idx == 0:
                continue # Skip headers

            mesh_stats: MeshStats = MeshStats(row[0], row[1], int(row[2]), int(row[3]), int(row[4]), int(row[5]))
            statistics.append(mesh_stats)

    return statistics

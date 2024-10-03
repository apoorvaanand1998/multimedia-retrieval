import os
import csv
import datetime

import numpy as np
import vedo

from constants import OUTPUT_DIR_RELATIVE_PATH, STATS_FILE_NAME, STATS_FILE_HEADERS, DB_RELATIVE_PATH
from Mesh import MeshStats, Mesh


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


def save_array_to_txt(file_path: str, array: list[any]):
    f = open(file_path, 'w')
    for el in array:
        f.write(str(el))
        f.write("\n")
    f.close()


def save_output_stats(db_name: str, obj_stats: list[any]) -> str:
    if not os.path.exists(os.path.join(OUTPUT_DIR_RELATIVE_PATH, "Statistics", db_name)):
        os.makedirs(os.path.join(OUTPUT_DIR_RELATIVE_PATH, "Statistics", db_name))

    stats_file_path = os.path.join(OUTPUT_DIR_RELATIVE_PATH, "Statistics", db_name,
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

    stats_file_path = str(os.path.join(OUTPUT_DIR_RELATIVE_PATH, "Statistics",
                                       db_name, STATS_FILE_NAME))

    statistics: list[MeshStats] = []
    with open(stats_file_path) as stat_file:
        stat_reader = csv.reader(stat_file, delimiter=',', quotechar='"')

        for idx, row in enumerate(stat_reader):
            if idx == 0:
                continue  # Skip headers

            mesh_stats: MeshStats = MeshStats(row[1], row[2], int(row[3]), int(row[4]), int(row[5]), int(row[6]))
            statistics.append(mesh_stats)

    return statistics


def find_outliers(data: list[any]):
    # Convert list to a numpy array for easy computation
    data = np.array(data)

    # Calculate Q1 (25th percentile) and Q3 (75th percentile)
    Q1 = np.percentile(data, 25)
    Q3 = np.percentile(data, 75)

    # Compute the IQR
    IQR = Q3 - Q1

    # Calculate the lower and upper bounds
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Find outliers
    # outliers_lower = data[(data < lower_bound)][:2]
    # outliers_upper = data[(data > upper_bound)][:2]
    outliers = data[(data < lower_bound) | (data > upper_bound)][:2]

    return outliers


def save_to_db(mesh: Mesh, db_name: str):
    final_path = None
    if mesh is not None:
        db_path = str(os.path.join(DB_RELATIVE_PATH, db_name, mesh.get_class()))
        if not os.path.exists(db_path):
            os.makedirs(db_path)

        final_path = str(os.path.join(db_path, mesh.name))
        vedo.save(mesh.vedo_mesh, final_path)

    return final_path


def get_time_from_seconds(seconds: float) -> str:
    return str(datetime.timedelta(seconds=666))

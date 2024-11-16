import os
import csv
import time

import numpy as np
import vedo

import anand

from constants import OUTPUT_DIR_RELATIVE_PATH, STATS_FILE_NAME, STATS_FILE_HEADERS, DB_RELATIVE_PATH, \
    DESCRIPTORS_FILE_NAME, DESCRIPTORS_FILE_HEADERS
from Mesh import MeshStats, Mesh, MeshDescriptors


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


def save_vertices_to_txt(file_path: str, vertices):
    with open(file_path, mode='w') as stat_file:
        stat_writer = csv.writer(stat_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for mesh_vertices in vertices:
            stat_writer.writerow(mesh_vertices)

    return str(file_path)


def get_vertices_from_txt(file_path: str) -> list[list[float]]:
    vertices: list[list[float]] = []
    with open(file_path) as stat_file:
        stat_reader = csv.reader(stat_file, delimiter=',', quotechar='"')

        for idx, row in enumerate(stat_reader):
            mesh_vertices: list[float] = []
            for vertex in row:
                vertex = vertex.strip("[]").split()
                mesh_vertices.append([float(v) for v in vertex])
            vertices.append(mesh_vertices)

    return vertices


def save_output_descriptors(db_name: str, obj_descriptors: list[MeshDescriptors]) -> str:
    if not os.path.exists(os.path.join(OUTPUT_DIR_RELATIVE_PATH, "Descriptors", db_name)):
        os.makedirs(os.path.join(OUTPUT_DIR_RELATIVE_PATH, "Descriptors", db_name))

    descriptors_file_path = os.path.join(OUTPUT_DIR_RELATIVE_PATH, "Descriptors", db_name,
                                         DESCRIPTORS_FILE_NAME)
    with open(descriptors_file_path, mode='w') as stat_file:
        stat_writer = csv.writer(stat_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        stat_writer.writerow(DESCRIPTORS_FILE_HEADERS.split(","))

        # Path,Name,Class,Surface Area,Compactness,3D Rectangularity,Diameter,Convexity,Eccentricity, A3, D1, D2, D3, D4
        for descriptors_row in obj_descriptors:
            row = [descriptors_row.path, descriptors_row.name, descriptors_row.get_class(),
                   descriptors_row.surface_area, descriptors_row.compactness,
                   descriptors_row.rectangularity, descriptors_row.diameter,
                   descriptors_row.convexity, descriptors_row.eccentricity,
                   descriptors_row.a3, descriptors_row.d1,
                   descriptors_row.d2, descriptors_row.d3,
                   descriptors_row.d4]
            stat_writer.writerow(row)

    return str(descriptors_file_path)


def save_output_descriptors_one(db_name: str, descriptors: MeshDescriptors) -> str:
    if not os.path.exists(os.path.join(OUTPUT_DIR_RELATIVE_PATH, "Descriptors", db_name)):
        os.makedirs(os.path.join(OUTPUT_DIR_RELATIVE_PATH, "Descriptors", db_name))

    descriptors_file_path = os.path.join(OUTPUT_DIR_RELATIVE_PATH, "Descriptors", db_name,
                                         DESCRIPTORS_FILE_NAME)

    data = get_output_descriptors(db_name)
    if len(data) == 0:
        save_output_descriptors(db_name, [descriptors])
        return str(descriptors_file_path)

    idx = -1
    for i, desc in enumerate(data):
        if desc.path == descriptors.path and desc.name == descriptors.name and desc.get_class() == descriptors.get_class():
            idx = i
            break

    if idx != -1:
        data[idx] = descriptors
    else:
        data.append(descriptors)

    save_output_descriptors(db_name, data)

    return str(descriptors_file_path)


def get_output_descriptors(db_name: str) -> list[MeshDescriptors]:
    if not os.path.exists(os.path.join(OUTPUT_DIR_RELATIVE_PATH, "Descriptors", db_name, DESCRIPTORS_FILE_NAME)):
        return []

    descriptors_file_path = str(os.path.join(OUTPUT_DIR_RELATIVE_PATH, "Descriptors",
                                             db_name, DESCRIPTORS_FILE_NAME))

    descriptors: list[MeshDescriptors] = []
    with open(descriptors_file_path) as stat_file:
        stat_reader = csv.reader(stat_file, delimiter=',', quotechar='"')

        for idx, row in enumerate(stat_reader):
            if idx == 0:
                continue  # Skip headers

            mesh_descriptors: MeshDescriptors = MeshDescriptors(row[0], row[1], row[2],
                                                                float(row[3]) if row[3] != '' else None,
                                                                float(row[4]) if row[4] != '' else None,
                                                                float(row[5]) if row[5] != '' else None,
                                                                float(row[6]) if row[6] != '' else None,
                                                                float(row[7]) if row[7] != '' else None,
                                                                float(row[8]) if row[8] != '' else None)

            if len(row) > 9:
                # shape desc
                a3_str = row[9].replace("[", "").replace("]", "").replace("\n", " ").split()
                a3 = np.array(a3_str, dtype=float)
                mesh_descriptors.set_a3(a3)

                d1_str = row[10].replace("[", "").replace("]", "").replace("\n", " ").split()
                d1 = np.array(d1_str, dtype=float)
                mesh_descriptors.set_d1(d1)

                d2_str = row[11].replace("[", "").replace("]", "").replace("\n", " ").split()
                d2 = np.array(d2_str, dtype=float)
                mesh_descriptors.set_d2(d2)

                d3_str = row[12].replace("[", "").replace("]", "").replace("\n", " ").split()
                d3 = np.array(d3_str, dtype=float)
                mesh_descriptors.set_d3(d3)

                d4_str = row[13].replace("[", "").replace("]", "").replace("\n", " ").split()
                d4 = np.array(d4_str, dtype=float)
                mesh_descriptors.set_d4(d4)

            descriptors.append(mesh_descriptors)

    return descriptors


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
    if not os.path.exists(os.path.join(OUTPUT_DIR_RELATIVE_PATH, "Statistics", db_name)):
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
    return time.strftime("%H:%M:%S", time.gmtime(seconds))

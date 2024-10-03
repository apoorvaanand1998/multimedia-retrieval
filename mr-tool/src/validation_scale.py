import csv
import math
import os
import matplotlib.pyplot as plt
import numpy as np
import vedo

from Mesh import Mesh
import utils
from constants import OUTPUT_DIR_RELATIVE_PATH

statistics_folder = os.path.join(OUTPUT_DIR_RELATIVE_PATH, "Statistics",
                                 "ShapeDatabase_INFOMR_preprocessed_no_resample")
statistics_scale_before_file = "scale_before.txt"
statistics_scale_after_file = "scale_after.txt"


def parse(list: str):
    # Step 1: Split the string into individual lists
    list_strings = list.split('\n')

    # Step 2: Remove brackets and convert to list of lists
    result = []
    for item in list_strings:
        # Remove brackets and split by space, then convert to floats
        numbers = item.strip("[]").split()
        # Convert strings to floats and add to result
        result.append([float(num) for num in numbers])

    return result


def generate_scale_evidence_one(db_name: str, file_name: str):
    db_map, db_total_count = utils.get_database_map("../../" + db_name)

    map: dict[str, float] = dict()

    for obj_class, obj_list in db_map.items():
        for obj in obj_list:
            path = str(os.path.join("..", "..", db_name, obj_class, obj))
            mesh = Mesh(path)
            highest_dimension = mesh.get_value_of_largest_bbox_dimension()

            map[path] = highest_dimension

    with open(file_name, mode='w') as stat_file:
        stat_writer = csv.writer(stat_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        stat_writer.writerow("Path,Highest_Dim".split(","))

        for key in map:
            stat_row = [key, map[key]]
            stat_writer.writerow(stat_row)
    print("Wrote " + file_name)


def generate_scale_evidence():
    generate_scale_evidence_one("ShapeDatabase_INFOMR",
                                os.path.join(statistics_folder, statistics_scale_before_file))
    generate_scale_evidence_one("ShapeDatabase_INFOMR_preprocessed_no_resample",
                                os.path.join(statistics_folder, statistics_scale_after_file))


def histogram(points, title, granularity=False):
    fig, ax = plt.subplots()

    points = np.array(points)
    points = points[abs(points - np.mean(points)) < 2 * np.std(points)]

    # n_bins = int(math.sqrt(points.shape[0]))
    bins = np.linspace(0, 4, 30)

    # ax.hist(points, n_bins, density=True, histtype='bar', stacked=True)
    N, bins, patches = ax.hist(points, bins=bins, log=False)
    # ax.set_ylim([0, 3000])
    # if granularity:
        # plt.yscale('log')
        # plt.yticks(np.arange(0, 10000, 1000))
        # plt.yticks([0, 10, 100, 1000, 10000])
    ax.set_title(title)

    plt.show()

def main():
    # path_before = os.path.join(statistics_folder, statistics_scale_before_file)
    # path_after = os.path.join(statistics_folder, statistics_scale_after_file)
    # if not os.path.exists(path_before) or not os.path.exists(path_after):
    # generate_scale_evidence()


    file_before = os.path.join(statistics_folder, statistics_scale_before_file)
    before: list[float] = []
    with open(file_before) as stat_file:
        stat_reader = csv.reader(stat_file, delimiter=',', quotechar='"')

        for idx, row in enumerate(stat_reader):
            if idx == 0:
                continue  # Skip headers

            before.append(float(row[1]))

    file_after = os.path.join(statistics_folder, statistics_scale_after_file)
    after: list[float] = []
    with open(file_after) as stat_file:
        stat_reader = csv.reader(stat_file, delimiter=',', quotechar='"')

        for idx, row in enumerate(stat_reader):
            if idx == 0:
                continue  # Skip headers

            after.append(float(row[1]))

    for x in after:
        if x < 0:
            print('x')

    histogram(before, "Highest dimension's value BEFORE")
    histogram(after, "Highest dimension's value AFTER", True)


main()

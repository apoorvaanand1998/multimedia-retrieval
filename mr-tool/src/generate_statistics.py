import math
import os
import matplotlib.pyplot as plt
import ast
import numpy as np
from constants import OUTPUT_DIR_RELATIVE_PATH

statistics_folder = os.path.join(OUTPUT_DIR_RELATIVE_PATH, "Statistics", "ShapeDatabase_INFOMR_preprocessed_no_resample")
statistics_scale_before_file = "scale_before.txt"
statistics_scale_after_file = "scale_after.txt"
statistics_translation_before_file = "translation_before.txt"
statistics_translation_after_file = "translation_after.txt"


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


def histogram(points, title):
    fig, ax = plt.subplots()

    points = np.array(points)

    n_bins = int(math.sqrt(points.shape[0]))
    bins = np.linspace(0, 1e-3, 60)

    # ax.hist(points, n_bins, density=True, histtype='bar', stacked=True)
    N, bins, patches = ax.hist(points, bins=bins, log=False)
    ax.set_title(title)

    fig.tight_layout()
    plt.show()

def scatter_plot(points, title):
    plt.title(title)

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    points = [sublist for sublist in points if sublist]

    xs = [sublist[0] for sublist in points]
    ys = [sublist[1] for sublist in points]
    zs = [sublist[2] for sublist in points]
    ax.set_xlim(min(xs), max(xs))
    ax.set_ylim(min(ys), max(ys))
    ax.set_zlim(min(zs), max(zs))
    ax.set_xticks(np.arange(0, 1001, 100))  # Change increments as needed
    ax.set_yticks(np.arange(0, 1001, 100))  # Adjust for y-axis if necessary
    ax.set_zticks(np.arange(0, 1001, 100))  # Adjust for z-axis if necessary

    for idx, point in enumerate(points):
        ax.scatter(point[0], point[1], point[2], marker='o')

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    plt.show()


def main():
    # DB Translation Statistics
    file = open(os.path.join(statistics_folder, statistics_scale_before_file), 'r')
    scale_before = file.read()
    file.close()

    file = open(os.path.join(statistics_folder, statistics_scale_after_file), 'r')
    scale_after = file.read()
    file.close()

    # DB Scale Statistics
    file = open(os.path.join(statistics_folder, statistics_translation_before_file), 'r')
    translation_before = parse(file.read())
    translation_before = [sublist for sublist in translation_before if sublist] # last element is empty. I m lazy
    distances_from_origin_before = []
    for point in translation_before:
        distance = math.sqrt(point[0]**2 + point[1]**2 + point[2]**2)
        distances_from_origin_before.append(distance)
    file.close()

    file = open(os.path.join(statistics_folder, statistics_translation_after_file), 'r')
    translation_after = parse(file.read())
    translation_after = [sublist for sublist in translation_after if sublist] # last element is empty. I m lazy
    distances_from_origin_after = []
    for point in translation_after:
        distance = math.sqrt(point[0]**2 + point[1]**2 + point[2]**2)
        distances_from_origin_after.append(distance)
    file.close()

    # scatter_plot(translation_before, "Translation Before")
    # scatter_plot(translation_after, "Translation After")
    histogram(distances_from_origin_before, "Distances from origin BEFORE")
    histogram(distances_from_origin_after, "Distances from origin AFTER")


main()

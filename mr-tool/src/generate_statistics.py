import csv
import math
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from utils import get_vertices_from_txt
from constants import OUTPUT_DIR_RELATIVE_PATH

statistics_folder = os.path.join(OUTPUT_DIR_RELATIVE_PATH, "Statistics", "remeshed_ShapeDB_normalized_all")
statistics_scale_before_file = "scale_before.txt"
statistics_scale_after_file = "scale_after.txt"
statistics_translation_before_file = "translation_before.txt"
statistics_translation_after_file = "translation_after.txt"
statistics_align_pca_before_file = "align_pca_before.txt"
statistics_align_pca_after_file = "align_pca_after.txt"
statistics_flip_before_file = "flip_before.txt"
statistics_flip_after_file = "flip_after.txt"


def parse(list: str):
    # Step 1: Split the string into individual lists
    list_strings = list.split('\n')

    # Step 2: Remove brackets and convert to list of lists
    result = []
    for item in list_strings:
        # Remove brackets and split by space, then convert to floats
        numbers = item.strip("[]").split()

        numbers = [n.strip(",") for n in numbers]

        # Convert strings to floats and add to result
        result.append([float(num) for num in numbers])

    return result


def plot_histograms_align_pca(meshes_vertices, title):
    x_coords = meshes_vertices[0]
    y_coords = meshes_vertices[1]
    z_coords = meshes_vertices[2]

    # Plot histograms for each coordinate axis
    fig, ax = plt.subplots(1, 3, figsize=(15, 5))

    n_bins = int(math.sqrt(len(x_coords)))

    ax[0].hist(x_coords, bins=n_bins, color=['r'] * len(x_coords), log=True, alpha=0.7)
    ax[0].set_title("X-axis (Largest PC)")

    ax[1].hist(y_coords, bins=n_bins, color=['g'] * len(y_coords), log=True, alpha=0.7)
    ax[1].set_title("Y-axis (2nd Largest PC)")

    ax[2].hist(z_coords, bins=n_bins, color=['b'] * len(z_coords), log=True, alpha=0.7)
    ax[2].set_title("Z-axis (Smallest PC)")

    plt.suptitle(title)
    plt.show()

def plot_histograms_align_pca_variance(meshes_variances, title):
    x_variances = meshes_variances[0]
    y_variances = meshes_variances[1]
    z_variances = meshes_variances[2]

    # Plot histograms for each coordinate axis
    fig, ax = plt.subplots(1, 3, figsize=(15, 5))

    n_bins = int(math.sqrt(len(x_variances)))

    ax[0].hist(x_variances, bins=n_bins, color='r', log=True, alpha=0.7)
    ax[0].set_title("X-axis Variances (Largest PC)")

    ax[1].hist(y_variances, bins=n_bins, color='g', log=True, alpha=0.7)
    ax[1].set_title("Y-axis Variances (2nd Largest PC)")

    ax[2].hist(z_variances, bins=n_bins, color='b', log=True, alpha=0.7)
    ax[2].set_title("Z-axis Variances (Smallest PC)")

    plt.suptitle(title)
    plt.show()


def plot_histograms_flip(means_per_axis, title):
    means_per_axis = np.array(means_per_axis)
    x_coords = means_per_axis[:, 0]
    y_coords = means_per_axis[:, 1]
    z_coords = means_per_axis[:, 2]

    # Plot histograms for each coordinate axis
    fig, ax = plt.subplots(1, 3, figsize=(15, 5))

    ax[0].hist(x_coords, bins=30, color=['r'], alpha=0.7)
    ax[0].set_title("X-axis (Largest PC)")

    ax[1].hist(y_coords, bins=30, color=['g'], alpha=0.7)
    ax[1].set_title("Y-axis (2nd Largest PC)")

    ax[2].hist(z_coords, bins=30, color=['b'], alpha=0.7)
    ax[2].set_title("Z-axis (Smallest PC)")

    plt.suptitle(title)
    plt.show()




def histogram_translation(points, title):
    fig, ax = plt.subplots()

    points = np.array(points)

    n_bins = int(math.sqrt(points.shape[0]))
    bins = np.linspace(0, 1e-1, 60)

    # ax.hist(points, n_bins, density=True, histtype='bar', stacked=True)
    N, bins, patches = ax.hist(points, bins=bins, log=False)
    ax.set_title(title)

    fig.tight_layout()
    plt.show()


def histogram_scale(points, title, granularity=False):
    fig, ax = plt.subplots()

    points = np.array(points)
    points = points[abs(points - np.mean(points)) < 2 * np.std(points)]

    # n_bins = int(math.sqrt(points.shape[0]))
    bins = np.linspace(0, 6, 30)

    # ax.hist(points, n_bins, density=True, histtype='bar', stacked=True)
    N, bins, patches = ax.hist(points, bins=bins, log=False)
    # ax.set_ylim([0, 3000])
    # if granularity:
    # plt.yscale('log')
    # plt.yticks(np.arange(0, 10000, 1000))
    # plt.yticks([0, 10, 100, 1000, 10000])
    ax.set_title(title)

    plt.show()


def translation():
    file = open(os.path.join(statistics_folder, statistics_translation_before_file), 'r')
    translation_before = parse(file.read())
    translation_before = [sublist for sublist in translation_before if sublist]  # last element is empty. I m lazy
    distances_from_origin_before = []
    for point in translation_before:
        distance = math.sqrt(point[0] ** 2 + point[1] ** 2 + point[2] ** 2)
        distances_from_origin_before.append(distance)
    file.close()

    file = open(os.path.join(statistics_folder, statistics_translation_after_file), 'r')
    translation_after = parse(file.read())
    translation_after = [sublist for sublist in translation_after if sublist]  # last element is empty. I m lazy
    distances_from_origin_after = []
    for point in translation_after:
        distance = math.sqrt(point[0] ** 2 + point[1] ** 2 + point[2] ** 2)
        distances_from_origin_after.append(distance)
    file.close()

    histogram_translation(distances_from_origin_before, "Distances from origin BEFORE")
    histogram_translation(distances_from_origin_after, "Distances from origin AFTER")


def scale():
    file_before = os.path.join(statistics_folder, statistics_scale_before_file)
    before: list[float] = []
    with open(file_before) as stat_file:
        stat_reader = csv.reader(stat_file, delimiter=',', quotechar='"')

        for idx, row in enumerate(stat_reader):
            if idx == 0:
                continue  # Skip headers

            before.append(float(row[0]))

    file_after = os.path.join(statistics_folder, statistics_scale_after_file)
    after: list[float] = []
    with open(file_after) as stat_file:
        stat_reader = csv.reader(stat_file, delimiter=',', quotechar='"')

        for idx, row in enumerate(stat_reader):
            if idx == 0:
                continue  # Skip headers

            after.append(float(row[0]))

    for x in after:
        if x < 0:
            print('x')

    histogram_scale(before, "Highest dimension's value BEFORE")
    histogram_scale(after, "Highest dimension's value AFTER", True)


def plot_variance_heatmap(objects_variances, title):
    """
    Plots a heatmap of variances for multiple objects across principal components.

    objects_eigenvalues: List of lists, where each inner list contains the
                         eigenvalues for an object.
    """
    plt.figure(figsize=(10, 6))
    sns.heatmap(objects_variances, cmap="coolwarm", cbar=True)

    # Add labels and title
    plt.title(title)
    plt.xlabel("Principal Components")
    plt.ylabel("Objects")
    plt.xticks([0.5, 1.5, 2.5], ['PC1 (X)', 'PC2 (Y)', 'PC3 (Z)'], rotation=0)

    plt.tight_layout()
    plt.show()

def align_pca():
    align_pca_before = get_vertices_from_txt(os.path.join(statistics_folder, statistics_align_pca_before_file))
    align_pca_before = [sublist for sublist in align_pca_before if sublist]  # last element is empty. I m lazy
    x_coords = []
    y_coords = []
    z_coords = []
    # x_variance = []
    # y_variance = []
    # z_variance = []
    variances_per_axis_per_object_before = []
    for mesh_vertices in align_pca_before:
        mesh_vertices = np.array(mesh_vertices)
        x_coords.append(mesh_vertices[:, 0])
        y_coords.append(mesh_vertices[:, 1])
        z_coords.append(mesh_vertices[:, 2])
        variances_per_axis_per_object_before.append([
            np.var(mesh_vertices[:, 0]),
            np.var(mesh_vertices[:, 1]),
            np.var(mesh_vertices[:, 2])
        ])
        # x_variance.append(np.var(mesh_vertices[:, 0]))
        # y_variance.append(np.var(mesh_vertices[:, 1]))
        # z_variance.append(np.var(mesh_vertices[:, 2]))
    # variances_per_axes_before = [x_variance, y_variance, z_variance]
    v_per_axes_before = [x_coords, y_coords, z_coords]

    align_pca_after = get_vertices_from_txt(os.path.join(statistics_folder, statistics_align_pca_after_file))
    align_pca_after = [sublist for sublist in align_pca_after if sublist]  # last element is empty. I m lazy
    x_coords = []
    y_coords = []
    z_coords = []
    x_variance = []
    y_variance = []
    z_variance = []
    variances_per_axis_per_object_after = []
    for mesh_vertices in align_pca_after:
        mesh_vertices = np.array(mesh_vertices)
        x_coords.append(mesh_vertices[:, 0])
        y_coords.append(mesh_vertices[:, 1])
        z_coords.append(mesh_vertices[:, 2])
        variances_per_axis_per_object_after.append([
            np.var(mesh_vertices[:, 0]),
            np.var(mesh_vertices[:, 1]),
            np.var(mesh_vertices[:, 2])
        ])
        # x_variance.append(np.var(mesh_vertices[:, 0]))
        # y_variance.append(np.var(mesh_vertices[:, 1]))
        # z_variance.append(np.var(mesh_vertices[:, 2]))
    # variances_per_axes_after = [x_variance, y_variance, z_variance]
    v_per_axes_after = [x_coords, y_coords, z_coords]

    # plot_histograms_align_pca(v_per_axes_before, "Distribution of Vertices per Axes BEFORE")
    # plot_histograms_align_pca(v_per_axes_after, "Distribution of Vertices per Axes AFTER")
    # plot_histograms_align_pca_variance(variances_per_axes_before, "Variance of Vertices per Axes BEFORE")
    # plot_histograms_align_pca_variance(variances_per_axes_after, "Variance of Vertices per Axes AFTER")
    plot_variance_heatmap(variances_per_axis_per_object_before, "Variance Heatmap Across Principal Components BEFORE")
    plot_variance_heatmap(variances_per_axis_per_object_after, "Variance Heatmap Across Principal Components AFTER")
    # print(variances_per_axes_before)
    # print(variances_per_axes_after)


def flip():
    file = open(os.path.join(statistics_folder, statistics_flip_before_file), 'r')
    flip_before = parse(file.read())
    flip_before = [sublist for sublist in flip_before if sublist]  # last element is empty. I m lazy
    means_before = []
    for mean_per_axis in flip_before:
        means_before.append(mean_per_axis)
    file.close()

    file = open(os.path.join(statistics_folder, statistics_flip_after_file), 'r')
    flip_after = parse(file.read())
    flip_after = [sublist for sublist in flip_after if sublist]  # last element is empty. I m lazy
    means_after = []
    for mean_per_axis in flip_after:
        means_after.append(mean_per_axis)
    file.close()

    plot_histograms_flip(means_before, "Mean per axis BEFORE")
    plot_histograms_flip(means_after, "Mean per axis AFTER")


def main():
    translation()
    scale()
    align_pca()
    flip()


main()

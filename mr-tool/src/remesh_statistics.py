import matplotlib.pyplot as plt
import numpy as np
import utils

def box_plot(data, title):
    data = np.array(data)

    fig, ax = plt.subplots()

    bplot = ax.boxplot(data)

    plt.title(title)
    plt.show()

def histogram(original_data, remeshed_data):
    original_data = np.array(original_data)
    remeshed_data = np.array(remeshed_data)

    # Plot the first histogram
    counts, bins, patches = plt.hist(original_data, bins=30, alpha=0.5, label='Original Distribution', color='blue', log=True, linewidth=1.5)


    # Plot the second histogram with different styling for highlight
    counts, bins, patches = plt.hist(remeshed_data, bins=30, alpha=0.7, label='Remeshed Distribution', color='pink', linewidth=1.5, log=True)


    # Adding legend and labels
    plt.legend()
    plt.xlabel('Number of cells')
    plt.ylabel('Number of objects')
    plt.title('Original vs. Remeshed distributions')

    # Show the plot
    plt.show()

def main():
    stats_original = utils.get_output_stats("ShapeDatabase_INFOMR")
    no_vertices_original = []
    for stat in stats_original:
        no_vertices_original.append(float(stat.no_cells))

    stats_remeshed = utils.get_output_stats("remeshed_ShapeDB")
    no_vertices_remeshed = []
    for stat in stats_remeshed:
        no_vertices_remeshed.append(float(stat.no_cells))

    # box_plot(no_vertices_original, "Original")
    # box_plot(no_vertices_remeshed, "Remeshed")
    histogram(no_vertices_original, no_vertices_remeshed)

main()
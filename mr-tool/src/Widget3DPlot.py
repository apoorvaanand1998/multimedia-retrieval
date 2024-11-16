import random

import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from Mesh import Mesh
from mpl_toolkits.mplot3d import Axes3D
from vedo import Plotter, Points
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class Widget3DPlot(QWidget):
    _maximum_points = 100

    _ui_layout_main: QVBoxLayout = None
    _ui_vedo_widget: QVTKRenderWindowInteractor = None

    _vedo_plotter: Plotter = None

    def __init__(self, points: list[list[float]], evidentiate: list[list[float]] = None, parent=None):
        super().__init__(parent)

        # Create a matplotlib figure
        self.figure = Figure(tight_layout=True)
        self.canvas = FigureCanvas(self.figure)

        # Create a layout and add the canvas to the widget
        self._ui_layout_main = QVBoxLayout()
        self._ui_layout_main.addWidget(self.canvas)
        self.setLayout(self._ui_layout_main)

        # Call the method to draw the bar chart
        self.plot_scatter_3d(points, evidentiate)

    def plot_scatter_3d(self, points: list[list[float]], evidentiate: list[list[float]] = None):
        if len(points) > self._maximum_points:
            points = random.sample(points, self._maximum_points)
        # Create a new figure and a 3D subplot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Unzip the points list into separate x, y, and z coordinate lists
        x_coords, y_coords, z_coords = zip(*points)

        # Plot the points
        ax.scatter(x_coords, y_coords, z_coords, marker='o', color='b')

        if evidentiate is not None:
            for point in evidentiate:
                ax.scatter(point[0], point[1], point[2], marker='D', c='r')

        # Set labels and title
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        ax.set_title('3D Scatter Plot')

        # Show the plot
        plt.show()

        return

        # for optimization reasons, sample maximum N
        # points
        if len(points) > self._maximum_points:
            points = random.sample(points, self._maximum_points)

        # Create an axis
        ax = self.figure.add_subplot(projection='3d')

        def randrange(n, vmin, vmax):
            """
            Helper function to make an array of random numbers having shape (n, )
            with each number distributed Uniform(vmin, vmax).
            """
            return (vmax - vmin) * np.random.rand(n) + vmin

        # Clear previous plots
        ax.clear()

        for point in points:
            ax.scatter(point[0], point[1], point[2], marker='o', c='b')

        if evidentiate is not None:
            for point in evidentiate:
                ax.scatter(point[0], point[1], point[2], marker='D', c='r')

        # Set labels and title
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        ax.set_title('Test 3D Scatter')

        # Redraw the canvas
        self.canvas.draw()

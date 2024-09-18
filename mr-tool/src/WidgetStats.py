import math

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from WidgetHistogram import WidgetHistogram
from WidgetBarChart import WidgetBarChart
from Mesh import MeshStats
import utils


class WidgetStats(QWidget):
    _ui_layout_main: QVBoxLayout = None

    _ui_label_title: QLabel = None

    def __init__(self, db_map: dict[str, list[str]], db_count: int, db_name: str):
        super().__init__()

        self.db_map = db_map
        self.db_count = db_count
        self.db_name = db_name

        self.meshes_stats: list[MeshStats] = utils.get_output_stats(self.db_name)

        self._ui_layout_main = QVBoxLayout()

        self._ui_label_title = QLabel(self.db_name)

        self._ui_layout_main.addWidget(self._ui_label_title)

        # Diagram
        layout_diagrams = QVBoxLayout()

        # BarChart of class distribution
        layout_diagrams.addWidget(self.create_barchart_classes())

        # Histogram of faces
        layout_diagrams.addWidget(self.create_histogram_faces())

        # Histogram of vertices
        layout_diagrams.addWidget(self.create_histogram_vertices())

        self._ui_layout_main.addLayout(layout_diagrams)

        # Average shape vedo plot

        # Outliers shapes

        self.setLayout(self._ui_layout_main)

    def create_barchart_classes(self):
        classes_labels = list(self.db_map.keys())
        counts = [len(sublist) for sublist in list(self.db_map.values())]

        return WidgetBarChart(
            counts,
            classes_labels,
            self
        )

    def create_histogram_faces(self):
        # Analyzing the range of data
        list_cells = []
        min_no_faces = self.meshes_stats[0].no_cells
        max_no_faces = self.meshes_stats[0].no_cells
        for mesh_stat in self.meshes_stats:
            if min_no_faces > mesh_stat.no_cells:
                min_no_faces = mesh_stat.no_cells
            if max_no_faces < mesh_stat.no_cells:
                max_no_faces = mesh_stat.no_cells
            list_cells.append(mesh_stat.no_cells)
        range_no_faces = max_no_faces - min_no_faces

        # Divide the range into equally-divided bins
        # The numbers of bins for this can be found with
        # bins = sqrt(len(list))
        # TODO: Search for some proper proof of this to add to the report. I just did ChatGPT
        no_bins = math.sqrt(len(self.meshes_stats))

        return WidgetHistogram("Number of Faces", True, list_cells, int(no_bins), min_no_faces, max_no_faces)

    def create_histogram_vertices(self):
        # Analyzing the range of data
        list_cells = []
        min_no_vertices = self.meshes_stats[0].no_vertices
        max_no_vertices= self.meshes_stats[0].no_vertices
        for mesh_stat in self.meshes_stats:
            if min_no_vertices > mesh_stat.no_vertices:
                min_no_vertices = mesh_stat.no_vertices
            if max_no_vertices < mesh_stat.no_vertices:
                max_no_vertices = mesh_stat.no_vertices
            list_cells.append(mesh_stat.no_vertices)
        range_no_vertices = max_no_vertices - min_no_vertices

        # Divide the range into equally-divided bins
        # The numbers of bins for this can be found with
        # bins = sqrt(len(list))
        # TODO: Search for some proper proof of this to add to the report. I just did ChatGPT
        no_bins = math.sqrt(len(self.meshes_stats))

        return WidgetHistogram("Number of Vertices", True, list_cells, int(no_bins), min_no_vertices, max_no_vertices)

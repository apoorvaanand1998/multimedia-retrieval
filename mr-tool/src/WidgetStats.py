import math
import os

from PyQt5.QtCore import Qt

from constants import DB_RELATIVE_PATH
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea
from WidgetHistogram import WidgetHistogram
from WidgetBarChart import WidgetBarChart
from Widget3DViewer import Widget3DViewer
from Mesh import Mesh, MeshStats
import utils


class WidgetStats(QWidget):
    _ui_layout_main: QVBoxLayout = None

    _ui_label_title: QLabel = None

    db_map: dict[str, list[str]] = None
    db_count: int = None
    db_name: str = None
    db_stats: list[MeshStats] = None

    db_avg_vertices: int = None
    db_outliers_vertices: int = None
    db_avg_faces: int = None
    db_outliers_faces: int = None

    def __init__(self, db_map: dict[str, list[str]], db_count: int, db_name: str, db_stats: list[MeshStats]):
        super().__init__()

        self.db_map = db_map
        self.db_count = db_count
        self.db_name = db_name
        self.db_stats = db_stats

        # Compute statistics
        (self.db_avg_vertices, self.db_outliers_vertices,
         self.db_avg_faces, self.db_outliers_faces) = self.create_statistics()

        # UI
        self.meshes_stats: list[MeshStats] = utils.get_output_stats(self.db_name)

        self._ui_layout_main = QVBoxLayout()

        self._ui_label_title = QLabel(self.db_name)

        self._ui_layout_main.addWidget(self._ui_label_title)

        w_avg_shape_vertices, w_avg_shape_faces = self.create_3d_views(self.db_avg_vertices, self.db_avg_faces)

        # Top Row
        layout_row_1 = QVBoxLayout()

        layout_row_1.addWidget(self.create_barchart_classes())
        layout_row_1.addLayout(self.create_db_metadata())

        self._ui_layout_main.addLayout(layout_row_1)

        # Middle Row
        layout_row_2 = QVBoxLayout()

        layout_row_2.addWidget(self.create_histogram_vertices())
        layout_row_2.addWidget(w_avg_shape_vertices)

        self._ui_layout_main.addLayout(layout_row_2)

        # Bottom Row
        layout_row_3 = QVBoxLayout()

        layout_row_3.addWidget(self.create_histogram_faces())
        layout_row_3.addWidget(w_avg_shape_faces)

        self._ui_layout_main.addLayout(layout_row_3)

        self.setLayout(self._ui_layout_main)


    def create_3d_views(self, avg_vertices: int, avg_faces: int):
        # 3D Widget for average shape
        avg_shape_vertices_stats = self.db_stats[0]
        avg_shape_faces_stats = self.db_stats[0]
        for stats in self.db_stats:
            distance_vertices_current_shape = math.fabs(stats.no_vertices - avg_vertices)
            distance_vertices_avg_shape = math.fabs(avg_shape_vertices_stats.no_vertices - avg_vertices)
            if distance_vertices_current_shape < distance_vertices_avg_shape:
                avg_shape_vertices_stats = stats

            distance_faces_current_shape = math.fabs(stats.no_vertices - avg_faces)
            distance_faces_avg_shape = math.fabs(avg_shape_vertices_stats.no_cells - avg_faces)
            if distance_faces_current_shape < distance_faces_avg_shape:
                avg_shape_faces_stats = stats

        # 3D Widget for AVG Shape by Vertices
        mesh_file_path = str(os.path.join(DB_RELATIVE_PATH, self.db_name, avg_shape_vertices_stats._class,
                                          avg_shape_vertices_stats.name))
        mesh: Mesh = Mesh(mesh_file_path)
        w_avg_shape_vertices = Widget3DViewer(mesh)

        # 3D Widget for AVG Shape by Faces
        mesh_file_path = str(os.path.join(DB_RELATIVE_PATH, self.db_name, avg_shape_faces_stats._class,
                                          avg_shape_faces_stats.name))
        mesh: Mesh = Mesh(mesh_file_path)
        w_avg_shape_faces = Widget3DViewer(mesh)

        # 3D Widget for outliers

        return w_avg_shape_vertices, w_avg_shape_faces

    def create_statistics(self):
        total_vertices = 0
        total_faces = 0
        list_vertices = []
        list_faces = []
        for stat in self.db_stats:
            total_vertices += stat.no_vertices
            total_faces += stat.no_cells
            list_vertices.append(stat.no_vertices)
            list_faces.append(stat.no_cells)

        avg_vertices = int(total_vertices / len(self.db_stats))
        avg_faces = int(total_faces / len(self.db_stats))

        outliers_vertices = utils.find_outliers(list_vertices)
        outliers_faces = utils.find_outliers(list_faces)

        return avg_vertices, outliers_vertices, avg_faces, outliers_faces

    def create_db_metadata(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Database Name: " + self.db_name))
        layout.addWidget(QLabel("Database Size(Classes): " + str(len(list(self.db_map.keys())))))
        layout.addWidget(QLabel("Database Size(Objects): " + str(self.db_count)))
        layout.addWidget(QLabel("Database Average Shape Vertices: " + str(self.db_avg_vertices)))
        layout.addWidget(QLabel("Database Average Shape Faces: " + str(self.db_avg_faces)))

        return layout

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
        max_no_vertices = self.meshes_stats[0].no_vertices
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

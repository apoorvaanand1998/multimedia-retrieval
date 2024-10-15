import os
import utils
import constants

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QTableWidget, QHeaderView, QTableWidgetItem, \
    QPushButton
from Mesh import Mesh, MeshDescriptors


class WidgetDescriptors(QWidget):

    def __init__(self, db_map, db_name):
        super().__init__()
        self._db_map = db_map
        self._db_name = db_name

        self._mesh_descriptors = self.get_descriptors()

        self._ui_layout_main = QVBoxLayout()

        self._ui_w_descriptors = self.setup()
        self._ui_layout_main.addWidget(self._ui_w_descriptors)

        self.setLayout(self._ui_layout_main)

    def setup(self, mesh: Mesh = None):
        widget = QWidget()
        if mesh is not None:
            filtered: [MeshDescriptors] = [d for d in self._mesh_descriptors
                                           if d.name == mesh.name and d.get_class() == mesh.get_class()]
            descriptors: MeshDescriptors = filtered[0] if len(filtered) > 0 else MeshDescriptors(None, None, None, None,
                                                                                                 None, None, None, None)

            layout = QVBoxLayout()

            table = QTableWidget()
            table_headers = utils.DESCRIPTORS_FILE_HEADERS.split(",")[3:]  # skip path, name, class
            table.setColumnCount(len(table_headers))
            table.setRowCount(1)
            table.setHorizontalHeaderLabels(table_headers)

            # surface area
            if descriptors.surface_area is not None:
                table.setItem(0, 0, QTableWidgetItem(descriptors.surface_area))
            else:
                button = QPushButton("Calculate")
                button.clicked.connect(self.calculate_surface_area)
                table.setCellWidget(0, 0, button)

            # compactness (with respect to a sphere)
            if descriptors.compactness is not None:
                table.setItem(0, 1, QTableWidgetItem(descriptors.compactness))
            else:
                button = QPushButton("Calculate")
                button.clicked.connect(self.calculate_compactness)
                table.setCellWidget(0, 1, button)

            # 3D rectangularity (shape volume divided by OBB volume)
            if descriptors.rectangularity is not None:
                table.setItem(0, 2, QTableWidgetItem(descriptors.rectangularity))
            else:
                button = QPushButton("Calculate")
                button.clicked.connect(self.calculate_rectangularity)
                table.setCellWidget(0, 2, button)

            # diameter
            if descriptors.diameter is not None:
                table.setItem(0, 3, QTableWidgetItem(descriptors.diameter))
            else:
                button = QPushButton("Calculate")
                button.clicked.connect(self.calculate_diameter)
                table.setCellWidget(0, 3, button)

            # convexity (shape volume divided by convex hull volume)
            if descriptors.convexity is not None:
                table.setItem(0, 4, QTableWidgetItem(descriptors.convexity))
            else:
                button = QPushButton("Calculate")
                button.clicked.connect(self.calculate_convexity)
                table.setCellWidget(0, 4, button)

            # eccentricity (ratio of largest to smallest eigenvalues of covariance matrix)
            if descriptors.eccentricity is not None:
                table.setItem(0, 5, QTableWidgetItem(descriptors.eccentricity))
            else:
                button = QPushButton("Calculate")
                button.clicked.connect(self.calculate_eccentricity)
                table.setCellWidget(0, 5, button)

            # Table will fit the screen horizontally
            table.horizontalHeader().setStretchLastSection(True)
            table.horizontalHeader().setSectionResizeMode(
                QHeaderView.Stretch)

            layout.addWidget(table)
            widget.setLayout(layout)

        return widget

    def calculate_surface_area(self):
        print('c')

    def calculate_compactness(self):
        print('c')

    def calculate_rectangularity(self):
        print('c')

    def calculate_diameter(self):
        print('c')

    def calculate_convexity(self):
        print('c')

    def calculate_eccentricity(self):
        print('c')

    def get_descriptors(self):
        return utils.get_output_descriptors(self._db_name)

    # Used by IWndowDBSelector
    def selected_object_changed(self, mesh: Mesh):
        self._ui_layout_main.removeWidget(self._ui_w_descriptors)
        self._ui_w_descriptors = self.setup(mesh)
        self._ui_layout_main.addWidget(self._ui_w_descriptors)

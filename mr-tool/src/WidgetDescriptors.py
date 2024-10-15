from PyQt5.QtCore import Qt

import utils
import global_descriptors

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QTableWidget, QHeaderView, QTableWidgetItem, \
    QPushButton
from Mesh import Mesh, MeshDescriptors


class WidgetDescriptors(QWidget):

    def __init__(self, db_map, db_name):
        super().__init__()
        self._db_map = db_map
        self._db_name = db_name

        self._mesh = None
        self._mesh_descriptors = None
        self.get_descriptors()

        self._ui_layout_main = QVBoxLayout()

        self._ui_w_descriptors = self.setup()
        self._ui_layout_main.addWidget(self._ui_w_descriptors)

        self.setLayout(self._ui_layout_main)

    def setup(self):
        widget = QWidget()
        if self._mesh is not None:
            layout = QVBoxLayout()

            table = QTableWidget()
            table_headers = utils.DESCRIPTORS_FILE_HEADERS.split(",")[3:]  # skip path, name, class
            table.setColumnCount(len(table_headers))
            table.setRowCount(1)
            table.setHorizontalHeaderLabels(table_headers)

            # surface area
            if self._mesh_descriptors.surface_area is not None:
                item = QTableWidgetItem(str(self._mesh_descriptors.surface_area))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                table.setItem(0, 0, item)
            else:
                button = QPushButton("Calculate")
                button.clicked.connect(self.calculate_surface_area)
                table.setCellWidget(0, 0, button)

            # compactness (with respect to a sphere)
            if self._mesh_descriptors.compactness is not None:
                item = QTableWidgetItem(str(self._mesh_descriptors.compactness))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                table.setItem(0, 1, item)
            else:
                button = QPushButton("Calculate")
                button.clicked.connect(self.calculate_compactness)
                table.setCellWidget(0, 1, button)

            # 3D rectangularity (shape volume divided by OBB volume)
            if self._mesh_descriptors.rectangularity is not None:
                item = QTableWidgetItem(str(self._mesh_descriptors.rectangularity))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                table.setItem(0, 2, item)
            else:
                button = QPushButton("Calculate")
                button.clicked.connect(self.calculate_rectangularity)
                table.setCellWidget(0, 2, button)

            # diameter
            if self._mesh_descriptors.diameter is not None:
                item = QTableWidgetItem(str(self._mesh_descriptors.diameter))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                table.setItem(0, 3, item)
            else:
                button = QPushButton("Calculate")
                button.clicked.connect(self.calculate_diameter)
                table.setCellWidget(0, 3, button)

            # convexity (shape volume divided by convex hull volume)
            if self._mesh_descriptors.convexity is not None:
                item = QTableWidgetItem(str(self._mesh_descriptors.convexity))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                table.setItem(0, 4, item)
            else:
                button = QPushButton("Calculate")
                button.clicked.connect(self.calculate_convexity)
                table.setCellWidget(0, 4, button)

            # eccentricity (ratio of largest to smallest eigenvalues of covariance matrix)
            if self._mesh_descriptors.eccentricity is not None:
                item = QTableWidgetItem(str(self._mesh_descriptors.eccentricity))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                table.setItem(0, 5, item)
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
        self._mesh_descriptors.set_surface_area(global_descriptors.calculate_surface_area(self._mesh))
        utils.save_output_descriptors_one(self._db_name, self._mesh_descriptors)
        self.reload()

    def calculate_compactness(self):
        self._mesh_descriptors.set_compactness(global_descriptors.calculate_compactness(self._mesh))
        utils.save_output_descriptors_one(self._db_name, self._mesh_descriptors)
        self.reload()

    def calculate_rectangularity(self):
        self._mesh_descriptors.set_rectangularity(global_descriptors.calculate_rectangularity(self._mesh))
        utils.save_output_descriptors_one(self._db_name, self._mesh_descriptors)
        self.reload()

    def calculate_diameter(self):
        self._mesh_descriptors.set_diameter(global_descriptors.calculate_diameter(self._mesh))
        utils.save_output_descriptors_one(self._db_name, self._mesh_descriptors)
        self.reload()

    def calculate_convexity(self):
        self._mesh_descriptors.set_convexity(global_descriptors.calculate_convexity(self._mesh))
        utils.save_output_descriptors_one(self._db_name, self._mesh_descriptors)
        self.reload()

    def calculate_eccentricity(self):
        self._mesh_descriptors.set_eccentricity(global_descriptors.calculate_eccentricity(self._mesh))
        utils.save_output_descriptors_one(self._db_name, self._mesh_descriptors)
        self.reload()

    def get_descriptors(self):
        if self._mesh is None:
            self._mesh_descriptors = MeshDescriptors(None, None, None, None, None,
                                                     None, None, None, None)
            return

        all_descriptors: list[MeshDescriptors] = utils.get_output_descriptors(self._db_name)
        filtered: [MeshDescriptors] = [d for d in all_descriptors
                                       if d.name == self._mesh.name and d.get_class() == self._mesh.get_class()]
        self._mesh_descriptors = filtered[0] if len(filtered) > 0 else MeshDescriptors(self._mesh.path, self._mesh.name,
                                                                                       self._mesh.get_class(), None,
                                                                                       None,
                                                                                       None, None, None, None)

    def reload(self):
        self.get_descriptors()
        self._ui_layout_main.removeWidget(self._ui_w_descriptors)
        self._ui_w_descriptors = self.setup()
        self._ui_layout_main.addWidget(self._ui_w_descriptors)

    # Used by IWndowDBSelector
    def selected_object_changed(self, mesh: Mesh):
        self._mesh = mesh
        self.reload()

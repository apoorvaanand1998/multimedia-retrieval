import math
import os
import time

from PyQt5.QtCore import Qt

import utils
import global_descriptors
import constants

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QTableWidget, QHeaderView, QTableWidgetItem, \
    QPushButton, QListWidget, QProgressBar, QApplication
from Mesh import Mesh, MeshDescriptors


class WidgetDescriptors(QWidget):

    def __init__(self, db_map, db_name, db_count):
        super().__init__()
        self._db_map = db_map
        self._db_name = db_name
        self._db_count = db_count

        self._mesh = None
        self._mesh_descriptors = None
        self.get_descriptors()

        self._ui_layout_main = QVBoxLayout()

        self._ui_w_descriptors = self.setup()
        self._ui_layout_main.addWidget(self._ui_w_descriptors)

        self._ui_w_all = self.setup_all()
        self._ui_layout_main.addWidget(self._ui_w_all)

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

    def setup_all(self):
        widget = QWidget()

        layout = QVBoxLayout(widget)

        button = QPushButton("Calculate descriptors for all items in the database")
        button.clicked.connect(self.calculate_for_all_objects)
        layout.addWidget(button)

        self._ui_progress_label = QLabel("")
        layout.addWidget(self._ui_progress_label)

        self._ui_progress_bar = QProgressBar()
        self._ui_progress_bar.setRange(0, self._db_count)
        layout.addWidget(self._ui_progress_bar)

        self._ui_log_box = QListWidget()
        self._ui_log_box.setMinimumHeight(750)
        layout.addWidget(self._ui_log_box)

        widget.setLayout(layout)
        return widget

    def calculate_for_all_objects(self):
        count = 0
        all_meshes_descriptors: list[MeshDescriptors] = []
        total_time = 0
        for key in self._db_map:
            for mesh_name in self._db_map[key]:
                start_time = time.time()
                path = str(os.path.join(constants.DB_RELATIVE_PATH, self._db_name, key, mesh_name))
                self._ui_progress_label.setText(str(count + 1) + "/" + str(
                    self._db_count) + " | " + path + " | Total time: " + utils.get_time_from_seconds(total_time))

                mesh = Mesh(path)
                mesh_descriptors = MeshDescriptors(path, mesh.name, mesh.get_class(), None, None, None, None, None,
                                                   None)

                self._ui_log_box.addItem("\nCalculating descriptors for " + path)

                # Surfacea Area #
                try:
                    sa = global_descriptors.calculate_surface_area(mesh)
                    mesh_descriptors.set_surface_area(sa)
                    self._ui_log_box.addItem("\t* Surface Area: " + str(sa))
                except Exception as e:
                    self._ui_log_box.addItem("\t* Surface Area Error: " + str(e))

                # Compactness #
                try:
                    co = global_descriptors.calculate_compactness(mesh)
                    mesh_descriptors.set_compactness(co)
                    self._ui_log_box.addItem("\t* Compactness: " + str(co))
                except Exception as e:
                    self._ui_log_box.addItem("\t* Compactness Error: " + str(e))

                # Rectangularity #
                try:
                    re = global_descriptors.calculate_rectangularity(mesh)
                    mesh_descriptors.set_rectangularity(re)
                    self._ui_log_box.addItem("\t* 3D Rectangularity: " + str(re))
                except Exception as e:
                    self._ui_log_box.addItem("\t* 3D Rectangularity Error: " + str(e))

                # Diameter #
                try:
                    di = global_descriptors.calculate_diameter(mesh)
                    mesh_descriptors.set_diameter(di)
                    self._ui_log_box.addItem("\t* Diameter: " + str(di))
                except Exception as e:
                    self._ui_log_box.addItem("\t* Diameter Error: " + str(e))

                # Convexity #
                try:
                    conv = global_descriptors.calculate_convexity(mesh)
                    mesh_descriptors.set_convexity(conv)
                    self._ui_log_box.addItem("\t* Convexity: " + str(conv))
                except Exception as e:
                    self._ui_log_box.addItem("\t* Convexity Error: " + str(e))

                # Eccentricity #
                try:
                    ec = global_descriptors.calculate_eccentricity(mesh)
                    mesh_descriptors.set_eccentricity(ec)
                    self._ui_log_box.addItem("\t* Eccentricity: " + str(ec))
                except Exception as e:
                    self._ui_log_box.addItem("\t* Eccentricity Error: " + str(e))

                end_time = time.time()

                self._ui_log_box.addItem(
                    "\t Finished computing mesh descriptors for " + mesh.get_class() + "/" + mesh.name + " | Time it took: " + str(
                        round((end_time - start_time), 2)) + " s")
                total_time += end_time - start_time

                all_meshes_descriptors.append(mesh_descriptors)
                count += 1

                self._ui_progress_bar.setValue(count)
                self._ui_log_box.scrollToBottom()
                QApplication.processEvents()

        output_file = utils.save_output_descriptors(self._db_name, all_meshes_descriptors)

        self._ui_log_box.addItem("Finished calculating descriptors for all objects.")
        self._ui_log_box.addItem("Total time: " + str(total_time))

        self._ui_log_box.addItem("Output file: " + output_file)

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

        # Pointless to remove this as well and also may prove buggy but
        # for now it's fine
        self._ui_layout_main.removeWidget(self._ui_w_all)
        self._ui_w_all = self.setup_all()
        self._ui_layout_main.addWidget(self._ui_w_all)

    # Used by IWndowDBSelector
    def selected_object_changed(self, mesh: Mesh):
        self._mesh = mesh
        self.reload()

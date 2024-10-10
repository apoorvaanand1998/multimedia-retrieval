import os
import time

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QListWidget, QWidget, QLabel, QPushButton, QLineEdit, \
    QProgressBar, QApplication, QCheckBox, QScrollArea, QSizePolicy
from PyQt5.uic.properties import QtWidgets

from Widget3DViewer import Widget3DViewer
from Mesh import Mesh
from NormalizationWizard import NormalizationWizard
from StepResample import StepResample
from StepTranslate import StepTranslate
from StepScale import StepScale
from constants import DB_ORIGINAL_RELATIVE_PATH, DB_PREPROCESSED_NAME, DB_ORIGINAL_NAME, DB_RELATIVE_PATH
from utils import save_to_db, get_database_map, save_array_to_txt
from QHSeparationLine import QHSeparationLine


class WindowNormalization(QMainWindow):
    _db_name: str = DB_ORIGINAL_NAME
    _db_path: str = DB_ORIGINAL_RELATIVE_PATH
    _output_single_db_name: str = DB_PREPROCESSED_NAME

    _input_all_db_name: str = DB_ORIGINAL_NAME

    _output_all_db_name: str = DB_PREPROCESSED_NAME
    _output_all_target_no_vertices: int = 5000
    _output_all_epsilon_no_vertices: int = 500

    _normalization_flag_resample: bool = False
    _normalization_flag_translation: bool = True
    _normalization_flag_scale: bool = True

    # If after a decimation/subdivison,
    # the number of vertices doesn't change by at least this amount
    # we skip it
    _output_all_minimum_change: int = 50

    _wizard: NormalizationWizard = None

    _ui_layout_main: QVBoxLayout = None
    _ui_layout_db_all: QHBoxLayout = None

    _ui_layout_db_selection: QVBoxLayout = None
    _ui_class_list: QListWidget = None
    _ui_object_list: QListWidget = None

    _ui_3d_viewer: Widget3DViewer = None

    _ui_normalization: QWidget = None

    _ui_progress_bar: QProgressBar = None
    _ui_log_box: QListWidget = None

    def __init__(self):
        super(WindowNormalization, self).__init__()

        self._wizard = NormalizationWizard(
            mesh=None,
            window=self
        )

        self._ui_layout_main = QVBoxLayout()

        self.central_widget = QWidget()
        self.central_widget.setLayout(self._ui_layout_main)
        self.central_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.setCentralWidget(self.central_widget)

        self._ui_layout_db_all = QHBoxLayout()

        # Class - Item selection List
        self._ui_class_list, self._ui_object_list = self.ui_create_db_lists()
        self.ui_create_db_events()

        layout_database = QVBoxLayout()
        layout_database.addWidget(self._ui_class_list)
        layout_database.addWidget(self._ui_object_list)

        # 3D Viewer
        self._ui_3d_viewer = Widget3DViewer(with_options=False)
        self._ui_3d_viewer._flag_shaded_wireframe = True
        self._ui_3d_viewer._flag_bbox = True

        self._ui_layout_db_all.addLayout(layout_database)
        self._ui_layout_db_all.addWidget(self._ui_3d_viewer)

        # Normalization Steps
        self._ui_normalization = self._wizard.ui_widget
        self._ui_layout_db_all.addWidget(self._ui_normalization)

        self._ui_layout_main.addLayout(self._ui_layout_db_all)

        # Normalization Output
        layout_normalization_single = QHBoxLayout()

        line_edit = QLineEdit(self._output_single_db_name)
        line_edit.textChanged.connect(lambda text: self.output_single_db_name(text))
        layout_normalization_single.addWidget(line_edit)

        btn_single = QPushButton("Save current mesh")
        btn_single.pressed.connect(lambda: save_to_db(self._wizard.get_current_mesh(), line_edit.text()))
        layout_normalization_single.addWidget(btn_single)

        self._ui_layout_main.addLayout(layout_normalization_single)

        # Normalize all shapes
        divider_line = QHSeparationLine()
        self._ui_layout_main.addWidget(divider_line)

        layout_normalization_all = QVBoxLayout()

        layout_normalization_all_controls = QHBoxLayout()

        layout_normalization_all_inputs = QVBoxLayout()

        l = QHBoxLayout()
        l.addWidget(QLabel("Input Database: "))
        line_edit = QLineEdit(self._input_all_db_name)
        line_edit.textChanged.connect(self.set_input_db)
        l.addWidget(line_edit)
        layout_normalization_all_inputs.addLayout(l)

        l = QHBoxLayout()
        l.addWidget(QLabel("Output Database: "))
        line_edit = QLineEdit(self._output_all_db_name)
        line_edit.textChanged.connect(self.set_output_db)
        l.addWidget(line_edit)
        layout_normalization_all_inputs.addLayout(l)

        l = QHBoxLayout()
        l.addWidget(QLabel("Target Average for Resample: "))
        line_edit_no_vertices_target = QLineEdit(str(self._output_all_target_no_vertices))
        line_edit_no_vertices_target.textChanged.connect(self.set_target_no_vertices)
        l.addWidget(line_edit_no_vertices_target)
        layout_normalization_all_inputs.addLayout(l)

        layout_normalization_all_controls.addLayout(layout_normalization_all_inputs)

        layout_normalization_checkboxes = QVBoxLayout()

        cb = QCheckBox("Resample")
        cb.setChecked(self._normalization_flag_resample)
        cb.stateChanged.connect(self.check_resample)
        layout_normalization_checkboxes.addWidget(cb)

        cb = QCheckBox("Translation")
        cb.setChecked(self._normalization_flag_translation)
        cb.stateChanged.connect(self.check_translation)
        layout_normalization_checkboxes.addWidget(cb)

        cb = QCheckBox("Scale")
        cb.setChecked(self._normalization_flag_scale)
        cb.stateChanged.connect(self.check_scale)
        layout_normalization_checkboxes.addWidget(cb)

        layout_normalization_all_controls.addLayout(layout_normalization_checkboxes)

        btn_all = QPushButton("Process all shapes")
        btn_all.pressed.connect(self.process_all_shapes)
        layout_normalization_all_controls.addWidget(btn_all)

        layout_normalization_all.addLayout(layout_normalization_all_controls)

        self._ui_layout_main.addLayout(layout_normalization_all)

        layout_progress = QVBoxLayout()

        self._ui_progress_label = QLabel("")
        layout_progress.addWidget(self._ui_progress_label)

        self._ui_progress_bar = QProgressBar()
        self._ui_progress_bar.setRange(0, 100)
        layout_progress.addWidget(self._ui_progress_bar)

        self._ui_log_box = QListWidget()
        self._ui_log_box.setMinimumHeight(750)
        layout_progress.addWidget(self._ui_log_box)

        self._ui_layout_main.addLayout(layout_progress)

        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.central_widget)
        self.setCentralWidget(scroll)



    def check_resample(self, s):
        self._normalization_flag_resample = s == Qt.Checked

    def check_translation(self, s):
        self._normalization_flag_translation = s == Qt.Checked

    def check_scale(self, s):
        self._normalization_flag_scale = s == Qt.Checked

    def set_input_db(self, text):
        self._input_all_db_name = text

    def set_output_db(self, text):
        self._output_all_db_name = text

    def process_all_shapes(self):
        try:
            input_db_path = os.path.join(DB_RELATIVE_PATH, self._input_all_db_name)
            if not os.path.exists(input_db_path):
                print("ERROR: INPUT DB " + input_db_path + " does not exist")
                return

            db_map, db_total_count = get_database_map(self._db_path)
            self._ui_progress_bar.setRange(0, db_total_count)

            step_resample = StepResample()
            step_resample._decimate_desired_vertices = self._output_all_target_no_vertices
            step_resample._subdivide_iterations = 1

            step_translation = StepTranslate()
            step_translation_stats_before = []  # Barycenters before
            step_translation_stats_after = []  # Barycenters after

            step_scale = StepScale()
            step_scale_stats_before = []  # Volume before
            step_scale_stats_after = []  # Volume after

            start_time = time.time()

            obj_count = 0
            broke_objs_names = []
            for obj_class, obj_list in db_map.items():
                for obj in obj_list:
                    self._ui_log_box.addItem(
                        str(obj_count + 1) + "/" + str(db_total_count) +
                        " | Normalizing " + obj_class + " -> " + obj)
                    obj_count += 1

                    stop_time = time.time()
                    self._ui_progress_label.setText(
                        "From " + self._input_all_db_name + " to " + self._output_all_db_name + "\n" +
                        str(obj_count + 1) + "/" + str(db_total_count) +
                        " | Normalizing " + obj_class + " -> " + obj + " | " +
                        str(stop_time - start_time) + "s"
                    )

                    mesh = Mesh(str(os.path.join(self._db_path, obj_class, obj)))

                    # Resample
                    if self._normalization_flag_resample:
                        self._ui_log_box.addItem("\tResample. Current vertices: " + str(mesh.get_vertices()))

                        min = self._output_all_target_no_vertices - self._output_all_epsilon_no_vertices
                        max = self._output_all_target_no_vertices + self._output_all_epsilon_no_vertices
                        while mesh.get_vertices() < min or mesh.get_vertices() > max:
                            vertices_before = mesh.get_vertices()
                            print(mesh._class + " - " + mesh.name + " - " + str(mesh.get_vertices()))

                            v = mesh.get_vertices()
                            if mesh.get_vertices() < min:
                                self._ui_log_box.addItem("\tSubdividing from " + str(mesh.get_vertices()))
                                step_resample.set_mode(0)  # Subdivide
                            elif mesh.get_vertices() > max:
                                self._ui_log_box.addItem("\tDecimating from " + str(mesh.get_vertices()))
                                step_resample.set_mode(2)  # Decimate with desired vertices
                            QApplication.processEvents()
                            mesh = step_resample.apply(mesh)

                            # Subdivide breaking the object bug
                            if mesh.get_vertices() == 0:
                                self._ui_log_box.addItem(
                                    "\tObject broke from subdivision. Skipping at " + str(mesh.get_vertices()))
                                QApplication.processEvents()
                                broke_objs_names.append(
                                    mesh._class + " -> " + mesh.name + ". Reason: 0 vertices due to subdivide")
                                break

                            # Decimate doesn t work anymore
                            if vertices_before - mesh.get_vertices() < self._output_all_minimum_change:
                                self._ui_log_box.addItem("\tDecimate didn't meet the required " + str(
                                    self._output_all_minimum_change) + " vertices delta. Skipping at " + str(
                                    mesh.get_vertices()))
                                QApplication.processEvents()
                                broke_objs_names.append(
                                    mesh._class + " -> " + mesh.name +
                                    ". Reason: Didn't meet the required " + str(
                                        self._output_all_minimum_change) + " vertices delta")
                                break
                        self._ui_log_box.addItem("\tResample complete. Final vertices: " + str(mesh.get_vertices()))

                    # Translation
                    if self._normalization_flag_translation:
                        self._ui_log_box.addItem("\n\tTranslation. Current barycenter: " + str(mesh.get_barycenter()))

                        step_translation_stats_before.append(mesh.get_barycenter())
                        mesh = step_translation.apply(mesh)
                        step_translation_stats_after.append(mesh.get_barycenter())

                        self._ui_log_box.addItem(
                            "\tTranslation complete. Final barycenter: " + str(mesh.get_vertices()))

                    # Scale
                    if self._normalization_flag_scale:
                        self._ui_log_box.addItem("\n\tScale. " +
                                                 "Current AABB dimensions: " + str(mesh.get_bounding_box_dimensions()) +
                                                 "Current Volume: " + str(mesh.get_volume()))
                        step_scale_stats_before.append(mesh.get_volume())
                        mesh = step_scale.apply(mesh)
                        step_scale_stats_after.append(mesh.get_volume())

                        self._ui_log_box.addItem("\tScale complete. " +
                                                 "Final AABB dimensions: " + str(mesh.get_bounding_box_dimensions()) +
                                                 "Final Volume: " + str(mesh.get_volume()))

                    final_path = save_to_db(mesh, self._output_all_db_name)
                    self._ui_log_box.addItem("\tFinal object saved at: " + final_path)
                    self._ui_log_box.scrollToBottom()

                    self._ui_progress_bar.setValue(obj_count)

                    QApplication.processEvents()

            self._ui_log_box.addItem("Broken objs: " + str(len(broke_objs_names)))
            self._ui_log_box.addItem(
                "Minimum change required (if not met,obj is skipped): " + str(self._output_all_minimum_change))
            self._ui_log_box.scrollToBottom()
            QApplication.processEvents()

            save_array_to_txt(self._db_name + "_broken_normalization.txt", broke_objs_names)

        except Exception as e:
            print("Error: ")
            print(e)

    def set_target_no_vertices(self, n):
        self._output_all_target_no_vertices = n

    def set_epsilon_no_vertices(self, n):
        self._output_all_epsilon_no_vertices = n

    def update_3d_viewer(self):
        self._ui_3d_viewer.set_mesh(self._wizard.get_current_mesh())
        self._ui_3d_viewer.show_mesh()

        self._ui_layout_db_all.removeWidget(self._ui_normalization)
        self._ui_normalization = self._wizard.ui_widget
        self._ui_layout_db_all.addWidget(self._ui_normalization)

    def ui_object_changed(self, list_item):
        # If class has changed and there was
        # a selected item, then there's no selected item
        # now just display a text
        if list_item is None:
            self._ui_3d_viewer.show_none()
            return

        self._selected_object = list_item.text()

        mesh = Mesh(os.path.join(self._db_path, self._selected_class, self._selected_object))
        self._ui_3d_viewer.set_mesh(mesh)
        self._ui_3d_viewer.show_mesh()

        self._wizard.reset(mesh)

        self._ui_layout_db_all.removeWidget(self._ui_normalization)
        self._ui_normalization = self._wizard.ui_widget
        self._ui_layout_db_all.addWidget(self._ui_normalization)

    def ui_class_changed(self, list_item):
        self._selected_class = list_item.text()

        files = os.listdir(os.path.join(self._db_path, self._selected_class))
        self._ui_object_list.clear()
        self._ui_object_list.addItems(files)

        self._wizard.reset()
        self._ui_layout_db_all.removeWidget(self._ui_normalization)

    def ui_create_db_lists(self):
        # List of all classes
        folders = os.listdir(self._db_path)
        ui_class_list = QListWidget()

        for folder in folders:
            if os.path.isdir(os.path.join(self._db_path, folder)):
                ui_class_list.addItem(folder)

        first_class = ui_class_list.item(0)
        ui_class_list.setCurrentItem(first_class)

        self._selected_class = first_class.text()

        # List for displaying active class
        files = os.listdir(os.path.join(self._db_path, first_class.text()))
        ui_items_list = QListWidget()
        ui_items_list.addItems(files)

        return ui_class_list, ui_items_list

    def ui_create_db_events(self):
        # Set on click events for class elements
        self._ui_class_list.currentItemChanged.connect(self.ui_class_changed)

        # Set on click events for object elements
        self._ui_object_list.currentItemChanged.connect(self.ui_object_changed)

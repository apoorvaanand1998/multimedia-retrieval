import os

from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QListWidget, QWidget, QLabel, QPushButton
from Widget3DViewer import Widget3DViewer
from Mesh import Mesh
from NormalizationWizard import NormalizationWizard
from StepResample import StepResample
from constants import DB_ORIGINAL_RELATIVE_PATH


class WindowNormalization(QMainWindow):
    _db_path: str = DB_ORIGINAL_RELATIVE_PATH
    _wizard: NormalizationWizard = None

    _ui_layout_main: QVBoxLayout = None
    _ui_layout_db_all: QHBoxLayout = None

    _ui_layout_db_selection: QVBoxLayout = None
    _ui_class_list: QListWidget = None
    _ui_object_list: QListWidget = None

    _ui_3d_viewer: Widget3DViewer = None

    _ui_normalization: QWidget = None

    def __init__(self):
        super(WindowNormalization, self).__init__()

        self._wizard = NormalizationWizard(
            mesh=None,
            steps=[StepResample()],
            window=self
        )

        self._ui_layout_main = QVBoxLayout()

        self.central_widget = QWidget(self)
        self.central_widget.setLayout(self._ui_layout_main)
        self.setCentralWidget(self.central_widget)

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

        self._ui_layout_db_all.addLayout(layout_database)
        self._ui_layout_db_all.addWidget(self._ui_3d_viewer)

        # Normalization Steps
        self._ui_normalization = self._wizard.ui_widget
        self._ui_layout_db_all.addWidget(self._ui_normalization)

        self._ui_layout_main.addLayout(self._ui_layout_db_all)

    def update_3d_viewer(self):
        self._ui_3d_viewer.set_mesh(self._wizard.get_current_mesh())
        self._ui_3d_viewer.show_mesh()

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

import os

from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QListWidget, QWidget
from Widget3DViewer import Widget3DViewer
from Mesh import Mesh
from constants import DB_ORIGINAL_RELATIVE_PATH


class WindowNormalization(QMainWindow):
    _db_path: str = DB_ORIGINAL_RELATIVE_PATH

    _ui_layout_main: QVBoxLayout = None

    _ui_layout_db_selection: QVBoxLayout = None
    _ui_class_list: QListWidget = None
    _ui_object_list: QListWidget = None

    _ui_3d_viewer: Widget3DViewer = None

    def __init__(self):
        super(WindowNormalization, self).__init__()

        self._ui_layout_main = QVBoxLayout()

        self.central_widget = QWidget(self)
        self.central_widget.setLayout(self._ui_layout_main)
        self.setCentralWidget(self.central_widget)

        layout_db_all = QHBoxLayout()

        # Class - Item selection List
        self._ui_class_list, self._ui_object_list = self.ui_create_db_lists()
        self.ui_create_db_events()

        layout_database = QVBoxLayout()
        layout_database.addWidget(self._ui_class_list)
        layout_database.addWidget(self._ui_object_list)

        # 3D Viewer
        self._ui_3d_viewer = Widget3DViewer(with_options=False)

        layout_db_all.addLayout(layout_database)
        layout_db_all.addWidget(self._ui_3d_viewer)

        self._ui_layout_main.addLayout(layout_db_all)

        # 3D Viewers for normalisation steps
        layout_normalisation = QHBoxLayout()

        # test_mesh = Mesh(os.path.join(DB_ORIGINAL_RELATIVE_PATH, "AircraftBuoyant", "m1337.obj"))
        layout_normalisation.addWidget(Widget3DViewer(with_options=False))
        layout_normalisation.addWidget(Widget3DViewer(with_options=False))
        layout_normalisation.addWidget(Widget3DViewer(with_options=False))
        layout_normalisation.addWidget(Widget3DViewer(with_options=False))
        layout_normalisation.addWidget(Widget3DViewer(with_options=False))

        layout_normalisation.setContentsMargins(0, 0, 0, 0)

        self._ui_layout_main.addLayout(layout_normalisation)

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

    def ui_class_changed(self, list_item):
        self._selected_class = list_item.text()

        files = os.listdir(os.path.join(self._db_path, self._selected_class))
        self._ui_object_list.clear()
        self._ui_object_list.addItems(files)

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

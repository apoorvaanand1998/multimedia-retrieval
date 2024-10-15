from PyQt5.QtCore import Qt

import constants
import os
import utils

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QComboBox, QScrollArea, QListWidget, QHBoxLayout, \
    QApplication
from WidgetNoDb import WidgetNoDb
from Mesh import Mesh
from Widget3DViewer import Widget3DViewer


class IWindowDBSelector(QMainWindow):

    def __init__(self, main_widget_class, with_db_browser=False):
        super(IWindowDBSelector, self).__init__()

        self._ui_layout_main = QVBoxLayout()
        self._scroll = QScrollArea()

        self.with_db_browser = with_db_browser

        self.main_widget = None
        self.main_widget_class = main_widget_class

        self.db_selector_setup(constants.DB_ORIGINAL_NAME)
        self.on_db_selector_changed(0)

    def db_selector_setup(self, db_name: str):
        self.central_widget = QWidget(self)
        self.central_widget.setLayout(self._ui_layout_main)
        self.setCentralWidget(self.central_widget)

        # DB Selector
        self._ui_db_selector = QComboBox()
        self._ui_db_selector.addItems(constants.DATABASES)
        self._ui_db_selector.setCurrentText(db_name)
        self._ui_db_selector.currentIndexChanged.connect(self.on_db_selector_changed)

        self._ui_layout_main.addWidget(self._ui_db_selector)

    def on_db_selector_changed(self, idx: int):
        db_name = constants.DATABASES[idx]

        self._db_path = str(os.path.join(constants.DB_RELATIVE_PATH, db_name))

        self._ui_layout_main.removeWidget(self._scroll)

        self._scroll = QScrollArea()
        self._scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        layout = QVBoxLayout()

        if os.path.exists(self._db_path):
            if self.with_db_browser:
                layout.addLayout(self.db_ui_setup())

            db_map, db_count = utils.get_database_map(self._db_path)
            self.main_widget = self.main_widget_class(db_map, db_name)
        else:
            self.main_widget = WidgetNoDb(db_name)

        layout.addWidget(self.main_widget)
        self._scroll.setLayout(layout)

        self._ui_layout_main.addWidget(self._scroll)

    def db_ui_setup(self):
        layout_db_all = QHBoxLayout()

        # Class - Item selection List
        self._ui_class_list, self._ui_object_list = self.ui_create_db_lists()
        self.ui_create_db_events()

        layout_database = QVBoxLayout()
        layout_database.addWidget(self._ui_class_list)
        layout_database.addWidget(self._ui_object_list)

        # 3D Viewer
        self._ui_3d_viewer = Widget3DViewer()

        layout_db_all.addLayout(layout_database)
        layout_db_all.addWidget(self._ui_3d_viewer)

        return layout_db_all

    def no_db_ui_setup(self, db_name: str):
        self.db_selector_setup(db_name)
        self._ui_layout_main.addWidget(WidgetNoDb(db_name))

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

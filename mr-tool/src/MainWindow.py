import os
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vedo import Plotter, load
from util import constants

class MainWindow(QMainWindow):
    _selected_class = ""  # relative path to the selected object in the database
    _selected_object = ""  # relative path to the selected object in the database

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle(constants.UI_MAIN_APP_TITLE)

        # Create a central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Main layout
        layout_main = QHBoxLayout()
        self.central_widget.setLayout(layout_main)

        # Database display widgets
        self.ui_class_list, self.ui_object_list = self.ui_create_db_lists()
        self.ui_create_db_events()

        layout_database = QVBoxLayout()
        layout_database.addWidget(self.ui_class_list)
        layout_database.addWidget(self.ui_object_list)

        layout_main.addLayout(layout_database)

        # Main visualization window using vedo
        self.ui_vedo_widget, self.ui_vedo_plotter = self.ui_create_vedo_widget()

        layout_vedo = QVBoxLayout()
        layout_vedo.addWidget(self.ui_vedo_widget)

        layout_main.addLayout(layout_vedo)

    def ui_object_changed(self, list_item):
        # Reset drawing
        self.ui_vedo_plotter.clear()

        # If class has changed and there was
        # a selected item, then there's no selected item
        # now just display a text
        if list_item is None:
            self.ui_vedo_plotter.show([], constants.UI_NO_ITEM_SELECTED_PLACEHOLDER, at=0)
            return

        self._selected_object = list_item.text()

        mesh = load(os.path.join(constants.DB_RELATIVE_PATH, self._selected_class, self._selected_object))
        self.ui_vedo_plotter.show(mesh)

    def ui_class_changed(self, list_item):
        self._selected_class = list_item.text()

        files = os.listdir(os.path.join(constants.DB_RELATIVE_PATH, self._selected_class))
        self.ui_object_list.clear()
        self.ui_object_list.addItems(files)


    def ui_create_vedo_widget(self):
        # Create the VTK render window interactor (QVTKRenderWindowInteractor)
        vtkWidget = QVTKRenderWindowInteractor()

        # Create a vedo Plotter and link it to the VTK widget
        plotter = Plotter(qt_widget=vtkWidget, interactive=False)

        plotter.show([], constants.UI_NO_ITEM_SELECTED_PLACEHOLDER, at=0)

        # Start the VTK interactor
        vtkWidget.GetRenderWindow().Render()
        plotter.interactor.Start()

        return vtkWidget, plotter

    def ui_create_db_lists(self):
        # List of all classes
        folders = os.listdir(constants.DB_RELATIVE_PATH)
        ui_class_list = QListWidget()
        ui_class_list.addItems(folders)

        first_class = ui_class_list.item(0)
        ui_class_list.setCurrentItem(first_class)

        self._selected_class = first_class.text()

        # List for displaying active class
        files = os.listdir(os.path.join(constants.DB_RELATIVE_PATH, first_class.text()))
        ui_items_list = QListWidget()
        ui_items_list.addItems(files)

        return ui_class_list, ui_items_list

    def ui_create_db_events(self):
        # Set on click events for class elements
        self.ui_class_list.currentItemChanged.connect(self.ui_class_changed)

        # Set on click events for object elements
        self.ui_object_list.currentItemChanged.connect(self.ui_object_changed)
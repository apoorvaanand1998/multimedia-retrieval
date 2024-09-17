import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QListWidget, QLabel, QCheckBox, \
    QTabWidget, QApplication
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vedo import Plotter, load
from WidgetNoDb import WidgetNoDb
import constants

from Mesh import Mesh


class WindowDatabase(QMainWindow):
    _selected_class = None  # relative path to the selected object in the database
    _selected_object = None  # relative path to the selected object in the database

    _active_mesh: Mesh = None
    _active_mesh_bbox: bool = False
    _active_mesh_wireframe: bool = False
    _active_mesh_shaded_wireframe: bool = False

    _db_path: str = None

    _ui_layout_main: QVBoxLayout = None

    _ui_class_list: QListWidget = None
    _ui_object_list: QListWidget = None

    _ui_vedo_widget: QVTKRenderWindowInteractor = None
    _ui_vedo_plotter: Plotter = None

    _ui_mesh_metadata: list[QLabel] = []

    _ui_layout_vedo: QVBoxLayout = None
    _ui_layout_options: QVBoxLayout = None

    _ui_tab_menu: QTabWidget = None

    _ui_db_selector: QComboBox = None

    def __init__(self):
        super(WindowDatabase, self).__init__()

        self._db_path = constants.DB_ORIGINAL_RELATIVE_PATH

        self.on_db_selector_changed(0)

    def db_selector_setup(self, db_name: str):
        self._ui_layout_main = QVBoxLayout()

        self.central_widget = QWidget(self)
        self.central_widget.setLayout(self._ui_layout_main)
        self.setCentralWidget(self.central_widget)

        # DB Selector
        self._ui_db_selector = QComboBox()
        self._ui_db_selector.addItems(constants.DATABASES)
        self._ui_db_selector.setCurrentText(db_name)
        self._ui_db_selector.currentIndexChanged.connect(self.on_db_selector_changed)

        self._ui_layout_main.addWidget(self._ui_db_selector)

    def no_db_ui_setup(self, db_name: str):
        self.db_selector_setup(db_name)

        self._ui_layout_main.addWidget(WidgetNoDb(db_name))




    def db_ui_setup(self, db_name: str):
        self.db_selector_setup(db_name)

        layout_db_all = QHBoxLayout()

        # Database display widgets
        self._ui_class_list, self._ui_object_list = self.ui_create_db_lists()
        self.ui_create_db_events()

        layout_database = QVBoxLayout()
        layout_database.addWidget(self._ui_class_list)
        layout_database.addWidget(self._ui_object_list)

        layout_db_all.addLayout(layout_database)

        # Main visualization window using vedo
        self._ui_vedo_widget, self._ui_vedo_plotter = self.ui_create_vedo_widget()

        self._ui_layout_vedo = QVBoxLayout()
        self._ui_layout_vedo.addWidget(self._ui_vedo_widget)

        # Selected Mesh metadata
        self._ui_mesh_metadata = self.ui_create_mesh_metadata()

        layout_db_all.addLayout(self._ui_layout_vedo)

        # Options
        self._ui_layout_options = QVBoxLayout()
        self._ui_layout_options.setAlignment(Qt.AlignTop)

        w_options = self.ui_create_options()
        for option in w_options:
            self._ui_layout_options.addWidget(option)

        layout_db_all.addLayout(self._ui_layout_options)

        self._ui_layout_main.addLayout(layout_db_all)

    def on_db_selector_changed(self, idx: int):
        db_name = constants.DATABASES[idx]
        self._db_path = str(os.path.join(constants.DB_RELATIVE_PATH, db_name))
        
        if not os.path.exists(self._db_path):
            self.no_db_ui_setup(db_name)
        else:
            self.db_ui_setup(db_name)

    def show_bbox_clicked(self, s):
        if s == Qt.Checked:
            self._active_mesh_bbox = True
        else:
            self._active_mesh_bbox = False

        self.show_mesh()

    def show_wireframe_clicked(self, s):
        if s == Qt.Checked:
            self._active_mesh_wireframe = True
        else:
            self._active_mesh_wireframe = False

        self.show_mesh()

    def show_mesh(self):
        if self._selected_object is not None:
            # Reset drawing
            self._ui_vedo_plotter.clear()

            mesh = load(os.path.join(self._db_path, self._selected_class, self._selected_object))
            to_show = [mesh]

            if self._active_mesh_bbox:
                to_show.append(mesh.box())

            if self._active_mesh_wireframe:
                mesh.lighting("plastic").wireframe(True)

            if self._active_mesh_shaded_wireframe:
                wireframe = mesh.copy()
                wireframe.lighting("off").wireframe(True)
                wireframe.color((0, 0, 255))
                to_show.append(wireframe)

            self._ui_vedo_plotter.show(to_show)

    def show_shaded_wireframe_clicked(self, s):
        if s == Qt.Checked:
            self._active_mesh_shaded_wireframe = True
        else:
            self._active_mesh_shaded_wireframe = False

        self.show_mesh()

    def ui_create_options(self):
        w_show_bbox = QCheckBox("Show Bounding Box")
        w_show_bbox.stateChanged.connect(self.show_bbox_clicked)

        w_show_wireframe = QCheckBox("Show Wireframe")
        w_show_wireframe.stateChanged.connect(self.show_wireframe_clicked)

        w_show_shaded_wireframe = QCheckBox("Show Wireframe + Shaded")
        w_show_shaded_wireframe.stateChanged.connect(self.show_shaded_wireframe_clicked)

        return [w_show_bbox, w_show_wireframe, w_show_shaded_wireframe]

    def ui_object_changed(self, list_item):
        # Reset drawing
        self._ui_vedo_plotter.clear()

        # If class has changed and there was
        # a selected item, then there's no selected item
        # now just display a text
        if list_item is None:
            self._ui_vedo_plotter.show([], constants.UI_NO_ITEM_SELECTED_PLACEHOLDER, at=0)
            _selected_object = None
            return

        self._selected_object = list_item.text()

        self._active_mesh = Mesh(os.path.join(self._db_path, self._selected_class, self._selected_object))
        self.show_mesh()

        for widget in self._ui_mesh_metadata:
            self._ui_layout_vedo.removeWidget(widget)

        self._ui_mesh_metadata = self.ui_create_mesh_metadata()

        for widget in self._ui_mesh_metadata:
            self._ui_layout_vedo.addWidget(widget)

    def ui_class_changed(self, list_item):
        self._selected_class = list_item.text()

        files = os.listdir(os.path.join(self._db_path, self._selected_class))
        self._ui_object_list.clear()
        self._ui_object_list.addItems(files)

        for widget in self._ui_mesh_metadata:
            self._ui_layout_vedo.removeWidget(widget)
            widget.setParent(None)
            widget.deleteLater()

        self._ui_mesh_metadata = []

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

    def ui_create_mesh_metadata(self):
        if self._active_mesh is None:
            return []

        return [
            QLabel("Vertices: " + str(self._active_mesh.get_vertices())),
            QLabel("Cells: " + str(self._active_mesh.get_cells())),
            QLabel("Triangles: " + str(self._active_mesh.get_no_triangles())),
            QLabel("Quads: " + str(self._active_mesh.get_no_quads()))
        ]

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

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QLabel, QLineEdit
from Mesh import Mesh
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vedo import Plotter
from constants import UI_NO_ITEM_SELECTED_PLACEHOLDER


class Widget3DViewer(QWidget):
    _mesh: Mesh = None

    _ui_layout_main: QVBoxLayout = None
    _ui_layout_metadata: QVBoxLayout = None
    _ui_widgets_metadata: list[QLabel] = None

    _ui_vedo_widget: QVTKRenderWindowInteractor = None
    _ui_vedo_plotter: Plotter = None

    _flag_bbox: bool = False
    _flag_wireframe: bool = False
    _flag_shaded_wireframe: bool = False

    _title: str = None

    def __init__(self, mesh: Mesh = None, with_options: bool = True,
                 with_description: bool = True, title: str = None):
        super().__init__()

        self._mesh = mesh
        self._title = title

        self._ui_layout_main = QVBoxLayout()

        # Vedo 3D Plotter
        self._ui_vedo_widget, self._ui_vedo_plotter = self.ui_create_vedo_widget()
        self._ui_vedo_widget.setContentsMargins(0, 0, 0, 0)
        self._ui_layout_main.addWidget(self._ui_vedo_widget)

        # Selected Mesh metadata and Options
        layout_metadata_options = QHBoxLayout()

        self._ui_layout_metadata = QVBoxLayout()
        self._ui_widgets_metadata = self.ui_create_mesh_metadata()
        for metadata in self._ui_widgets_metadata:
            self._ui_layout_metadata.addWidget(metadata)

        layout_options = QVBoxLayout()
        layout_options.setAlignment(Qt.AlignTop)

        w_options = self.ui_create_options()
        for option in w_options:
            layout_options.addWidget(option)

        if with_description:
            layout_metadata_options.addLayout(self._ui_layout_metadata)

        if with_options:
            layout_metadata_options.addLayout(layout_options)

        self._ui_layout_main.addLayout(layout_metadata_options)

        self.setLayout(self._ui_layout_main)

        self.setMinimumSize(600, 600)

        self.show_mesh()

    def set_mesh(self, mesh: Mesh):
        self._mesh = mesh

    def show_none(self):
        self._ui_vedo_plotter.clear()
        self._ui_vedo_plotter.show([], UI_NO_ITEM_SELECTED_PLACEHOLDER, at=0)

        for widget in self._ui_widgets_metadata:
            self._ui_layout_metadata.removeWidget(widget)
            widget.setParent(None)
            widget.deleteLater()

        self._ui_widgets_metadata = []

    def show_mesh(self):
        if self._mesh is None:
            self.show_none()
            return

        self._ui_vedo_plotter.clear()

        to_show = [self._mesh.vedo_mesh]

        if self._flag_bbox:
            to_show.append(self._mesh.vedo_mesh.box())

        if self._flag_wireframe:
            self._mesh.vedo_mesh.lighting("plastic").wireframe(True)
        else:
            self._mesh.vedo_mesh.lighting("plastic").wireframe(False)

        if self._flag_shaded_wireframe:
            wireframe = self._mesh.vedo_mesh.copy()
            wireframe.lighting("off").wireframe(True)
            wireframe.color((0, 0, 255))
            to_show.append(wireframe)

        self._ui_vedo_plotter.show(to_show, self._title, axes=1, interactive=False)

        for widget in self._ui_widgets_metadata:
            self._ui_layout_metadata.removeWidget(widget)
            widget.setParent(None)
            widget.deleteLater()

        self._ui_widgets_metadata = self.ui_create_mesh_metadata()

        for widget in self._ui_widgets_metadata:
            self._ui_layout_metadata.addWidget(widget)

    def ui_create_vedo_widget(self):
        # Create the VTK render window interactor (QVTKRenderWindowInteractor)
        vtk_widget = QVTKRenderWindowInteractor()

        # Create a vedo Plotter and link it to the VTK widget
        plotter = Plotter(qt_widget=vtk_widget, interactive=False)

        # Start the VTK interactor
        vtk_widget.GetRenderWindow().Render()
        plotter.interactor.Start()

        return vtk_widget, plotter

    def ui_create_options(self):
        w_show_bbox = QCheckBox("Show Bounding Box")
        w_show_bbox.stateChanged.connect(self.show_bbox_clicked)

        w_show_wireframe = QCheckBox("Show Wireframe")
        w_show_wireframe.stateChanged.connect(self.show_wireframe_clicked)

        w_show_shaded_wireframe = QCheckBox("Show Wireframe + Shaded")
        w_show_shaded_wireframe.stateChanged.connect(self.show_shaded_wireframe_clicked)

        return [w_show_bbox, w_show_wireframe, w_show_shaded_wireframe]

    def ui_create_mesh_metadata(self):
        if self._mesh is None:
            return []

        return [
            QLabel("Class: " + str(self._mesh.get_class())),
            QLabel("Name: " + str(self._mesh.name)),
            QLabel("\nVertices: " + str(self._mesh.get_no_vertices())),
            QLabel("Cells: " + str(self._mesh.get_no_cells())),
            QLabel("Triangles: " + str(self._mesh.get_no_triangles())),
            QLabel("Quads: " + str(self._mesh.get_no_quads()))
        ]

    def show_shaded_wireframe_clicked(self, s):
        if s == Qt.Checked:
            self._flag_shaded_wireframe = True
        else:
            self._flag_shaded_wireframe = False

        self.show_mesh()

    def show_wireframe_clicked(self, s):
        if s == Qt.Checked:
            self._flag_wireframe = True
        else:
            self._flag_wireframe = False

        self.show_mesh()

    def show_bbox_clicked(self, s):
        if s == Qt.Checked:
            self._flag_bbox = True
        else:
            self._flag_bbox = False

        self.show_mesh()

    @property
    def mesh(self):
        return self._mesh

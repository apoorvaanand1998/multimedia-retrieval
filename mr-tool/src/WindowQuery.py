from PyQt5.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget, QScrollArea, QPushButton, QFileDialog, \
    QHBoxLayout, QLabel, QListWidget
from PyQt5.QtCore import QDir, QThread, pyqtSignal
import constants
from Mesh import Mesh, MeshDescriptors
from Widget3DViewer import Widget3DViewer
import normalization
import global_descriptors


# Worker thread class
class WorkerThread(QThread):
    # Define a signal to notify the main thread
    progress_signal = pyqtSignal(int)

    def run(self):
        # Loop from 1 to 100 and emit the progress signal
        for i in range(1, 101):
            self.msleep(100)  # Sleep to simulate work (100 ms per loop)
            self.progress_signal.emit(i)


class WindowQuery(QMainWindow):
    _query_mesh: Mesh = None
    _query_mesh_normalized: Mesh = None

    _central_widget: QWidget = None
    _ui_layout_main: QVBoxLayout = None

    _widget_query_mesh: QWidget = None
    _ui_query_mesh_3d_viewer: Widget3DViewer = None
    _ui_query_mesh_normalized_3d_viewer: Widget3DViewer = None

    def __init__(self):
        super().__init__()
        self._central_widget = QWidget(self)
        self._ui_layout_main = QVBoxLayout()

        button = QPushButton("Browse Mesh")
        button.setMinimumSize(self.width(), self.height() / 4)
        button.clicked.connect(self.browse_file)

        self._ui_layout_main.addWidget(button)

        self.setup_query_mesh()

        self._central_widget.setLayout(self._ui_layout_main)
        self.setCentralWidget(self._central_widget)

        # scroll = QScrollArea(self)
        # scroll.setWidget(self._central_widget)

        # self.setCentralWidget(scroll)

    def setup_query_mesh(self):
        if self._widget_query_mesh is not None:
            self._ui_layout_main.removeWidget(self._widget_query_mesh)

        self._widget_query_mesh = QWidget()
        layout = QHBoxLayout()

        if self._query_mesh is not None:
            self._query_mesh_normalized = normalization.full_normalization(self._query_mesh)

            # Original Mesh
            self._ui_query_mesh_3d_viewer = Widget3DViewer(self._query_mesh, title="Original Mesh", with_options=False,
                                                           with_description=False)
            self._ui_query_mesh_3d_viewer._flag_shaded_wireframe = True
            self._ui_query_mesh_3d_viewer.show_mesh()

            layout.addWidget(self._ui_query_mesh_3d_viewer)

            # Normalised Mesh
            self._ui_query_mesh_normalized_3d_viewer = Widget3DViewer(self._query_mesh_normalized,
                                                                      title="Normalized Mesh", with_options=False,
                                                                      with_description=False)
            self._ui_query_mesh_normalized_3d_viewer._flag_shaded_wireframe = True
            self._ui_query_mesh_normalized_3d_viewer.show_mesh()

            layout.addWidget(self._ui_query_mesh_normalized_3d_viewer)

            # Normalised Mesh Descriptors
            layout.addWidget(self.setup_descriptors())

        self._widget_query_mesh.setLayout(layout)
        self._ui_layout_main.addWidget(self._widget_query_mesh)

    def setup_descriptors(self):
        descriptors: MeshDescriptors = global_descriptors.calculate_descriptors(self._query_mesh_normalized)

        w = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Global Descriptors"))
        list = QListWidget()
        list.addItem("Surfacea Area  : " + str(descriptors.surface_area))
        list.addItem("Compactness    : " + str(descriptors.compactness))
        list.addItem("Rectangularity : " + str(descriptors.rectangularity))
        list.addItem("Convexity      : " + str(descriptors.convexity))
        list.addItem("Diameter       : " + str(descriptors.diameter))
        list.addItem("Eccentricity   : " + str(descriptors.eccentricity))

        layout.addWidget(list)

        w.setLayout(layout)
        return w

    def browse_file(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setFilter(QDir.Files)

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            f = open(filenames[0], 'r')

            with f:
                try:
                    self._query_mesh = Mesh(filenames[0])
                    self.setup_query_mesh()
                except Exception as e:
                    print(e)

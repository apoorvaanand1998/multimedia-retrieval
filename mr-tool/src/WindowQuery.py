import time

from PyQt5.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget, QScrollArea, QPushButton, QFileDialog, \
    QHBoxLayout, QLabel, QListWidget, QProgressBar
from PyQt5.QtCore import QDir, QThread, pyqtSignal
import constants
from Mesh import Mesh, MeshDescriptors
from Widget3DViewer import Widget3DViewer
import resample
import normalization
import global_descriptors


# Worker thread class
class WorkerThread(QThread):
    # Define a signal to notify the main thread
    progress_signal = pyqtSignal(str, int, bool)

    file: str = None
    mesh: Mesh = None
    mesh_normalized: Mesh = None
    mesh_descriptors: MeshDescriptors = None

    def __init__(self, file: str):
        super().__init__()
        self.file = file

    def run(self):
        steps = 13
        step_progress = steps / 100 * 10

        # Loop from 1 to 100 and emit the progress signal
        # Step 1 - Load Mesh
        self.progress_signal.emit("Loading mesh...", 0, False)
        self.mesh = Mesh(self.file)
        self.progress_signal.emit("Loading mesh...", step_progress * 1, False)

        # Step 2 - Remeshing
        self.progress_signal.emit("Remeshing... Target value: 5000", step_progress * 1, False)
        resampled_mesh = resample.resample_mesh(self.mesh)
        if resampled_mesh is None:
            self.mesh_normalized = self.mesh.__copy__()
            self.progress_signal.emit("Remeshing Failed ... Continuing", step_progress * 2, False)
            time.sleep(2)
        else:
            self.mesh_normalized = resampled_mesh

        # Step 3 - Normalise Mesh
        # Step 3.1 - Translation
        self.progress_signal.emit("Normalising mesh... Translation", step_progress * 3, False)
        translated_mesh = normalization.translate_to_origin(self.mesh_normalized)
        time.sleep(0.5)

        # Step 3.2 - Scaling
        self.progress_signal.emit("Normalising mesh... Scaling", step_progress * 4, False)
        scaled_mesh = normalization.scale_to_unit_size(translated_mesh)
        time.sleep(0.5)

        # Step 3.3 - Align PCA
        self.progress_signal.emit("Normalising mesh... Align PCA", step_progress * 5, False)
        aligned_mesh = normalization.align_principal_axes(scaled_mesh)
        time.sleep(0.5)

        # Step 3.4 - Moment Flip
        self.progress_signal.emit("Normalising mesh... Moment Flip", step_progress * 6, False)
        flipped_mesh = normalization.flip_along_axes(aligned_mesh)
        time.sleep(0.5)

        self.mesh_normalized = flipped_mesh

        # Step 4 - Computing Global Descriptors
        self.mesh_descriptors = MeshDescriptors(self.mesh.path, self.mesh.name, self.mesh.get_class(),
                                                None, None, None, None, None, None)

        # Step 4.1 - Surface Area
        self.progress_signal.emit("Computing Global Descriptors... Surface Area", step_progress * 7, False)
        self.mesh_descriptors.set_surface_area(global_descriptors.calculate_surface_area(self.mesh_normalized))
        time.sleep(0.5)

        # Step 4.2 - Compactness
        self.progress_signal.emit("Computing Global Descriptors... Compactness", step_progress * 8, False)
        self.mesh_descriptors.set_compactness(global_descriptors.calculate_compactness(self.mesh_normalized))
        time.sleep(0.5)

        # Step 4.2 - Diameter
        self.progress_signal.emit("Computing Global Descriptors... Diameter", step_progress * 9, False)
        self.mesh_descriptors.set_diameter(global_descriptors.calculate_diameter(self.mesh_normalized))
        time.sleep(0.5)

        # Step 4.2 - Convexity
        self.progress_signal.emit("Computing Global Descriptors... Convexity", step_progress * 10, False)
        self.mesh_descriptors.set_convexity(global_descriptors.calculate_convexity(self.mesh_normalized))
        time.sleep(0.5)

        # Step 4.2 - Rectangularity
        self.progress_signal.emit("Computing Global Descriptors... Rectangularity", step_progress * 11, False)
        self.mesh_descriptors.set_rectangularity(global_descriptors.calculate_rectangularity(self.mesh_normalized))
        time.sleep(0.5)

        # Step 4.2 - Compactness
        self.progress_signal.emit("Computing Global Descriptors... Eccentricity", step_progress * 12, False)
        self.mesh_descriptors.set_eccentricity(global_descriptors.calculate_eccentricity(self.mesh_normalized))
        time.sleep(0.5)

        self.progress_signal.emit("Succesfully Loaded Mesh. Closing window in 2 seconds", 100, False)
        time.sleep(2)
        self.progress_signal.emit("Succesfully Loaded Mesh. Closing window in 2 seconds", 100, True)


class WindowLoadMesh(QMainWindow):
    _label: QLabel = None
    _progress_bar: QProgressBar = None

    worker: WorkerThread = None
    parent_window: QMainWindow = None

    def __init__(self, file: str, parent_window: QMainWindow):
        super().__init__()

        self.parent_window = parent_window

        w = QWidget(self)

        layout = QVBoxLayout()

        self.setWindowTitle("Loading Mesh " + file)

        self._label = QLabel("Loading Mesh")
        layout.addWidget(self._label)

        self._progress_bar = QProgressBar(w)
        self._progress_bar.setRange(0, 100)
        layout.addWidget(self._progress_bar)

        w.setLayout(layout)

        self.setCentralWidget(w)

        # Create the worker thread
        self.worker = WorkerThread(file)
        # Connect the progress signal to the update_label slot
        self.worker.progress_signal.connect(self.update_progress)
        # Start the worker thread
        self.worker.start()

    def update_progress(self, label_text: str, progress_bar_value: int, finished: bool):
        self._label.setText(label_text)
        self._progress_bar.setValue(progress_bar_value)

        if finished:
            self.parent_window._query_mesh = self.worker.mesh
            self.parent_window._query_mesh_normalized = self.worker.mesh_normalized
            self.parent_window._query_mesh_descriptors = self.worker.mesh_descriptors

            self.close()

            self.parent_window.setup_query_mesh()


class WindowQuery(QMainWindow):
    _query_mesh: Mesh = None
    _query_mesh_normalized: Mesh = None
    _query_mesh_descriptors: MeshDescriptors = None

    _central_widget: QWidget = None
    _ui_layout_main: QVBoxLayout = None

    _widget_query_mesh: QWidget = None
    _ui_query_mesh_3d_viewer: Widget3DViewer = None
    _ui_query_mesh_normalized_3d_viewer: Widget3DViewer = None

    _ui_loading: QMainWindow = None

    _window_load_mesh: WindowLoadMesh = None

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
                    self._window_load_mesh = WindowLoadMesh(filenames[0], self)
                    self._window_load_mesh.show()

                    self.setup_query_mesh()
                except Exception as e:
                    print(e)

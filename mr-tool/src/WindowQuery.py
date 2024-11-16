import time

from PyQt5.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget, QScrollArea, QPushButton, QFileDialog, \
    QHBoxLayout, QLabel, QListWidget, QProgressBar, QListWidgetItem, QLineEdit, QComboBox
from PyQt5.QtCore import QDir, QThread, pyqtSignal
import constants
from Mesh import Mesh, MeshDescriptors
from Widget3DViewer import Widget3DViewer
from WidgetSimpleHist import WidgetSimpleHist
import FINAL_resample
import FINAL_normalization
import FINAL_mesh_repair
import FINAL_global_descriptors
import FINAL_shape_descriptors
import FINAL_query


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
        steps = 17 + 1
        step_progress = 100 / steps

        # Loop from 1 to 100 and emit the progress signal
        # Step 1 - Load Mesh
        self.mesh = Mesh(self.file)
        self.progress_signal.emit("Loading mesh...", step_progress * 1, False)

        # Step 2 - Remeshing
        self.progress_signal.emit("Remeshing... Target value: 5000", step_progress * 1, False)
        resampled_mesh = FINAL_resample.resample_mesh(Mesh(self.mesh.path, self.mesh.vedo_mesh))
        if resampled_mesh is None:
            self.mesh_normalized = Mesh(self.mesh.path, self.mesh.vedo_mesh)
            self.progress_signal.emit("Remeshing Failed ... Continuing", step_progress * 2, False)
            time.sleep(2)
        else:
            self.mesh_normalized = Mesh(resampled_mesh.path, resampled_mesh.vedo_mesh)

        # Step 2.5 - Filling Holes
        self.progress_signal.emit("Filling Holes", step_progress * 1, False)
        vedo_m, _ = FINAL_mesh_repair.fill_holes(self.mesh_normalized.vedo_mesh)
        self.mesh_normalized.set_vedo_mesh(vedo_m)

        # Normalise Mesh
        # Step 3 - Translation
        self.progress_signal.emit("Normalising mesh... Translation", step_progress * 3, False)
        translated_mesh = FINAL_normalization.translate_to_origin(self.mesh_normalized)
        time.sleep(0.5)

        a = translated_mesh.get_no_vertices()

        # Step 4 - Scaling
        self.progress_signal.emit("Normalising mesh... Scaling", step_progress * 4, False)
        scaled_mesh = FINAL_normalization.scale_to_unit_size(translated_mesh)
        time.sleep(0.5)

        # Step 5 - Align PCA
        self.progress_signal.emit("Normalising mesh... Align PCA", step_progress * 5, False)
        aligned_mesh = FINAL_normalization.align_principal_axes(scaled_mesh)
        time.sleep(0.5)

        # Step 6 - Moment Flip
        self.progress_signal.emit("Normalising mesh... Moment Flip", step_progress * 6, False)
        flipped_mesh = FINAL_normalization.flip_along_axes(aligned_mesh)
        time.sleep(0.5)

        self.mesh_normalized = flipped_mesh

        # Computing Global Descriptors
        self.mesh_descriptors = MeshDescriptors(self.mesh.path, self.mesh.name, self.mesh.get_class(),
                                                None, None, None, None, None, None)

        # Step 7- Surface Area
        self.progress_signal.emit("Computing Global Descriptors... Surface Area", step_progress * 7, False)
        try:
            self.mesh_descriptors.set_surface_area(FINAL_global_descriptors.calculate_surface_area(self.mesh_normalized))
        except Exception as e:
            print('Cannot calculate surface area. Putting None')
            print(e)
        time.sleep(0.5)

        # Step 8 - Compactness
        self.progress_signal.emit("Computing Global Descriptors... Compactness", step_progress * 8, False)
        try:
            self.mesh_descriptors.set_compactness(FINAL_global_descriptors.calculate_compactness(self.mesh_normalized))
        except Exception as e:
            print('Cannot calculate Compactness. Putting None')
            print(e)
        time.sleep(0.5)

        # Step 9 - Diameter
        self.progress_signal.emit("Computing Global Descriptors... Diameter", step_progress * 9, False)
        try:
            self.mesh_descriptors.set_diameter(FINAL_global_descriptors.calculate_diameter(self.mesh_normalized))
        except Exception as e:
            print('Cannot calculate diameter. Putting None')
            print(e)
        time.sleep(0.5)

        # Step 10 - Convexity
        self.progress_signal.emit("Computing Global Descriptors... Convexity", step_progress * 10, False)
        try:
            self.mesh_descriptors.set_convexity(FINAL_global_descriptors.calculate_convexity(self.mesh_normalized))
        except Exception as e:
            print("Cannot calculate convexity. Putting None")
            print(e)
        time.sleep(0.5)

        # Step 11 - Rectangularity
        self.progress_signal.emit("Computing Global Descriptors... Rectangularity", step_progress * 11, False)
        try:
            self.mesh_descriptors.set_rectangularity(
                FINAL_global_descriptors.calculate_rectangularity(self.mesh_normalized))
        except Exception as e:
            print("Cannot calculate rectangularity. Putting None")
            print(e)
        time.sleep(0.5)

        # Step 12 - Compactness
        self.progress_signal.emit("Computing Global Descriptors... Eccentricity", step_progress * 12, False)
        self.mesh_descriptors.set_eccentricity(FINAL_global_descriptors.calculate_eccentricity(self.mesh_normalized))
        time.sleep(0.5)

        # Computing shape descriptors
        # Step 13 - A3
        self.progress_signal.emit("Computing Shape Descriptors... A3", step_progress * 13, False)
        self.mesh_descriptors.set_a3(FINAL_shape_descriptors.a3(self.mesh_normalized.vedo_mesh))

        # Step 14 - D1
        self.progress_signal.emit("Computing Shape Descriptors... D1", step_progress * 14, False)
        self.mesh_descriptors.set_d1(FINAL_shape_descriptors.d1(self.mesh_normalized.vedo_mesh))

        # Step 15 - D2
        self.progress_signal.emit("Computing Shape Descriptors... D2", step_progress * 15, False)
        self.mesh_descriptors.set_d2(FINAL_shape_descriptors.d2(self.mesh_normalized.vedo_mesh))

        # Step 16 - D3
        self.progress_signal.emit("Computing Shape Descriptors... D3", step_progress * 16, False)
        self.mesh_descriptors.set_d3(FINAL_shape_descriptors.d3(self.mesh_normalized.vedo_mesh))

        # Step 17 - D4
        self.progress_signal.emit("Computing Shape Descriptors... D4", step_progress * 17, False)
        self.mesh_descriptors.set_d4(FINAL_shape_descriptors.d4(self.mesh_normalized.vedo_mesh))

        self.progress_signal.emit("Succesfully Loaded Mesh. Closing window in 2 seconds", 100, False)
        time.sleep(1)
        self.progress_signal.emit("Succesfully Loaded Mesh. Closing window in 1 second", 100, True)
        time.sleep(1)


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

        self._label = QLabel("")
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
        self._label.setText(self._label.text() + "\n" + label_text)
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

    _widget_query_results: QWidget = None
    _query_no_results: int = None
    _distance_algorithm: FINAL_query.QueryMode = FINAL_query.QueryMode.EUCLIDEAN
    _query_results: list[FINAL_query.QueryResult] = None
    _query_no_queried: int = None
    _query_no_skipped: int = None

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

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setWidget(self._central_widget)

        self.setCentralWidget(scroll)

    def setup_query_mesh(self):
        if self._widget_query_mesh is not None:
            self._ui_layout_main.removeWidget(self._widget_query_mesh)

        self._widget_query_mesh = QWidget()
        layout = QHBoxLayout()

        if self._query_mesh is not None:
            # Original Mesh
            self._ui_query_mesh_3d_viewer = Widget3DViewer(self._query_mesh, title="Original Mesh", with_options=True,
                                                           with_description=True)
            self._ui_query_mesh_3d_viewer._flag_shaded_wireframe = True
            self._ui_query_mesh_3d_viewer.show_mesh()

            layout.addWidget(self._ui_query_mesh_3d_viewer)

            # Normalised Mesh
            self._ui_query_mesh_normalized_3d_viewer = Widget3DViewer(self._query_mesh_normalized,
                                                                      title="Normalized Mesh", with_options=True,
                                                                      with_description=True)
            self._ui_query_mesh_normalized_3d_viewer._flag_shaded_wireframe = True
            self._ui_query_mesh_normalized_3d_viewer.show_mesh()

            layout.addWidget(self._ui_query_mesh_normalized_3d_viewer)

            # Normalised Mesh Descriptors
            layout.addWidget(self.setup_descriptors())

        self._widget_query_mesh.setLayout(layout)
        self._ui_layout_main.addWidget(self._widget_query_mesh)

        self.setup_query()

    def set_no_results(self, n):
        self._query_no_results = int(n)

    def set_distance_algorithm(self, s):
        self._distance_algorithm = FINAL_query.QueryMode[s]

    def start_query(self):
        self._query_results, self._query_no_queried, self._query_no_skipped = FINAL_query.query(
            self._query_mesh_descriptors, self._query_no_results, self._distance_algorithm)
        self.setup_query()

    def setup_query(self):
        if self._query_mesh is None:
            return

        if self._widget_query_results is not None:
            self._ui_layout_main.removeWidget(self._widget_query_results)

        self._widget_query_results = QWidget()
        layout = QVBoxLayout()

        # Inputs
        layout_inputs = QHBoxLayout()

        w_no_results = QLineEdit()
        w_no_results.setPlaceholderText("Number of results")
        w_no_results.textChanged.connect(self.set_no_results)
        layout_inputs.addWidget(w_no_results)

        w_start_search = QPushButton("Query")
        w_start_search.clicked.connect(self.start_query)
        layout_inputs.addWidget(w_start_search)

        l_combo = QHBoxLayout()
        l_combo.addWidget(QLabel("Distance algorithm: "))

        w_combobox = QComboBox()
        w_combobox.addItem("euclidean")
        w_combobox.addItem("emd")
        w_combobox.currentTextChanged.connect(self.set_distance_algorithm)
        l_combo.addWidget(w_combobox)

        layout.addLayout(layout_inputs)
        layout.addLayout(l_combo)

        if self._query_results is not None:
            # meta of query
            layout_results_meta = QHBoxLayout()
            layout_results_meta.addWidget(QLabel("Queried: " + str(self._query_no_queried)))
            layout_results_meta.addWidget(QLabel("Skipped: " + str(self._query_no_skipped)))
            layout.addLayout(layout_results_meta)

            layout_results = QHBoxLayout()
            next_row = 3
            showed = 0
            for idx, query_result in enumerate(self._query_results):
                if idx == next_row:
                    layout.addLayout(layout_results)
                    layout_results = QHBoxLayout()
                    showed += next_row

                mesh: Mesh = Mesh(query_result.mesh_descriptors.path)
                title = mesh.get_class() + "/" + mesh.name + "\nDist: " + str(query_result.dist)
                w_result = Widget3DViewer(mesh, title=title, with_options=True, with_description=True)
                layout_results.addWidget(w_result)

            if showed != len(self._query_results):
                layout.addLayout(layout_results)

        self._widget_query_results.setLayout(layout)
        self._ui_layout_main.addWidget(self._widget_query_results)

    def setup_descriptors(self):
        if self._query_mesh_descriptors is not None:
            descriptors = self._query_mesh_descriptors
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

        shape_descriptors_layout_0 = QHBoxLayout()
        a3 = WidgetSimpleHist(self._query_mesh_descriptors.a3[0], self._query_mesh_descriptors.a3[1], "A3")
        d1 = WidgetSimpleHist(self._query_mesh_descriptors.d1[0], self._query_mesh_descriptors.d1[1], "D1")
        d2 = WidgetSimpleHist(self._query_mesh_descriptors.d2[0], self._query_mesh_descriptors.d2[1], "D2")
        shape_descriptors_layout_0.addWidget(a3)
        shape_descriptors_layout_0.addWidget(d1)
        shape_descriptors_layout_0.addWidget(d2)

        layout.addLayout(shape_descriptors_layout_0)

        shape_descriptors_layout_1 = QHBoxLayout()
        d3 = WidgetSimpleHist(self._query_mesh_descriptors.d3[0], self._query_mesh_descriptors.d3[1], "D3")
        d4 = WidgetSimpleHist(self._query_mesh_descriptors.d4[0], self._query_mesh_descriptors.d4[1], "D4")
        shape_descriptors_layout_1.addWidget(d3)
        shape_descriptors_layout_1.addWidget(d4)

        layout.addLayout(shape_descriptors_layout_1)

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

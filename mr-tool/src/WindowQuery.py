from PyQt5.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget, QScrollArea, QPushButton, QFileDialog, \
    QHBoxLayout
from PyQt5.QtCore import QDir
import constants
from Mesh import Mesh
from Widget3DViewer import Widget3DViewer


class WindowQuery(QMainWindow):
    _query_mesh: Mesh = None

    _central_widget: QWidget = None
    _ui_layout_main: QVBoxLayout = None

    _widget_query_mesh: QWidget = None
    _ui_query_mesh_3d_viewer: Widget3DViewer = None

    def __init__(self):
        super().__init__()
        self._central_widget = QWidget(self)
        self._ui_layout_main = QVBoxLayout()

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

        if self._query_mesh is None:
            button = QPushButton("Browse Mesh")
            button.setMinimumSize(self.width(), self.height() / 4)
            button.clicked.connect(self.browse_file)

            layout.addWidget(button)
        else:
            self._ui_query_mesh_3d_viewer = Widget3DViewer(self._query_mesh, with_options=False)

            layout.addWidget(self._ui_query_mesh_3d_viewer)
            # TODO: Calculate and Add Normalized 3d Viewer

            # TODO: Calculate and Add Shape descriptors

        self._widget_query_mesh.setLayout(layout)
        self._ui_layout_main.addWidget(self._widget_query_mesh)

    def browse_file(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setFilter(QDir.Files)
        filenames = list[str]

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            f = open(filenames[0], 'r')

            with f:
                try:
                    self._query_mesh = Mesh(filenames[0])
                    self.setup_query_mesh()
                except Exception as e:
                    print(e)

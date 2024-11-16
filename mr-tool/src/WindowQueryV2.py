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
import test


class WindowQueryV2(QMainWindow):

    def __init__(self):
        super().__init__()

        self._central_widget = QWidget(self)
        self._ui_layout_main = QVBoxLayout()

        self.setup_results(4)

        self._central_widget.setLayout(self._ui_layout_main)
        self.setCentralWidget(self._central_widget)

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setWidget(self._central_widget)

        self.setCentralWidget(scroll)

    def setup_results(self, k: int = 5):
        layout_all = QVBoxLayout()
        for i in range(3):
            layout = QHBoxLayout()

            if i == 0:
                query_mesh = Mesh("../../ShapeDatabase_INFOMR/Bicycle/D00016.obj")
                result_meshes = test.find_dist('Bicycle/D00016')[0: k]

            if i == 1:
                query_mesh = Mesh("../../ShapeDatabase_INFOMR/Starship/m1354.obj")
                result_meshes = test.find_dist('Starship/m1354')[0: k]


            if i == 2:
                query_mesh = Mesh("../../ShapeDatabase_INFOMR/AquaticAnimal/m56.obj")
                result_meshes = test.find_dist('AquaticAnimal/m56')[0: k]


            w_query_item = Widget3DViewer(query_mesh)
            layout.addWidget(w_query_item)

            a = result_meshes.iloc[0: k][['name', 'dist']]

            for j in range(k):
                l = QHBoxLayout()
                b = a.iloc[j].to_list()
                result_mesh = Mesh("../../remeshed_normalized_filled_ShapeDB/" + b[0] + ".obj")
                w_result_item = Widget3DViewer(result_mesh, title="Dist: " + str(b[1]))
                l.addWidget(w_result_item)

                w = QWidget()
                w.setStyleSheet("background-color: 'lightblue'")
                w.setLayout(l)
                layout.addWidget(w)

            layout_all.addLayout(layout)

        self._ui_layout_main.addLayout(layout_all)

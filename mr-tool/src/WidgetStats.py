from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from WidgetHistogram import WidgetHistogram
from WidgetBarChart import WidgetBarChart
import utils


class WidgetStats(QWidget):
    _ui_layout_main: QVBoxLayout = None

    _ui_label_title: QLabel = None

    def __init__(self, db_map: dict[str, list[str]], db_count: int, db_name: str):
        super().__init__()

        self.db_map = db_map
        self.db_count = db_count
        self.db_name = db_name

        self.meshes_stats = utils.get_output_stats(self.db_name)

        self._ui_layout_main = QVBoxLayout()

        self._ui_label_title = QLabel(self.db_name)

        self._ui_layout_main.addWidget(self._ui_label_title)

        # Histogram of vertices
        self._ui_layout_main.addWidget(self.create_barchart_classes())

        # Histogram of faces

        # Histogram of classes

        # Average shape vedo plot

        # Outliers shapes

        self.setLayout(self._ui_layout_main)

    def create_barchart_classes(self):
        classes_labels = list(self.db_map.keys())
        counts = [len(sublist) for sublist in list(self.db_map.values())]

        return WidgetBarChart(
            counts,
            classes_labels,
            self
        )

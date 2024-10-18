import time
import os
import utils
import constants
from Mesh import Mesh

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QProgressBar, QListWidget, QApplication


class WidgetEmptyStats(QWidget):
    _ui_layout_main: QVBoxLayout = None

    _ui_label_title: QLabel = None
    _ui_load_button: QPushButton = None
    _ui_progress_bar: QProgressBar = None

    _ui_log_box: QListWidget = None

    def __init__(self, db_map, db_count, db_name):
        super().__init__()

        self.db_map = db_map
        self.db_count = db_count
        self.db_name = db_name

        self._ui_layout_main = QVBoxLayout()

        self._ui_label_title = QLabel(constants.UI_NO_STATS_FILE + " for " + self.db_name)
        self._ui_load_button = QPushButton(constants.UI_STATS_BUTTON)

        self._ui_progress_bar = QProgressBar(self)
        self._ui_progress_bar.setMaximum(self.db_count)

        self._ui_load_button.clicked.connect(self.on_load_button_clicked)

        self._ui_log_box = QListWidget()

        self._ui_layout_main.addWidget(self._ui_label_title)
        self._ui_layout_main.addWidget(self._ui_load_button)
        self._ui_layout_main.addWidget(self._ui_log_box)
        self._ui_layout_main.addWidget(self._ui_progress_bar)

        self.setLayout(self._ui_layout_main)

    def on_load_button_clicked(self):
        obj_count = 0
        obj_stats = []
        for obj_class, obj_list in self.db_map.items():
            for obj in obj_list:
                self._ui_log_box.addItem("Computing statistics for " + obj_class + " -> " + obj)
                self._ui_log_box.scrollToBottom()
                obj_count += 1

                mesh = Mesh(str(os.path.join(constants.DB_RELATIVE_PATH, self.db_name, obj_class, obj)))
                relative_path = str(os.path.join(constants.DB_RELATIVE_PATH, self.db_name, mesh._class, mesh.name))

                stats = mesh.get_statistics()
                stats.insert(0, relative_path)
                obj_stats.append(stats)

                self._ui_progress_bar.setValue(obj_count)

                QApplication.processEvents()

        self._ui_log_box.addItem("\nComputed statistics for " + str(obj_count) + " objects.")

        statistics_folder = str(os.path.join(constants.OUTPUT_DIR_RELATIVE_PATH, "Statistics",
                                         self.db_name))
        stats_file_path = utils.save_output_stats(self.db_name, obj_stats)

        self._ui_log_box.addItem("\nStatistics saved at " + stats_file_path + "")
        QApplication.processEvents()

        for i in range(0, 3):
            self._ui_log_box.addItem("\nReloading in " + str(3 - i) + "s")
            self._ui_log_box.scrollToBottom()
            QApplication.processEvents()

            time.sleep(1)

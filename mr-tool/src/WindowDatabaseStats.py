import os.path
import time

import constants
import utils

from Mesh import Mesh

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QProgressBar, QListWidget, QApplication
from vedo import load


class WindowDatabaseStats(QWidget):
    _ui_layout_main: QVBoxLayout = None

    _ui_label_title: QLabel = None
    _ui_load_button: QPushButton = None
    _ui_progress_bar: QProgressBar = None

    _ui_log_box: QListWidget = None

    _db_map: dict[str, list[str]] = None

    def __init__(self):
        super().__init__()

        self._db_map, self._db_total_count = utils.get_database_map()

        self._ui_layout_main = QVBoxLayout()

        if not os.path.exists(os.path.join(constants.OUTPUT_DIR_RELATIVE_PATH, constants.STATS_FILE_NAME)):
            self._ui_label_title = QLabel(constants.UI_NO_STATS_FILE)
            self._ui_load_button = QPushButton(constants.UI_STATS_BUTTON)
            self._ui_progress_bar = QProgressBar(self)
            self._ui_progress_bar.setMaximum(self._db_total_count)

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
        for obj_class, obj_list in self._db_map.items():
            for obj in obj_list:
                self._ui_log_box.addItem("Computing statistics for " + obj_class + " -> " + obj)
                self._ui_log_box.scrollToBottom()
                obj_count += 1

                mesh = Mesh(os.path.join(constants.DB_RELATIVE_PATH, obj_class, obj))
                obj_stats.append(mesh.get_statistics())

                self._ui_progress_bar.setValue(obj_count)

                QApplication.processEvents()

            if (obj_count > 3):
                break

        self._ui_log_box.addItem("\nComputed statistics for " + str(obj_count) + " objects.")

        stats_file_path = utils.save_output_stats(constants.DB_ORIGINAL_NAME, obj_stats)

        self._ui_log_box.addItem("\nStatistics saved at " + stats_file_path + "")
        QApplication.processEvents()

        for i in range(0, 3):
            self._ui_log_box.addItem("\nReloading in " + str(3 - i) + "s")
            self._ui_log_box.scrollToBottom()
            QApplication.processEvents()

            time.sleep(1)



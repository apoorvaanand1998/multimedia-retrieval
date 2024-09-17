import os.path
import time

import constants
import utils

from Mesh import Mesh
from WidgetNoDb import WidgetNoDb

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QProgressBar, QListWidget, QApplication, \
    QVBoxLayout, QComboBox, QMainWindow


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
        for obj_class, obj_list in self._db_map.items():
            for obj in obj_list:
                self._ui_log_box.addItem("Computing statistics for " + obj_class + " -> " + obj)
                self._ui_log_box.scrollToBottom()
                obj_count += 1

                mesh = Mesh(str(os.path.join(constants.DB_RELATIVE_PATH, obj_class, obj)))
                obj_stats.append(mesh.get_statistics())

                self._ui_progress_bar.setValue(obj_count)

                QApplication.processEvents()

        self._ui_log_box.addItem("\nComputed statistics for " + str(obj_count) + " objects.")

        stats_file_path = utils.save_output_stats(self.db_name, obj_stats)

        self._ui_log_box.addItem("\nStatistics saved at " + stats_file_path + "")
        QApplication.processEvents()

        for i in range(0, 3):
            self._ui_log_box.addItem("\nReloading in " + str(3 - i) + "s")
            self._ui_log_box.scrollToBottom()
            QApplication.processEvents()

            time.sleep(1)


class WidgetStats(QWidget):
    _ui_layout_main: QVBoxLayout = None

    _ui_label_title: QLabel = None

    def __init__(self, db_map, db_count, db_name):
        super().__init__()

        self.db_map = db_map
        self.db_count = db_count
        self.db_name = db_name

        self._ui_layout_main = QVBoxLayout()

        self._ui_label_title = QLabel(self.db_name)

        self._ui_layout_main.addWidget(self._ui_label_title)

        self.setLayout(self._ui_layout_main)


class WindowDatabaseStats(QMainWindow):
    _ui_layout_main: QVBoxLayout = None
    _ui_db_selector: QComboBox = None
    _ui_db_widget: QWidget = None

    def __init__(self):
        super().__init__()

        self.db_selector_setup(constants.DB_ORIGINAL_NAME)

        self.on_db_selector_changed(0)  # To set the first widget

        self._ui_layout_main.addWidget(self._ui_db_widget)

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

    def on_db_selector_changed(self, idx: int):
        db_name = constants.DATABASES[idx]

        db_path = str(os.path.join(constants.DB_RELATIVE_PATH, db_name))

        if os.path.exists(db_path):
            db_map, db_count = utils.get_database_map(db_path)
            stats_file_path = str(os.path.join(constants.OUTPUT_DIR_RELATIVE_PATH, db_name, constants.STATS_FILE_NAME))
            if os.path.exists(stats_file_path):
                self._ui_db_widget = WidgetStats(db_map, db_count, db_name)
            else:
                self._ui_db_widget = WidgetEmptyStats(db_map, db_count, db_name)
        else:
            self._ui_db_widget = WidgetNoDb(db_name)

        self.db_selector_setup(db_name)
        self._ui_layout_main.addWidget(self._ui_db_widget)

import os.path

from PyQt5.QtCore import Qt

import constants
import utils

from WidgetNoDb import WidgetNoDb
from WidgetStats import WidgetStats
from WidgetEmptyStats import WidgetEmptyStats

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QMainWindow, QScrollArea


class WindowDatabaseStats(QMainWindow):
    _ui_layout_main: QVBoxLayout = None
    _ui_db_selector: QComboBox = None
    _ui_db_widget: QWidget = None

    def __init__(self):
        super().__init__()

        self.db_selector_setup(constants.DB_ORIGINAL_NAME)

        self.on_db_selector_changed(0)  # To set the first widget

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
            stats_file_path = str(os.path.join(constants.OUTPUT_DIR_RELATIVE_PATH, "Statistics",
                                               db_name, constants.STATS_FILE_NAME))
            if os.path.exists(stats_file_path):
                db_stats = utils.get_output_stats(db_name)
                self._ui_db_widget = WidgetStats(db_map, db_count, db_name, db_stats)
            else:
                self._ui_db_widget = WidgetEmptyStats(db_map, db_count, db_name)
        else:
            self._ui_db_widget = WidgetNoDb(db_name)

        self.db_selector_setup(db_name)

        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setWidget(self._ui_db_widget)

        self._ui_layout_main.addWidget(scroll)

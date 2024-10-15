from PyQt5.QtCore import Qt

import constants
import os
import utils

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QComboBox, QScrollArea
from WidgetNoDb import WidgetNoDb


class IWindowDBSelector(QMainWindow):

    def __init__(self, main_widget_class):
        super(IWindowDBSelector, self).__init__()

        self.main_widget = None
        self.main_widget_class = main_widget_class

        self.db_selector_setup(constants.DB_ORIGINAL_NAME)
        self.on_db_selector_changed(0)

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
            self.main_widget = self.main_widget_class(db_map)
        else:
            self.main_widget = WidgetNoDb(db_name)

        self.db_selector_setup(db_name)

        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setWidget(self.main_widget)

        self._ui_layout_main.addWidget(scroll)

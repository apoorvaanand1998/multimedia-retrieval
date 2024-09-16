import os.path
from util import constants

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QProgressBar


class WindowDatabaseStats(QWidget):
    _ui_layout_main: QVBoxLayout = None

    _ui_label_title: QLabel = None
    _ui_load_button: QPushButton = None
    _ui_progress_bar: QProgressBar = None

    def __init__(self):
        super().__init__()
        self._ui_layout_main = QVBoxLayout()

        if not os.path.exists(os.path.join(constants.OUTPUT_DIR_RELATIVE_PATH, constants.STATS_FILE_NAME)):
            self._ui_label_title = QLabel(constants.UI_NO_STATS_FILE)
            self._ui_load_button = QPushButton(constants.UI_STATS_BUTTON)

            self._ui_load_button.clicked.connect(self.on_load_button_clicked)

            self._ui_layout_main.addWidget(self._ui_label_title)
            self._ui_layout_main.addWidget(self._ui_load_button)

        self.setLayout(self._ui_layout_main)

    def on_load_button_clicked(self):
        self._ui_progress_bar = QProgressBar()



        self._ui_layout_main.addWidget(self._ui_progress_bar)


import os.path
from util import constants

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QProgressBar


class WindowDatabaseStats(QWidget):
    _ui_label_title: QLabel = None
    _ui_load_button: QPushButton = None
    _ui_progress_bar: QProgressBar = None

    def __init__(self):
        super().__init__()
        layout_main = QVBoxLayout()

        a = os.path.join(constants.OUTPUT_DIR_RELATIVE_PATH, constants.STATS_FILE_NAME)

        if not os.path.exists(os.path.join(constants.OUTPUT_DIR_RELATIVE_PATH, constants.STATS_FILE_NAME)):
            self._ui_label_title = QLabel(constants.UI_NO_STATS_FILE)
            self._ui_load_button = QPushButton(constants.UI_STATS_BUTTON)
            self._ui_progress_bar = QProgressBar()

            self._ui_load_button.clicked.connect(self.on_load_button_clicked)

            layout_main.addWidget(self._ui_label_title)
            layout_main.addWidget(self._ui_load_button)
            layout_main.addWidget(self._ui_progress_bar)

        self.setLayout(layout_main)

    def on_load_button_clicked(self):
        print("a")

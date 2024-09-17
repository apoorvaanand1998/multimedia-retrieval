from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

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
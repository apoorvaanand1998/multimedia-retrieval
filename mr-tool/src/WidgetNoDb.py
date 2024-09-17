from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout


class WidgetNoDb(QWidget):
    _ui_layout_main: QVBoxLayout = None
    _ui_label_title: QLabel = None

    def __init__(self, db_name: str):
        super().__init__()

        self.db_name = db_name

        self._ui_layout_main = QVBoxLayout()

        self._ui_label_title = QLabel(self.db_name + " doesn't exist. Cannot generate stats")

        self._ui_layout_main.addWidget(self._ui_label_title)
        self.setLayout(self._ui_layout_main)

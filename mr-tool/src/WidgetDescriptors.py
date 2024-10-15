from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class WidgetDescriptors(QWidget):

    def __init__(self, db_map, db_name):
        super().__init__()

        self._ui_layout_main = QVBoxLayout()

        self._ui_layout_main.addWidget(QLabel("test"))

        self.setLayout(self._ui_layout_main)
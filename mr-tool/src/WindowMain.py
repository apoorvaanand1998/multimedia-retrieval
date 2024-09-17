from PyQt5.QtWidgets import QMainWindow, QTabWidget
from WindowDatabase import WindowDatabase
from WindowDatabaseStats import WindowDatabaseStats
import constants


class WindowMain(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(constants.UI_MAIN_APP_TITLE)

        central_widget = QTabWidget(self)
        central_widget.setTabPosition(QTabWidget.North)
        central_widget.setMouseTracking(False)

        central_widget.addTab(WindowDatabase(), "Database")
        central_widget.addTab(WindowDatabaseStats(), "Statistics")

        self.setCentralWidget(central_widget)


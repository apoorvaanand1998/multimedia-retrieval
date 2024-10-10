from PyQt5.QtWidgets import QMainWindow, QTabWidget
from WindowDatabase import WindowDatabase
from WindowDatabaseStats import WindowDatabaseStats
from WindowNormalization import WindowNormalization
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
        central_widget.addTab(WindowNormalization(), "Normalization")

        self.showMaximized()

        self.setCentralWidget(central_widget)


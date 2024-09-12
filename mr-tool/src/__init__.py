import sys
import MainWindow
from PyQt5.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)

    window = MainWindow.MainWindow()
    window.show()

    app.exec()


main()

import sys
from WindowMain import WindowMain
from PyQt5.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)

    window = WindowMain()
    window.show()

    app.exec()


main()

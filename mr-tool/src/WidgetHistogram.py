from PyQt5.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class WidgetHistogram(QWidget):
    _ui_layout_main: QVBoxLayout = None

    def __init__(self, hist_title: str, log_scale: bool, data: list[int], no_bins: int, min_val: int, max_val: int):
        super().__init__()
        self._ui_layout_main = QVBoxLayout()

        # Create a matplotlib figure
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        self._ui_layout_main.addWidget(self.canvas)

        self.setLayout(self._ui_layout_main)

        self.create_histogram(hist_title, log_scale, data, no_bins, min_val, max_val)

    def create_histogram(self, hist_title: str, log_scale: bool, data: list[int], no_bins: int, min_val: int,
                         max_val: int):
        ax = self.figure.add_subplot()

        # Clear previous plots
        ax.clear()

        # N is the count in each bin, bins is the lower-limit of the bin
        N, bins, patches = ax.hist(data, bins=no_bins, range=(min_val, max_val), log=log_scale)
        ax.set_title(hist_title)
        self.canvas.draw()

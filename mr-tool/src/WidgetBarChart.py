from PyQt5.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from vedo import Plotter
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class WidgetBarChart(QWidget):
    _ui_layout_main: QVBoxLayout = None
    _ui_vedo_widget: QVTKRenderWindowInteractor = None

    _vedo_plotter: Plotter = None

    def __init__(self, counts: list[int], class_labels: list[str], parent=None):
        super().__init__(parent)

        # Create a matplotlib figure
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Create a layout and add the canvas to the widget
        self._ui_layout_main = QVBoxLayout()
        self._ui_layout_main.addWidget(self.canvas)
        self.setLayout(self._ui_layout_main)

        # Call the method to draw the bar chart
        self.plot_bar_chart(counts, class_labels)

    def plot_bar_chart(self, counts: list[int], class_labels: list[str]):
        # Create an axis
        ax = self.figure.add_subplot(111)

        # Clear previous plots
        ax.clear()

        # Create the bar chart
        ax.bar(class_labels, counts)

        # Set labels and title
        ax.set_xlabel('Class')
        ax.set_ylabel('Count')
        ax.set_title('Class Item Distribution')

        # Redraw the canvas
        self.canvas.draw()

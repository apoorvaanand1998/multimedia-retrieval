from PyQt5.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class WidgetSimpleHist(QWidget):
    def __init__(self, c, bs, title, parent=None):
        super().__init__(parent)

        # Set up the layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a Matplotlib figure and canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Plot the histogram using bin data
        self.plot_histogram(c, bs, title)

    def plot_histogram(self, c, bs, title):
        # Clear the figure
        self.figure.clear()

        # Create a new Axes on the figure
        ax = self.figure.add_subplot(111)

        # Manually plot the histogram data using bar or step
        ax.step(bs[:-1], c, where='mid', color='blue')  # Using step plot for outline style

        # Customize the plot as needed
        ax.set_title(title)
        # ax.set_xlabel("Value")
        # ax.set_ylabel("Density")

        # Redraw the canvas
        self.canvas.draw()

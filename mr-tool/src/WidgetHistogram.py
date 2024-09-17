from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from vedo.pyplot import np, histogram
from vedo import Plotter, Line
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class WidgetHistogram(QWidget):
    _ui_layout_main: QVBoxLayout = None
    _ui_vedo_widget: QVTKRenderWindowInteractor = None

    _vedo_plotter: Plotter = None

    def __init__(self, data: list[int], no_bins: int):
        super().__init__()
        self._ui_layout_main = QVBoxLayout()

        self._ui_vedo_widget, self._vedo_plotter = self.ui_create_vedo_widget()
        self._vedo_plotter.show(self.create_histogram(data, no_bins))

        self._ui_layout_main.addWidget(self._ui_vedo_widget)

        self.setLayout(self._ui_layout_main)

    def create_histogram(self, data: list[int], no_bins: int):
        fig = histogram(
            data,
            bins=no_bins,
            xtitle="Classes",
            ytitle="Count",
        )

        return fig

    def ui_create_vedo_widget(self):
        # Create the VTK render window interactor (QVTKRenderWindowInteractor)
        vtk_widget = QVTKRenderWindowInteractor()

        # Create a vedo Plotter and link it to the VTK widget
        plotter = Plotter(qt_widget=vtk_widget, interactive=False)

        # Start the VTK interactor
        vtk_widget.GetRenderWindow().Render()
        plotter.interactor.Start()

        return vtk_widget, plotter

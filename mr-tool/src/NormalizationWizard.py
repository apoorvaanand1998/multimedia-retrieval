import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QCheckBox, QTabWidget, QHBoxLayout, QSlider, QPushButton, \
    QMainWindow
from IStepNormalization import IStepNormalization
from StepResample import StepResample
from StepTranslate import StepTranslate
from StepScale import StepScale
from StepAlignPCA import StepAlignPCA
from StepFlip import StepFlip
from Mesh import Mesh
from Widget3DPlot import Widget3DPlot


class NormalizationWizard:
    _original_mesh: Mesh = None
    _current_mesh: Mesh = None

    _steps: list[IStepNormalization] = None

    _ui_widget: QWidget = None

    _window: QMainWindow = None

    _s_resample = StepResample()
    _s_translate = StepTranslate()
    _s_scale = StepScale()
    _s_align = StepAlignPCA()
    _s_flip = StepFlip()

    def __init__(self, mesh: Mesh, window: QMainWindow):
        if mesh is not None:
            self._original_mesh = mesh
            self._current_mesh = mesh.__copy__()

        self._steps = [self._s_resample, self._s_translate, self._s_scale, self._s_align, self._s_flip]

        self._window = window

        self.update_ui()

    def get_current_mesh(self) -> Mesh:
        return self._current_mesh

    def reset(self, new_mesh: Mesh = None):
        if new_mesh is not None:
            self._original_mesh = new_mesh
            self._current_mesh = new_mesh.__copy__()

        self._current_mesh = self._original_mesh.__copy__() if self._original_mesh is not None else None

        self.update_ui()

    def on_subdivide_slider_changed(self, label, value, step):
        label.setText("Iterations: " + str(value))
        step._subdivide_iterations = value

    def on_decimate_slider_changed(self, label, value, step):
        float_value = value / 100
        label.setText("Fraction: " + str(float_value))
        step._decimate_fraction = float_value

    def on_reset_btn_clicked(self):
        self._current_mesh = self._original_mesh.__copy__()
        self.update_ui()

        self._window.update_3d_viewer()

    def on_apply_btn_clicked(self, step: IStepNormalization):
        self._current_mesh = step.apply(self._current_mesh)
        self.update_ui()

        self._window.update_3d_viewer()

    def on_align_pca_apply(self):
        self.on_apply_btn_clicked(self._s_align)

    def on_flip_apply(self):
        self.on_apply_btn_clicked(self._s_flip)

    def on_scale_apply(self):
        self.on_apply_btn_clicked(self._s_scale)

    def on_resample_apply(self):
        self.on_apply_btn_clicked(self._s_resample)

    def on_translate_apply(self):
        self.on_apply_btn_clicked(self._s_translate)

    def update_ui(self):
        self._ui_widget = QWidget()

        layout = QVBoxLayout(self._ui_widget)
        layout.setAlignment(Qt.AlignTop)

        if self._original_mesh is not None:
            for step in self._steps:
                if isinstance(step, StepAlignPCA):
                    layout_step = QVBoxLayout()
                    layout_step.addWidget(QLabel("Align PCA"))

                    button_reset = QPushButton("Reset")
                    button_reset.pressed.connect(self.on_reset_btn_clicked)
                    button_apply = QPushButton("Apply")
                    button_apply.pressed.connect(self.on_align_pca_apply)

                    layout_buttons = QHBoxLayout()
                    layout_buttons.addWidget(button_reset)
                    layout_buttons.addWidget(button_apply)

                    layout_step.addLayout(layout_buttons)

                    layout.addLayout(layout_step)
                if isinstance(step, StepFlip):
                    layout_step = QVBoxLayout()
                    layout_step.addWidget(QLabel("Flip according to PCA"))

                    button_reset = QPushButton("Reset")
                    button_reset.pressed.connect(self.on_reset_btn_clicked)
                    button_apply = QPushButton("Apply")
                    button_apply.pressed.connect(self.on_flip_apply)

                    layout_buttons = QHBoxLayout()
                    layout_buttons.addWidget(button_reset)
                    layout_buttons.addWidget(button_apply)

                    layout_step.addLayout(layout_buttons)

                    layout.addLayout(layout_step)

                if isinstance(step, StepResample):
                    layout_step = QVBoxLayout()
                    layout_step.addWidget(QLabel("Resampling"))

                    tab = QTabWidget()

                    subdivide = QWidget()
                    subdivide_layout = QHBoxLayout(subdivide)

                    subdivide_slider_label = QLabel("Iterations: 1")
                    subdivide_layout.addWidget(subdivide_slider_label)

                    subdivide_slider = QSlider(Qt.Horizontal)
                    subdivide_slider.setMaximum(10)
                    subdivide_slider.setMinimum(1)
                    subdivide_slider.setSingleStep(1)
                    subdivide_slider.valueChanged.connect(
                        lambda v: self.on_subdivide_slider_changed(subdivide_slider_label, v, step)
                    )
                    subdivide_layout.addWidget(subdivide_slider)
                    subdivide.setLayout(subdivide_layout)

                    decimate = QWidget()
                    decimate_layout = QHBoxLayout(decimate)
                    decimate_slider_label = QLabel("Fraction: 0.1")
                    decimate_layout.addWidget(decimate_slider_label)

                    decimate_slider = QSlider(Qt.Horizontal)
                    decimate_slider.setMaximum(100)
                    decimate_slider.setMinimum(1)
                    decimate_slider.setSingleStep(1)
                    decimate_slider.valueChanged.connect(
                        lambda v: self.on_decimate_slider_changed(decimate_slider_label, v, step)
                    )
                    decimate_layout.addWidget(decimate_slider)
                    decimate.setLayout(decimate_layout)

                    tab.addTab(subdivide, "Subdivide")
                    tab.addTab(decimate, "Decimate")
                    tab.currentChanged.connect(
                        lambda idx: step.set_mode(idx)
                    )

                    layout_step.addWidget(tab)

                    button_reset = QPushButton("Reset")
                    button_reset.pressed.connect(self.on_reset_btn_clicked)
                    button_apply = QPushButton("Apply")
                    button_apply.pressed.connect(self.on_resample_apply)

                    layout_buttons = QHBoxLayout()
                    layout_buttons.addWidget(button_reset)
                    layout_buttons.addWidget(button_apply)

                    layout_step.addLayout(layout_buttons)

                    layout.addLayout(layout_step)

                elif isinstance(step, StepTranslate):
                    layout_step = QVBoxLayout()
                    layout_step.addWidget(QLabel("Translation"))

                    layout_before_after = QHBoxLayout()

                    layout_before = QVBoxLayout()
                    plot_before = Widget3DPlot(
                        self._original_mesh.get_vertices().tolist(),
                        [self._original_mesh.get_barycenter().tolist()]
                    )
                    layout_before.addWidget(plot_before)
                    layout_before.addWidget(QLabel("Barycenter: " + str(self._original_mesh.get_barycenter())))

                    layout_before_after.addLayout(layout_before)

                    layout_after = QVBoxLayout()
                    # a = self._original_mesh.get_barycenter()
                    # b = self._current_mesh.get_barycenter()
                    if self._current_mesh is None or np.array_equal(self._current_mesh.get_barycenter(),
                                                                    self._original_mesh.get_barycenter()):
                        layout_after.addWidget(QLabel("Press apply to translate the vertices"))
                    else:
                        plot_after = Widget3DPlot(
                            self._current_mesh.get_vertices().tolist(),
                            [self._current_mesh.get_barycenter().tolist()]
                        )
                        layout_after.addWidget(plot_after)
                        layout_after.addWidget(QLabel("Barycenter: " + str(self._current_mesh.get_barycenter())))

                    layout_before_after.addLayout(layout_after)

                    layout_step.addLayout(layout_before_after)

                    button_reset = QPushButton("Reset")
                    button_reset.pressed.connect(self.on_reset_btn_clicked)
                    button_apply = QPushButton("Apply")
                    button_apply.pressed.connect(self.on_translate_apply)

                    layout_buttons = QHBoxLayout()
                    layout_buttons.addWidget(button_reset)
                    layout_buttons.addWidget(button_apply)

                    layout_step.addLayout(layout_buttons)

                    layout.addLayout(layout_step)

                elif isinstance(step, StepScale):
                    layout_step = QVBoxLayout()
                    layout_step.addWidget(QLabel("Scale to unit volume"))

                    layout_before_after = QHBoxLayout()

                    layout_before = QVBoxLayout()

                    layout_before.addWidget(
                        QLabel("Bounding Box Dimensions: " + str(self._original_mesh.get_bounding_box_dimensions()))
                    )
                    layout_before.addWidget(
                        QLabel("Volume: " + str(self._original_mesh.get_volume()))
                    )

                    layout_before_after.addLayout(layout_before)

                    layout_after = QVBoxLayout()

                    layout_after.addWidget(
                        QLabel("Bounding Box Dimensions: " + str(self._current_mesh.get_bounding_box_dimensions()))
                    )
                    layout_after.addWidget(
                        QLabel("Volume: " + str(self._current_mesh.get_volume()))
                    )

                    layout_before_after.addLayout(layout_after)

                    layout_step.addLayout(layout_before_after)

                    button_reset = QPushButton("Reset")
                    button_reset.pressed.connect(self.on_reset_btn_clicked)
                    button_apply = QPushButton("Apply")
                    button_apply.pressed.connect(self.on_scale_apply)

                    layout_buttons = QHBoxLayout()
                    layout_buttons.addWidget(button_reset)
                    layout_buttons.addWidget(button_apply)

                    layout_step.addLayout(layout_buttons)

                    layout.addLayout(layout_step)

        self._ui_widget.setLayout(layout)

    @property
    def ui_widget(self):
        return self._ui_widget

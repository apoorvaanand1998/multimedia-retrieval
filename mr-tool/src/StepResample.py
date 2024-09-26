from Mesh import Mesh
from IStepNormalization import IStepNormalization


class StepResample(IStepNormalization):
    _mode: int = 0  # 0 - Subdivide, 1 - Decimate
    _subdivide_iterations: int = 1
    _decimate_fraction: float = 0.9
    _decimate_desired_vertices: int = 100

    def __init__(self):
        super().__init__()

    def apply(self, mesh: Mesh) -> Mesh:
        # print("Step Resample:")
        # print("Mode: " + str(self._mode))
        # print("Subdivide Iterations: " + str(self._subdivide_iterations))
        # print("Decimate Fraction: " + str(self._decimate_fraction))

        if self._mode == 0:
            # Subdivide (Increase)
            mesh.subdivide(self._subdivide_iterations)
        elif self._mode == 1:
            mesh.decimate(self._decimate_fraction)
        elif self._mode == 2:
            mesh.decimate_target(self._decimate_desired_vertices)

        return mesh

    def set_mode(self, mode: int):
        self._mode = mode

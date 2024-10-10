from Mesh import Mesh
from IStepNormalization import IStepNormalization


class StepScale(IStepNormalization):

    def __init__(self):
        super().__init__()

    def apply(self, mesh: Mesh) -> Mesh:
        mesh.scale_to_unit_volume()
        return mesh

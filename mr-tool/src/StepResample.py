from Mesh import Mesh
from IStepNormalization import IStepNormalization


class StepResample(IStepNormalization):
    def __init__(self):
        super().__init__()

    def apply(self, mesh: Mesh):
        return mesh

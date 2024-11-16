from Mesh import Mesh
from IStepNormalization import IStepNormalization
from FINAL_normalization import flip_along_axes

class StepFlip(IStepNormalization):

    def __init__(self):
        super().__init__()

    def apply(self, mesh: Mesh) -> Mesh:
        flipped_mesh = flip_along_axes(mesh)
        return flipped_mesh
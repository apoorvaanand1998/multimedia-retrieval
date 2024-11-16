from Mesh import Mesh
from IStepNormalization import IStepNormalization
from FINAL_normalization import align_principal_axes


class StepAlignPCA(IStepNormalization):

    def __init__(self):
        super().__init__()

    def apply(self, mesh: Mesh) -> Mesh:
        aligned_mesh = align_principal_axes(mesh)
        return aligned_mesh

from Mesh import Mesh
from IStepNormalization import IStepNormalization


class StepTranslate(IStepNormalization):

    def __init__(self):
        super().__init__()

    def apply(self, mesh: Mesh) -> Mesh:
        mesh.translate_to_world_origin()
        return mesh

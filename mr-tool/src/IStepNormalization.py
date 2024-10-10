from PyQt5.QtWidgets import QVBoxLayout

from Mesh import Mesh


# Interface for normalization step
# A bit useless for Python, cuz it has dynamic methods
# Maybe delete later?
class IStepNormalization:
    def apply(self, mesh: Mesh) -> Mesh:
        return mesh

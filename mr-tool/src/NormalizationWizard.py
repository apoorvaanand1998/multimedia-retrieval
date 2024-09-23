from IStepNormalization import IStepNormalization
from Mesh import Mesh


class NormalizationWizard:
    _original_mesh: Mesh = None
    _steps: list[IStepNormalization] = None
    _steps_output: list[Mesh] = None
    _current_step_idx: int = None

    def __init__(self, mesh: Mesh, steps: list[IStepNormalization]):
        self.original_mesh = mesh
        self._steps = steps
        self._steps_output = []
        self._current_step_idx = 0

    def apply_next(self) -> Mesh:
        if self._current_step_idx >= len(self._steps):
            return self._original_mesh

        mesh = self._steps_output[self._current_step_idx] if self._current_step_idx > 0 else self._original_mesh
        step = self._steps[self._current_step_idx]
        self._current_step_idx += 1

        return step.apply(mesh)

    def reset(self):
        self._current_step_idx = 0

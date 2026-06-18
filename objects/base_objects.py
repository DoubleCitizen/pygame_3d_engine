import numpy as np

class BaseObjects3D:
    def __init__(self, color: np.ndarray):
        self._is_created = False
        self._color = color
        self._coords3d: list[np.ndarray] = []
        self._edges: tuple[tuple] = ()

    def get_edges(self) -> tuple[tuple]:
        return self._edges

    def get_color(self) -> np.ndarray:
        return self._color

    def get_pos3d(self) -> tuple[np.ndarray]:
        if not self._is_created:
            self._create()
            self._is_created = True
        return self._coords3d

    def _create(self):
        pass
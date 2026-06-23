import numpy as np
from objects.base_objects import BaseObjects3D

class Cube(BaseObjects3D):
    def __init__(self, color: np.ndarray, center: np.ndarray, radius: float):
        super().__init__(color)

        self._pos: np.ndarray = center
        self._radius: float = radius

    def _create(self):
        if not self._is_created:

            x0 = self._radius / np.sqrt(3)

            self._coords.append(np.array([-x0, -x0, -x0], dtype=float) + self._pos)
            self._coords.append(np.array([+x0, -x0, -x0], dtype=float) + self._pos)
            self._coords.append(np.array([-x0, +x0, -x0], dtype=float) + self._pos)
            self._coords.append(np.array([+x0, +x0, -x0], dtype=float) + self._pos)
            self._coords.append(np.array([-x0, -x0, +x0], dtype=float) + self._pos)
            self._coords.append(np.array([+x0, -x0, +x0], dtype=float) + self._pos)
            self._coords.append(np.array([-x0, +x0, +x0], dtype=float) + self._pos)
            self._coords.append(np.array([+x0, +x0, +x0], dtype=float) + self._pos)

            self._edges = ((0, 1), (1, 3), (3, 2), (0, 2), (4, 5), (5, 7), (7, 6), (4, 6), (0, 4), (1, 5), (2, 6), (3, 7))
            self._faces = (
                (0, 2, 3, 1), # Передняя (Z-)
                (4, 5, 7, 6), # Задняя (Z+)
                (0, 4, 6, 2), # Левая (X-)
                (1, 3, 7, 5), # Правая (X+)
                (0, 1, 5, 4), # Нижняя (Y-)
                (2, 6, 7, 3)  # Верхняя (Y+)
            )

            self._is_created = True
import numpy as np
import copy

class BaseObjects3D:
    def __init__(self, color: np.ndarray):
        self._is_created = False
        self._color = color
        self._coords3d: list[np.ndarray] = []
        self._coords3d_local: list[np.ndarray] = []
        self._coords4d: list[np.ndarray] = []
        self._coords4d_local: list[np.ndarray] = []
        self._edges: tuple[tuple] = ()
        self._faces: tuple[tuple] = ()
        self._yaw: float = 0
        self._pitch: float = 0
        self._roll: float = 0
        self._center: np.ndarray = 0

    def get_edges(self) -> tuple[tuple]:
        return self._edges
    
    def get_faces(self) -> tuple[tuple]:
        return self._faces

    def get_color(self) -> np.ndarray:
        return self._color
    
    def get_facets_normals(self) -> list[np.ndarray]:
        normals: list = []
        for face in self._faces:
            # ИСПРАВЛЕНО: Берем три разные последовательные вершины грани
            AB = self.get_pos3d()[face[1]] - self.get_pos3d()[face[0]]
            BC = self.get_pos3d()[face[2]] - self.get_pos3d()[face[1]]
            N = np.cross(AB, BC)
            normals.append(N)
        return normals

    def get_center(self) -> np.ndarray:
        return self._center

    def get_pos3d(self) -> list[np.ndarray]:
        if not self._is_created:
            self._create()
            if not self._coords3d_local:
                if len(self._coords3d) > 0:
                    self._coords3d_local = copy.deepcopy(self._coords3d) - self._center
            self._is_created = True
        return self._coords3d
    
    def get_pos4d(self) -> list[np.ndarray]:
        if not self._is_created:
            self._create()
        return self._coords4d

    def set_rotate(self, yaw, pitch, roll):
        self._yaw = yaw
        self._pitch = pitch
        self._roll = roll
        for i in range(len(self._coords3d_local)):
            X, Y, Z = self._coords3d_local[i]
            
            X_new = X * np.cos(yaw) - Z * np.sin(yaw)
            Z_new = X * np.sin(yaw) + Z * np.cos(yaw)
            X, Z = X_new, Z_new

            Y_new = Y * np.cos(pitch) - Z * np.sin(pitch)
            Z_new = Y * np.sin(pitch) + Z * np.cos(pitch)
            Y, Z = Y_new, Z_new

            Y_new = Y * np.cos(roll) - X * np.sin(roll)
            X_new = Y * np.sin(roll) + X * np.cos(roll)
            Y, X = Y_new, X_new

            Pworld_new = np.array([X, Y, Z], dtype=float) + self._center
            self._coords3d[i] = Pworld_new

    def rotate_in(self, yaw: float = 0, pitch: float = 0, roll: float = 0):
        self._yaw += yaw
        self._pitch += pitch
        self._roll += roll
        self.set_rotate(self._yaw, self._pitch, self._roll)

    def _create(self):
        pass
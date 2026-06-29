import numpy as np
import copy

class BaseObjects3D:
    def __init__(self, color: np.ndarray):
        self._is_created = False
        self._color = color
        self._coords: list[np.ndarray] = []
        self._coords_local: list[np.ndarray] = []
        self._edges: tuple[tuple] = ()
        self._faces: tuple[tuple] = ()
        self._yaw: float = 0
        self._pitch: float = 0
        self._roll: float = 0
        self._pos: np.ndarray = np.array([0, 0, 0], dtype=float)

    def get_edges(self) -> tuple[tuple]:
        return self._edges
    
    def get_faces(self) -> tuple[tuple]:
        return self._faces

    def get_color(self) -> np.ndarray:
        return self._color
    
    def get_facets_normals(self) -> list[np.ndarray]:
        normals: list = []
        for face in self._faces:
            AB = self.get_vertices()[face[1]] - self.get_vertices()[face[0]]
            BC = self.get_vertices()[face[2]] - self.get_vertices()[face[1]]
            N = np.cross(AB, BC)
            normals.append(N)
        return normals

    def get_pos(self) -> np.ndarray:
        return self._pos

    def get_vertices(self) -> list[np.ndarray]:
        if not self._is_created:
            self._create()
            if not self._coords_local:
                if len(self._coords) > 0:
                    self._coords_local = copy.deepcopy(self._coords) - self._pos
            self._is_created = True
        return self._coords

    def set_rotate(self, yaw, pitch, roll):
        self._yaw = yaw
        self._pitch = pitch
        self._roll = roll
        for i in range(len(self._coords_local)):
            X, Y, Z = self._coords_local[i]

            i_v = np.array([np.cos(yaw), np.sin(yaw)])
            j_v = np.array([-np.sin(yaw), np.cos(yaw)])
            X, Z = X * i_v + Z * j_v

            i_v = np.array([np.cos(pitch), np.sin(pitch)])
            j_v = np.array([-np.sin(pitch), np.cos(pitch)])
            Y, Z = Y * i_v + Z * j_v

            i_v = np.array([np.cos(roll), np.sin(roll)])
            j_v = np.array([-np.sin(roll), np.cos(roll)])
            Y, X = Y * i_v + X * j_v

            Pworld_new = np.array([X, Y, Z], dtype=float) + self._pos
            self._coords[i] = Pworld_new

    def rotate_in(self, yaw: float = 0, pitch: float = 0, roll: float = 0):
        self._yaw += yaw
        self._pitch += pitch
        self._roll += roll
        self.set_rotate(self._yaw, self._pitch, self._roll)

    def _create(self):
        pass
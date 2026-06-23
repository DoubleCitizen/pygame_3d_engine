from objects.base_objects import BaseObjects3D
import numpy as np
import copy

class Tesseract(BaseObjects3D):
    def __init__(self, color: np.ndarray, center4d: np.ndarray, radius: float):
        super().__init__(color)
        self._center4d: np.ndarray = center4d
        self._radius: float = radius
        # Заглушка для базового класса, чтобы не падал при проверках центра
        self._center = center4d[:3] 
        
        self._hyper_yaw: float = 0
        self._hyper_pitch: float = 0
        self._hyper_roll: float = 0

    def _create(self):
        if not self._is_created:
            x0 = self._radius / 2  # Честное 4D смещение вершин

            # Наполняем локальные 4D координаты (Вкруг нуля!)
            self._coords4d_local.append(np.array([-x0, -x0, -x0, -x0], dtype=float))
            self._coords4d_local.append(np.array([+x0, -x0, -x0, -x0], dtype=float))
            self._coords4d_local.append(np.array([-x0, +x0, -x0, -x0], dtype=float))
            self._coords4d_local.append(np.array([+x0, +x0, -x0, -x0], dtype=float))
            self._coords4d_local.append(np.array([-x0, -x0, +x0, -x0], dtype=float))
            self._coords4d_local.append(np.array([+x0, -x0, +x0, -x0], dtype=float))
            self._coords4d_local.append(np.array([-x0, +x0, +x0, -x0], dtype=float))
            self._coords4d_local.append(np.array([+x0, +x0, +x0, -x0], dtype=float))

            self._coords4d_local.append(np.array([-x0, -x0, -x0, +x0], dtype=float))
            self._coords4d_local.append(np.array([+x0, -x0, -x0, +x0], dtype=float))
            self._coords4d_local.append(np.array([-x0, +x0, -x0, +x0], dtype=float))
            self._coords4d_local.append(np.array([+x0, +x0, -x0, +x0], dtype=float))
            self._coords4d_local.append(np.array([-x0, -x0, +x0, +x0], dtype=float))
            self._coords4d_local.append(np.array([+x0, -x0, +x0, +x0], dtype=float))
            self._coords4d_local.append(np.array([-x0, +x0, +x0, +x0], dtype=float))
            self._coords4d_local.append(np.array([+x0, +x0, +x0, +x0], dtype=float))

            # Инициализируем списки мировых координат нужной длины
            
            self._coords3d = [np.zeros(3) for _ in range(16)]
            self._coords4d = [np.zeros(4) for _ in range(16)]

            # Твои идеальные ребра и грани
            self._edges = (
                (0, 1), (1, 3), (3, 2), (0, 2), (4, 5), (5, 7), (7, 6), (4, 6), (0, 4), (1, 5), (2, 6), (3, 7),
                (8, 9), (9, 11), (11, 10), (8, 10), (12, 13), (13, 15), (15, 14), (12, 14), (8, 12), (9, 13), (10, 14), (11, 15),
                (0, 8), (1, 9), (2, 10), (3, 11), (4, 12), (5, 13), (6, 14), (7, 15)
            )

            # self._faces = (
            #     (0, 1, 3, 2), (4, 5, 7, 6), (0, 4, 6, 2), (0, 1, 5, 4), (1, 5, 7, 3), (2, 3, 7, 6),
            #     (8, 9, 11, 10), (12, 13, 15, 14), (8, 12, 14, 10), (8, 9, 13, 12), (9, 13, 15, 11), (10, 11, 15, 14),
            #     (0, 1, 9, 8), (1, 3, 11, 9), (3, 2, 10, 11), (0, 2, 10, 8),
            #     (4, 5, 13, 12), (5, 7, 15, 13), (7, 6, 14, 15), (4, 6, 14, 12),
            #     (0, 4, 12, 8), (1, 5, 13, 9), (2, 6, 14, 10), (3, 7, 15, 11)
            # )
            self._is_created = True

    def get_pos3d(self) -> list[np.ndarray]:
        if not self._is_created:
            self._create()
        # Возвращаем актуальные спроецированные 3D точки, которые посчитал метод set_rotate
        return self._coords3d

    def set_rotate(self, yaw, pitch, roll, hyper_yaw=0, hyper_pitch=0, hyper_roll=0):
        self._yaw = yaw
        self._pitch = pitch
        self._roll = roll
        self._hyper_yaw = hyper_yaw
        self._hyper_pitch = hyper_pitch
        self._hyper_roll = hyper_roll

        D = 30.0          # Дистанция удаления в 4D мире
        focal_4d = 200.0  # Фокусное расстояние для 4D проекции

        for i in range(len(self._coords4d_local)):
            X, Y, Z, W = self._coords4d_local[i]  # ИСПРАВЛЕНО: Честная 4D распаковка

            # --- 3D ВРАЩЕНИЯ ---
            X_new = X * np.cos(yaw) - Z * np.sin(yaw)
            Z_new = X * np.sin(yaw) + Z * np.cos(yaw)
            X, Z = X_new, Z_new

            Y_new = Y * np.cos(pitch) - Z * np.sin(pitch)
            Z_new = Y * np.sin(pitch) + Z * np.cos(pitch)
            Y, Z = Y_new, Z_new

            Y_new = Y * np.cos(roll) - X * np.sin(roll)
            X_new = Y * np.sin(roll) + X * np.cos(roll)
            Y, X = Y_new, X_new

            # --- 4D ГИПЕР-ВРАЩЕНИЯ ---
            W_new = W * np.cos(hyper_yaw) - Z * np.sin(hyper_yaw)
            Z_new = W * np.sin(hyper_yaw) + Z * np.cos(hyper_yaw)
            W, Z = W_new, Z_new

            Y_new = Y * np.cos(hyper_pitch) - W * np.sin(hyper_pitch)
            W_new = Y * np.sin(hyper_pitch) + W * np.cos(hyper_pitch)
            Y, W = Y_new, W_new

            W_new = W * np.cos(hyper_roll) - X * np.sin(hyper_roll)
            X_new = W * np.sin(hyper_roll) + X * np.cos(hyper_roll)
            W, X = W_new, X_new

            # Перенос 4D точки в мировые координаты
            self._coords4d[i] = np.array([X, Y, Z, W], dtype=float) + self._center4d

            # --- ПЕРСПЕКТИВНАЯ ПРОЕКЦИЯ (4D -> 3D) ---
            # Сжимаем четвертое измерение W в привычное трехмерное пространство Z
            X_3d = (X * focal_4d) / (W + D)
            Y_3d = (Y * focal_4d) / (W + D)
            Z_3d = (Z * focal_4d) / (W + D)

            # Сохраняем результат + 3D центр объекта в мире
            self._coords3d[i] = np.array([X_3d, Y_3d, Z_3d], dtype=float) + self._center4d[:3]

    def rotate_in(self, yaw: float = 0, pitch: float = 0, roll: float = 0, hyper_yaw: float = 0, hyper_pitch: float = 0, hyper_roll: float = 0):
        self._yaw += yaw
        self._pitch += pitch
        self._roll += roll
        self._hyper_yaw += hyper_yaw
        self._hyper_pitch += hyper_pitch
        self._hyper_roll += hyper_roll
        self.set_rotate(self._yaw, self._pitch, self._roll, self._hyper_yaw, self._hyper_pitch, self._hyper_roll)
import numpy as np
import pygame

class Camera:
    def __init__(self, pos: np.ndarray = np.array([0.0, 0.0, 0.0], dtype=float), focal_length: float = 400.0):
        self.pos: np.ndarray = pos
        self.focal_length: float = focal_length
        
        # Углы поворота (накапливаем внутри класса)
        self.yaw: float = 0.0   # Влево-вправо
        self.pitch: float = 0.0 # Вверх-вниз

    def update(self):
        """Применяет скорость к виртуальной позиции камеры."""
        self.pos += self.velocity
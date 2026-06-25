import numpy as np
from objects.camera import Camera
from objects.base_objects import BaseObjects3D
import pygame
import time

class Player:
    def __init__(self, pos: np.ndarray, camera: Camera, yaw: float = 0, pitch: float = 0, objects: list[BaseObjects3D] = []):
        self._pos: np.ndarray = pos
        self._camera: Camera = camera
        self._yaw: float = yaw
        self._pitch: float = pitch
        self._mouse_sensitivity: float = 0.002
        self._speed: float = 0.1
        self._velocity: np.ndarray = np.array([0.0, 0.0, 0.0])
        self._gravity = 0.001
        self._is_mode_fly: bool = False
        self._is_falling: bool = False
        self._is_jump: bool = False
        self._time = time.time()
        self._jump_force = 0.01
        self._objects: list[BaseObjects3D] = objects

    def _physics_update(self):
        for object in self._objects:
            points: list = []
            if len(object._edges) == 0:
                continue
            for edge in object._edges:
                for i in edge:
                    points.append(object.get_vertices()[i])
            min_x, max_x = min(points, key=lambda x: x[0])[0], max(points, key=lambda x: x[0])[0]
            min_z, max_z = min(points, key=lambda x: x[2])[2], max(points, key=lambda x: x[2])[2]
            if max_x >= self._pos[0] >= min_x and max_z >= self._pos[2] >= min_z:
                if round(self._pos[1]) == round(points[0][1]):
                    self._is_falling = False
                    self._is_jump = False
                    if self._velocity[1] < 0:
                        self._velocity[1] = 0
                    self._time = time.time()
                    return
        self._velocity[1] -= self._gravity
        # self._pos += self._velocity
        self._is_jump = False
        self._is_falling = True

    def handle_input(self, keys, mouse_dx, mouse_dy):
        """Собирает ввод с мыши и клавиатуры и считает скорость движения."""
        # 1. Повороты от мыши
        self._yaw -= (self._mouse_sensitivity * mouse_dx)
        self._yaw %= 2 * np.pi
        
        self._pitch += (self._mouse_sensitivity * mouse_dy)
        self._pitch = max(-(np.pi/2), min(np.pi/2, self._pitch))

        # 2. Движение (Обнуляем скорость перед расчетом новых нажатий)
        if self._is_mode_fly:
            self._velocity = np.array([0.0, 0.0, 0.0])
        else:
            self._velocity = np.array([0.0, self._velocity[1], 0.0])

        # Вперед
        if keys[pygame.K_w]:
            self._velocity[0] -= self._speed * np.sin(self._yaw)
            self._velocity[2] += self._speed * np.cos(self._yaw)
            
        # Назад
        if keys[pygame.K_s]:
            self._velocity[0] += self._speed * np.sin(self._yaw)
            self._velocity[2] -= self._speed * np.cos(self._yaw)

        # Влево (стрейф)
        if keys[pygame.K_a]:
            self._velocity[0] -= self._speed * np.cos(self._yaw)
            self._velocity[2] -= self._speed * np.sin(self._yaw)
            
        # Вправо (стрейф)
        if keys[pygame.K_d]:
            self._velocity[0] += self._speed * np.cos(self._yaw)
            self._velocity[2] += self._speed * np.sin(self._yaw)
        # Вверх (Прыжок)
        if keys[pygame.K_SPACE] and not self._is_falling:
            self._is_jump = True
            self._velocity[1] += self._jump_force
            print(f"self._velocity[1] = {self._velocity[1]}")
            # self._velocity[1] += self._jump_length
        
        # Вниз (Присесть)
        if keys[pygame.K_LSHIFT]:
            self._velocity[1] -= self._speed

    def update(self):
        """Применяет скорость к виртуальной позиции камеры."""
        self._physics_update()
        self._pos += self._velocity
        self._camera.pos = self._pos + np.array([0, 0.5, 0], dtype=float)
        self._camera.pitch = self._pitch
        self._camera.yaw = self._yaw
        

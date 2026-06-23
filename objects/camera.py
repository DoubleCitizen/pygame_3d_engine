import numpy as np
import pygame

class Camera:
    def __init__(self, pos: np.ndarray = np.array([0.0, 0.0, 0.0], dtype=float), focal_length: float = 400.0):
        self.pos: np.ndarray = pos
        self.focal_length: float = focal_length
        
        # Углы поворота (накапливаем внутри класса)
        self.yaw: float = 0.0   # Влево-вправо
        self.pitch: float = 0.0 # Вверх-вниз
        
        # Настройки чувствительности и скорости
        self.mouse_sensitivity: float = 0.002
        self.speed: float = 0.1
        self.velocity: np.ndarray = np.array([0.0, 0.0, 0.0])

    def handle_input(self, keys, mouse_dx, mouse_dy):
        """Собирает ввод с мыши и клавиатуры и считает скорость движения."""
        # 1. Повороты от мыши
        self.yaw -= (self.mouse_sensitivity * mouse_dx)
        self.yaw %= 2 * np.pi
        
        self.pitch += (self.mouse_sensitivity * mouse_dy)
        self.pitch = max(-(np.pi/2), min(np.pi/2, self.pitch))

        # 2. Движение (Обнуляем скорость перед расчетом новых нажатий)
        self.velocity = np.array([0.0, 0.0, 0.0])

        # Вперед
        if keys[pygame.K_w]:
            self.velocity[0] -= self.speed * np.sin(self.yaw)
            self.velocity[2] += self.speed * np.cos(self.yaw)
            
        # Назад
        if keys[pygame.K_s]:
            self.velocity[0] += self.speed * np.sin(self.yaw)
            self.velocity[2] -= self.speed * np.cos(self.yaw)

        # Влево (стрейф)
        if keys[pygame.K_a]:
            self.velocity[0] -= self.speed * np.cos(self.yaw)
            self.velocity[2] -= self.speed * np.sin(self.yaw)
            
        # Вправо (стрейф)
        if keys[pygame.K_d]:
            self.velocity[0] += self.speed * np.cos(self.yaw)
            self.velocity[2] += self.speed * np.sin(self.yaw)

        # Вверх (Прыжок)
        if keys[pygame.K_SPACE]:
            self.velocity[1] += self.speed
        
        # Вниз (Присесть)
        if keys[pygame.K_LSHIFT]:
            self.velocity[1] -= self.speed

    def update(self):
        """Применяет скорость к виртуальной позиции камеры."""
        self.pos += self.velocity
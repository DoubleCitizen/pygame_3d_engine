import pygame
import sys
import camera
import numpy as np
import my_math
from objects.cube import Cube
from pygame_ext.renderer_3d import Renderer3D

# 1. Настройки окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FOCAL = 400
FPS = 60

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My 3D to 2D Renderer")
clock = pygame.time.Clock()

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Создаем шрифт для HUD (название системного шрифта, размер в пикселях)
hud_font = pygame.font.SysFont('Consolas', 18)

# # Точка прямо перед нами
# point_coords, _, visible = camera.project_3d_to_2d(np.array([0, 0, 15], dtype=float), FOCAL, SCREEN_WIDTH, SCREEN_HEIGHT)
# print(f"Пиксели: {point_coords}, Видна на экране: {visible}")

# # Точка прямо перед нами
# point_coords, _, visible = camera.project_3d_to_2d(np.array([10, 0, 15], dtype=float), FOCAL, SCREEN_WIDTH, SCREEN_HEIGHT)
# print(f"Пиксели: {point_coords}, Видна на экране: {visible}")

# # Точка прямо перед нами
# point_coords, _, visible = camera.project_3d_to_2d(np.array([0, 10, 15], dtype=float), FOCAL, SCREEN_WIDTH, SCREEN_HEIGHT)
# print(f"Пиксели: {point_coords}, Видна на экране: {visible}")

# point_coords, _, visible = camera.project_3d_to_2d(np.array([10, 10, 15], dtype=float), FOCAL, SCREEN_WIDTH, SCREEN_HEIGHT)
# print(f"Пиксели: {point_coords}, Видна на экране: {visible}")


# # Точка прямо перед нами
# point_coords, _, visible = camera.project_3d_to_2d(np.array([5, 5, 20], dtype=float), FOCAL, SCREEN_WIDTH, SCREEN_HEIGHT)
# print(f"Пиксели: {point_coords}, Видна на экране: {visible}")

# # Точка прямо перед нами
# point_coords, _, visible = camera.project_3d_to_2d(np.array([15, 5, 20], dtype=float), FOCAL, SCREEN_WIDTH, SCREEN_HEIGHT)
# print(f"Пиксели: {point_coords}, Видна на экране: {visible}")

# # Точка прямо перед нами
# point_coords, _, visible = camera.project_3d_to_2d(np.array([5, 15, 20], dtype=float), FOCAL, SCREEN_WIDTH, SCREEN_HEIGHT)
# print(f"Пиксели: {point_coords}, Видна на экране: {visible}")

# point_coords, _, visible = camera.project_3d_to_2d(np.array([15, 15, 20], dtype=float), FOCAL, SCREEN_WIDTH, SCREEN_HEIGHT)
# print(f"Пиксели: {point_coords}, Видна на экране: {visible}")


camera_pos = np.array([0,0,0], dtype=float)
camera_velocity = np.array([0.0, 0.0, 0.0])

speed = 0.1

pygame.mouse.set_visible(False)
# Захватываем мышь внутри окна (чтобы она не вылетала за пределы экрана)
pygame.event.set_grab(True)

# Углы поворота камеры (накапливаем их)
camera_yaw = 0.0   # Влево-вправо
camera_pitch = 0.0 # Вверх-вниз
mouse_sensitivity = 0.002 # Чувствительность мыши

# --- ВНУТРИ ГЛАВНОГО ЦИКЛА (вне блока for event) ---

# 1. Получаем смещение мыши с прошлого кадра (dx, dy)
# dx - движение по горизонтали, dy - по вертикали

cube1 = Cube(np.array([255, 255, 0]), np.array([-20, 0, 20], dtype=float), 10)
cube2 = Cube(np.array([255, 0, 255]), np.array([20, 0, 20], dtype=float), 10)

renderer_3d = Renderer3D(SCREEN_WIDTH, SCREEN_HEIGHT)
# Главный цикл
running = True
while running:
    # 2. Обработка событий (например, закрытие окна)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEWHEEL:
            FOCAL += event.y * 20
            if FOCAL < 0:
                FOCAL = 0

    keys = pygame.key.get_pressed()
    mouse_dx, mouse_dy = pygame.mouse.get_rel()
    # print(f"mouse_dx = {mouse_dx}")
    # print(f"mouse_dy = {mouse_dy}")
    # Обнуляем скорость каждый кадр
    camera_velocity = np.array([0.0, 0.0, 0.0])

    camera_yaw -= (mouse_sensitivity * mouse_dx)
    camera_yaw %= 2 * np.pi
    # camera_yaw = max(-(np.pi), min(np.pi, camera_yaw))
    camera_pitch += (mouse_sensitivity * mouse_dy)
    # camera_pitch %= 2 * np.pi
    camera_pitch = max(-(np.pi/2), min(np.pi/2, camera_pitch))



    # --- Ось Z (Вперед / Назад) ---
    # if keys[pygame.K_w]:
    #     X = speed * np.sin(camera_yaw)
    #     Z = speed * np.cos(camera_yaw)
    #     camera_velocity = np.array([X, 0, Z], dtype=float)
    #     # camera_velocity[2] = +speed      # Плюс Z
    # if keys[pygame.K_s]:
    #     X = speed * np.sin(camera_yaw)
    #     Z = speed * np.cos(camera_yaw)
    #     camera_velocity = np.array([-X, 0, -Z], dtype=float)
    #     # camera_velocity[2] = -speed     # Минус Z
    if keys[pygame.K_w]:
        camera_velocity[0] -= speed * np.sin(camera_yaw)
        camera_velocity[2] += speed * np.cos(camera_yaw)
        
    # Назад
    if keys[pygame.K_s]:
        camera_velocity[0] += speed * np.sin(camera_yaw)
        camera_velocity[2] -= speed * np.cos(camera_yaw)

    # Влево (стрейф)
    if keys[pygame.K_a]:
        camera_velocity[0] -= speed * np.cos(camera_yaw)
        camera_velocity[2] -= speed * np.sin(camera_yaw)
        
    # Вправо (стрейф)
    if keys[pygame.K_d]:
        camera_velocity[0] += speed * np.cos(camera_yaw)
        camera_velocity[2] += speed * np.sin(camera_yaw)

    if keys[pygame.K_SPACE]:
        camera_velocity[1] += speed
    
    if keys[pygame.K_LSHIFT]:
        camera_velocity[1] -= speed


    # # --- Ось X (Влево / Вправо) ---
    # if keys[pygame.K_a]:
    #     camera_velocity[0] = -speed      # Плюс X
    # if keys[pygame.K_d]:
    #     camera_velocity[0] = +speed     # Минус X

    # 3. Применяем итоговую скорость к координатам
    print(camera_pos)
    camera_pos += camera_velocity

    # 3. Очистка экрана (заливаем черным каждый кадр)
    screen.fill(BLACK)

    # ==========================================
    # ТУТ БУДЕТ ТВОЯ 3D МАТЕМАТИКА И ОТРИСОВКА
    # ==========================================
    
    # Пример отрисовки точки (круга): 
    # pygame.draw.circle(surface, color, (x, y), radius)
    # pygame.draw.circle(screen, GREEN, (400, 300), 5)
    
    # Пример отрисовки линии:
    # pygame.draw.line(surface, color, (x1, y1), (x2, y2), width)
    # pygame.draw.line(screen, WHITE, (100, 100), (200, 200), 2)

    # ==========================================
    # POINTS_COORDS1 += camera_velocity
    # POINTS_COORDS2 += camera_velocity
    # POINTS_COORDS3 += camera_velocity
    # POINTS_COORDS4 += camera_velocity
    # POINTS_COORDS5 += camera_velocity
    # POINTS_COORDS6 += camera_velocity
    # POINTS_COORDS7 += camera_velocity
    # POINTS_COORDS8 += camera_velocity
    renderer_3d.draw_object(cube1, screen, FOCAL, camera_pos, camera_yaw, camera_pitch)
    cube1.rotate_in(my_math.grad2rad(1))
    renderer_3d.draw_object(cube2, screen, FOCAL, camera_pos, camera_yaw, camera_pitch)
    cube2.rotate_in(0, my_math.grad2rad(1))

    fps_text = f"FPS: {int(clock.get_fps())}"
    camera_pos_text = f"camera_pos: {np.round(camera_pos, 2)}"
    camera_rotate_text = f"camera_yaw: {round(my_math.rad2grad(camera_yaw), 2)}° camera_pitch: {round(my_math.rad2grad(camera_pitch), 2)}°"
    focal_text = f"focal_lenght: {FOCAL}"

    fps_surface = hud_font.render(fps_text, True, WHITE)
    camera_pos_surface = hud_font.render(camera_pos_text, True, WHITE)
    camera_rotate_surface = hud_font.render(camera_rotate_text, True, WHITE)
    focal_surface = hud_font.render(focal_text, True, WHITE)

    screen.blit(fps_surface, (0, 20))
    screen.blit(camera_pos_surface, (0, 40))
    screen.blit(camera_rotate_surface, (0, 60))
    screen.blit(focal_surface, (0, 80))

    # 4. Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
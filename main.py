import pygame
import sys
import camera
import numpy as np

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

POINTS_COORDS1 = np.array([-5, -5, 15], dtype=float) # Передняя грань (Z=15)
POINTS_COORDS2 = np.array([ 5, -5, 15], dtype=float)
POINTS_COORDS3 = np.array([-5,  5, 15], dtype=float)
POINTS_COORDS4 = np.array([ 5,  5, 15], dtype=float)

POINTS_COORDS5 = np.array([-5, -5, 25], dtype=float) # Задняя грань (Z=25)
POINTS_COORDS6 = np.array([ 5, -5, 25], dtype=float)
POINTS_COORDS7 = np.array([-5,  5, 25], dtype=float)
POINTS_COORDS8 = np.array([ 5,  5, 25], dtype=float)

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




# Главный цикл
running = True
while running:
    # 2. Обработка событий (например, закрытие окна)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    mouse_dx, mouse_dy = pygame.mouse.get_rel()
    # print(f"mouse_dx = {mouse_dx}")
    # print(f"mouse_dy = {mouse_dy}")
    # Обнуляем скорость каждый кадр
    camera_velocity = np.array([0.0, 0.0, 0.0])

    camera_yaw -= mouse_sensitivity * mouse_dx
    camera_pitch += mouse_sensitivity * mouse_dy



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
    
    if keys[pygame.K_LCTRL]:
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
    point_coords1, _, visible = camera.project_3d_to_2d(POINTS_COORDS1, FOCAL, SCREEN_WIDTH, SCREEN_HEIGHT, camera_pos, camera_yaw, camera_pitch)
    point_coords2, _, visible = camera.project_3d_to_2d(POINTS_COORDS2, FOCAL, SCREEN_WIDTH, SCREEN_HEIGHT, camera_pos, camera_yaw, camera_pitch)
    point_coords3, _, visible = camera.project_3d_to_2d(POINTS_COORDS3, FOCAL, SCREEN_WIDTH, SCREEN_HEIGHT, camera_pos, camera_yaw, camera_pitch)
    point_coords4, _, visible = camera.project_3d_to_2d(POINTS_COORDS4, FOCAL, SCREEN_WIDTH, SCREEN_HEIGHT, camera_pos, camera_yaw, camera_pitch)
    point_coords5, _, visible = camera.project_3d_to_2d(POINTS_COORDS5, FOCAL, SCREEN_WIDTH, SCREEN_HEIGHT, camera_pos, camera_yaw, camera_pitch)
    point_coords6, _, visible = camera.project_3d_to_2d(POINTS_COORDS6, FOCAL, SCREEN_WIDTH, SCREEN_HEIGHT, camera_pos, camera_yaw, camera_pitch)
    point_coords7, _, visible = camera.project_3d_to_2d(POINTS_COORDS7, FOCAL, SCREEN_WIDTH, SCREEN_HEIGHT, camera_pos, camera_yaw, camera_pitch)
    point_coords8, _, visible = camera.project_3d_to_2d(POINTS_COORDS8, FOCAL, SCREEN_WIDTH, SCREEN_HEIGHT, camera_pos, camera_yaw, camera_pitch)
    # POINTS_COORDS1 += camera_velocity
    # POINTS_COORDS2 += camera_velocity
    # POINTS_COORDS3 += camera_velocity
    # POINTS_COORDS4 += camera_velocity
    # POINTS_COORDS5 += camera_velocity
    # POINTS_COORDS6 += camera_velocity
    # POINTS_COORDS7 += camera_velocity
    # POINTS_COORDS8 += camera_velocity

    

    if point_coords1 is not None and point_coords2 is not None:
        pygame.draw.line(screen, WHITE, point_coords1, point_coords2, 2)
    if point_coords2 is not None and point_coords4 is not None:
        pygame.draw.line(screen, WHITE, point_coords2, point_coords4, 2)
    if point_coords3 is not None and point_coords4 is not None:
        pygame.draw.line(screen, WHITE, point_coords3, point_coords4, 2)
    if point_coords1 is not None and point_coords3 is not None:
        pygame.draw.line(screen, WHITE, point_coords1, point_coords3, 2)

    if point_coords5 is not None and point_coords6 is not None:
        pygame.draw.line(screen, WHITE, point_coords5, point_coords6, 2)
    if point_coords6 is not None and point_coords8 is not None:
        pygame.draw.line(screen, WHITE, point_coords6, point_coords8, 2)
    if point_coords7 is not None and point_coords8 is not None:
        pygame.draw.line(screen, WHITE, point_coords7, point_coords8, 2)
    if point_coords5 is not None and point_coords7 is not None:
        pygame.draw.line(screen, WHITE, point_coords5, point_coords7, 2)

    if point_coords1 is not None and point_coords5 is not None:
        pygame.draw.line(screen, WHITE, point_coords1, point_coords5, 2)
    if point_coords2 is not None and point_coords6 is not None:
        pygame.draw.line(screen, WHITE, point_coords2, point_coords6, 2)
    if point_coords3 is not None and point_coords7 is not None:
        pygame.draw.line(screen, WHITE, point_coords3, point_coords7, 2)
    if point_coords4 is not None and point_coords8 is not None:
        pygame.draw.line(screen, WHITE, point_coords4, point_coords8, 2)

    

    # 4. Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
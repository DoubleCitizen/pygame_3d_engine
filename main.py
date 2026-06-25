import pygame
import sys
import numpy as np
import my_math
from objects.cube import Cube
from objects.camera import Camera
from objects.surface import Surface
from objects.tesseract import Tesseract
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

pygame.mouse.set_visible(False)
# Захватываем мышь внутри окна (чтобы она не вылетала за пределы экрана)
pygame.event.set_grab(True)

# Углы поворота камеры (накапливаем их)
# camera_yaw = 0.0   # Влево-вправо
# camera_pitch = 0.0 # Вверх-вниз
# mouse_sensitivity = 0.002 # Чувствительность мыши

# --- ВНУТРИ ГЛАВНОГО ЦИКЛА (вне блока for event) ---

# 1. Получаем смещение мыши с прошлого кадра (dx, dy)
# dx - движение по горизонтали, dy - по вертикали

cube1 = Cube(np.array([255, 255, 0]), np.array([-20, 0, 20], dtype=float), 10)
cube2 = Cube(np.array([255, 0, 255]), np.array([20, 0, 20], dtype=float), 10)
cube3 = Cube(np.array([35, 40, 255]), np.array([0, 0, 20], dtype=float), 10)
surface = Surface(np.array([35, 40, 80]), np.array([0, -5, 0], dtype=float), 50, 2)
tesseract = Tesseract(np.array([20, 255, 30]), np.array([0, 0, 120, 0], dtype=float), 5)

renderer_3d = Renderer3D(SCREEN_WIDTH, SCREEN_HEIGHT)
camera = Camera(pos=np.array([0.0, 0.0, 0.0], dtype=float), focal_length=400.0)
# Главный цикл
running = True
while running:
    # 2. Обработка событий (например, закрытие окна)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEWHEEL:
            camera.focal_length += event.y * 20
            if camera.focal_length < 0:
                camera.focal_length = 0

    # Получаем состояние клавиш и мыши
    keys = pygame.key.get_pressed()
    mouse_dx, mouse_dy = pygame.mouse.get_rel()

    # Передаем всё это камере — пускай сама разбирается!
    camera.handle_input(keys, mouse_dx, mouse_dy)
    camera.update()

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
    renderer_3d.add_queue_render_task(cube1, screen, FOCAL, camera.pos, camera.yaw, camera.pitch)
    cube1.rotate_in(my_math.grad2rad(1))
    renderer_3d.add_queue_render_task(cube2, screen, FOCAL, camera.pos, camera.yaw, camera.pitch)
    cube2.rotate_in(0, my_math.grad2rad(1))
    renderer_3d.add_queue_render_task(cube3, screen, FOCAL, camera.pos, camera.yaw, camera.pitch)
    cube3.rotate_in(0, 0, my_math.grad2rad(1))
    renderer_3d.add_queue_render_task(tesseract, screen, FOCAL, camera.pos, camera.yaw, camera.pitch)
    tesseract.rotate_in(hyper_yaw=0.01, hyper_roll=0.005)
    renderer_3d.add_queue_render_task(surface, screen, FOCAL, camera.pos, camera.yaw, camera.pitch)

    renderer_3d.draw_objects()

    fps_text = f"FPS: {int(clock.get_fps())}"
    camera_pos_text = f"camera_pos: {np.round(camera.pos, 2)}"
    camera_rotate_text = f"camera_yaw: {round(my_math.rad2grad(camera.yaw), 2)}° camera_pitch: {round(my_math.rad2grad(camera.pitch), 2)}°"
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
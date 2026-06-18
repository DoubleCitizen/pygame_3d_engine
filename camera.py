import numpy as np

from scipy.spatial.transform import Rotation as R

def project_3d_to_2d_scipy(XYZ: np.ndarray, focal_length, screen_width, screen_height, camera_pos: np.ndarray, angle_yaw: float = 0, angle_pitch: float = 0) -> tuple[None | np.ndarray, None | np.ndarray, bool]:
    # 1. СДВИГ: Вычитаем позицию камеры из координат точки мира
    relative_XYZ = XYZ - camera_pos

    # 2. ПОВОРОТ: Создаем объект поворота с помощью SciPy.
    # Мы говорим библиотеке: "Поверни сначала вокруг оси Y (yaw), а затем вокруг оси X (pitch)".
    # Буквы 'yx' задают порядок осей, а список углов — величину поворота (в радианах).
    # Знак минус нужен, так как при повороте камеры мир крутится в обратную сторону.
    camera_rotation = R.from_euler('yx', [angle_yaw, -angle_pitch])
    
    # Применяем созданный поворот напрямую к нашему 3D-вектору!
    # SciPy сам внутри перемножит нужные матрицы поворота
    X, Y, Z = camera_rotation.apply(relative_XYZ)

    # 3. ОТСЕЧЕНИЕ: Проверяем, не оказалась ли точка за спиной
    if Z <= 0:
        return None, np.array([X, Y, Z], dtype=float), False

    # 4. ПРОЕКЦИЯ (Pinhole деление на Z)
    x_proj = (X * focal_length) / Z
    y_proj = (Y * focal_length) / Z

    # 5. Экранные координаты (перенос в центр экрана)
    screen_x = screen_width / 2 + x_proj
    screen_y = screen_height / 2 - y_proj

    is_visible = (0 <= screen_x <= screen_width) and (0 <= screen_y <= screen_height)

    return np.array([screen_x, screen_y], dtype=float), np.array([X, Y, Z], dtype=float), is_visible

def project_3d_to_2d_linear(XYZ: np.ndarray, focal_length, screen_width, screen_height, camera_pos: np.ndarray, angle_yaw: float = 0, angle_pitch: float = 0) -> tuple[None | np.ndarray, None | np.ndarray, bool]:
    
    # 1. Вычитаем позицию камеры (делаем камеру центром мира)
    relative_XYZ = XYZ - camera_pos
    X, Y, Z = relative_XYZ

    # 2. Поворачиваем мир в противоположную сторону от взгляда мыши
    yaw = -angle_yaw
    pitch = -angle_pitch

    # Вращение влево-вправо
    X_new = X * np.cos(yaw) - Z * np.sin(yaw)
    Z_new = X * np.sin(yaw) + Z * np.cos(yaw)
    X, Z = X_new, Z_new

    # Вращение вверх-вниз
    Y_new = Y * np.cos(pitch) - Z * np.sin(pitch)
    Z_new = Y * np.sin(pitch) + Z * np.cos(pitch)
    Y, Z = Y_new, Z_new

    if Z <= 0:
        Z = 0.00000001
        return None, np.array([X, Y, Z], dtype=float), False

    x_proj: float = (X * focal_length) / Z
    y_proj: float = (Y * focal_length) / Z

    screen_x = screen_width / 2 + x_proj
    screen_y = screen_height / 2 - y_proj

    is_visible = (0 <= screen_x <= screen_width) and (0 <= screen_y <= screen_height)
    
    return np.array([screen_x, screen_y], dtype=float), np.array([X, Y, Z], dtype=float), is_visible

def project_3d_to_2d_matrix(XYZ: np.ndarray, focal_length, screen_width, screen_height, camera_pos: np.ndarray, angle_yaw: float = 0, angle_pitch: float = 0) -> tuple[None | np.ndarray, None | np.ndarray, bool]:
    # 1. Вычитаем позицию камеры (делаем камеру центром мира)
    relative_XYZ = XYZ - camera_pos
    X, Y, Z = relative_XYZ
    cx, cy, cz = camera_pos
    
    T = np.array([
        [1, 0, 0, -cx],
        [0, 1, 0, -cy],
        [0, 0, 1, -cz],
        [0, 0, 0, 1]
    ], dtype=float)

    R_yaw = np.array([
        [np.cos(angle_yaw), 0, np.sin(angle_yaw),     0],
        [0,                 1, 0,                       1],
        [-np.sin(angle_yaw),0, np.cos(angle_yaw),     0],
        [0                  ,0, 0,                      1]
    ], dtype=float)

    R_pitch = np.array([
        [1, 0,                    0,                     0],
        [0, np.cos(-angle_pitch), -np.sin(-angle_pitch), 0],
        [0, np.sin(-angle_pitch), np.cos(-angle_pitch),  0],
        [0, 0,                    0,                     1]
    ], dtype=float)

    f = focal_length
    P = np.array([
        [f, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0]
    ], dtype=float)

    VP = P @ R_pitch @ R_yaw @ T

    # Превращаем входную точку [X, Y, Z] в 4D-вектор [X, Y, Z, 1]
    point_4d = np.array([XYZ[0], XYZ[1], XYZ[2], 1.0], dtype=float)

    # Умножаем матрицу на точку
    projected_4d = VP @ point_4d

    # Извлекаем получившиеся компоненты
    X_clip, Y_clip, Z_clip, W_clip = projected_4d

    # Отсекаем всё, что за спиной (глубина W_clip, которая равна Z, должна быть больше нуля)
    if W_clip <= 0:
        return None, point_4d[:2], False

    # ПЕРСПЕКТИВНОЕ ДЕЛЕНИЕ (Делим X и Y на W_clip, то есть на глубину Z)
    x_proj = X_clip / W_clip
    y_proj = Y_clip / W_clip

    # Перенос в систему координат экрана
    screen_x = screen_width / 2 + x_proj
    screen_y = screen_height / 2 - y_proj

    is_visible = (0 <= screen_x <= screen_width) and (0 <= screen_y <= screen_height)

    return np.array([screen_x, screen_y], dtype=float), point_4d[:2], is_visible

WIDTH = 800
HEIGHT = 600
FOCAL = 400

# # Точка прямо перед нами
# point_coords, visible = project_3d_to_2d(np.array([0, 0, 15], dtype=float), FOCAL, WIDTH, HEIGHT)
# print(f"Пиксели: {point_coords}, Видна на экране: {visible}")

# # Точка прямо перед нами
# point_coords, visible = project_3d_to_2d(np.array([10, 0, 15], dtype=float), FOCAL, WIDTH, HEIGHT)
# print(f"Пиксели: {point_coords}, Видна на экране: {visible}")

# # Точка прямо перед нами
# point_coords, visible = project_3d_to_2d(np.array([0, 10, 15], dtype=float), FOCAL, WIDTH, HEIGHT)
# print(f"Пиксели: {point_coords}, Видна на экране: {visible}")

# point_coords, visible = project_3d_to_2d(np.array([10, 10, 15], dtype=float), FOCAL, WIDTH, HEIGHT)
# print(f"Пиксели: {point_coords}, Видна на экране: {visible}")


# # Точка прямо перед нами
# point_coords, visible = project_3d_to_2d(np.array([5, 5, 20], dtype=float), FOCAL, WIDTH, HEIGHT)
# print(f"Пиксели: {point_coords}, Видна на экране: {visible}")

# # Точка прямо перед нами
# point_coords, visible = project_3d_to_2d(np.array([15, 5, 20], dtype=float), FOCAL, WIDTH, HEIGHT)
# print(f"Пиксели: {point_coords}, Видна на экране: {visible}")

# # Точка прямо перед нами
# point_coords, visible = project_3d_to_2d(np.array([5, 15, 20], dtype=float), FOCAL, WIDTH, HEIGHT)
# print(f"Пиксели: {point_coords}, Видна на экране: {visible}")

# point_coords, visible = project_3d_to_2d(np.array([15, 15, 20], dtype=float), FOCAL, WIDTH, HEIGHT)
# print(f"Пиксели: {point_coords}, Видна на экране: {visible}")

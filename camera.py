import numpy as np

def project_3d_to_2d(XYZ: np.ndarray, focal_length, screen_width, screen_height, camera_pos: np.ndarray, angle_yaw: float = 0, angle_pitch: float = 0) -> tuple[None | np.ndarray, None | np.ndarray, bool]:
    
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

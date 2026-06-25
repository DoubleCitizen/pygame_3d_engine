import pygame
import numpy as np
import my_math
from objects.base_objects import BaseObjects3D
from camera import world_to_camera, camera_to_screen

NEAR = 0.1


def _clip_polygon(verts: list[np.ndarray]) -> list[np.ndarray]:
    result = []
    n = len(verts)
    for i in range(n):
        A = verts[i]
        B = verts[(i + 1) % n]
        a_inside = A[2] >= NEAR
        b_inside = B[2] >= NEAR

        if a_inside:
            result.append(A)

        if a_inside != b_inside:
            t = (NEAR - A[2]) / (B[2] - A[2])
            P = A + t * (B - A)
            result.append(P)

    return result


def _clip_line(A: np.ndarray, B: np.ndarray) -> tuple[np.ndarray | None, np.ndarray | None]:
    a_inside = A[2] >= NEAR
    b_inside = B[2] >= NEAR

    if not a_inside and not b_inside:
        return None, None

    if a_inside and b_inside:
        return A, B

    t = (NEAR - A[2]) / (B[2] - A[2])
    P = A + t * (B - A)
    return (A, P) if a_inside else (P, B)


class Renderer3D:
    def __init__(self, screen_width, screen_height):
        self._screen_width, self._screen_height = screen_width, screen_height
        self._queue_render_task: list = []

    def add_queue_render_task(self, obj: BaseObjects3D, screen, focal_lenght, camera_pos, angle_yaw, angle_pitch):
        self._queue_render_task.append((obj, screen, focal_lenght, camera_pos, angle_yaw, angle_pitch))

    def draw_objects(self):
        distances_and_id: list[list] = []
        for i, render_task in enumerate(self._queue_render_task):
            obj, screen, _, camera_pos, angle_yaw, angle_pitch = render_task
            distance = my_math.get_distance(obj.get_pos(), camera_pos)
            distances_and_id.append((i, distance))

        distances_and_id.sort(key=lambda x: x[1], reverse=True)

        for dist_id in distances_and_id:
            index, _ = dist_id
            obj, screen, focal, camera_pos, angle_yaw, angle_pitch = self._queue_render_task[index]

            # Шаг 1: переводим все вершины из мирового пространства в пространство камеры
            cam_coords = [
                world_to_camera(v, camera_pos, angle_yaw, angle_pitch)
                for v in obj.get_vertices()
            ]

            faces = obj.get_faces()
            edges = obj.get_edges()

            if faces:
                for face in faces:
                    # Шаг 2: собираем вершины грани в пространстве камеры
                    face_cam = [cam_coords[i] for i in face]

                    # Шаг 3: обрезаем грань по ближней плоскости
                    clipped = _clip_polygon(face_cam)
                    if len(clipped) < 3:
                        continue

                    # Шаг 4: проецируем обрезанные вершины на экран
                    screen_pts = [
                        camera_to_screen(c, focal, self._screen_width, self._screen_height)
                        for c in clipped
                    ]
                    pygame.draw.polygon(screen, obj.get_color(), screen_pts)
            else:
                for edge in edges:
                    A, B = _clip_line(cam_coords[edge[0]], cam_coords[edge[1]])
                    if A is None:
                        continue
                    s0 = camera_to_screen(A, focal, self._screen_width, self._screen_height)
                    s1 = camera_to_screen(B, focal, self._screen_width, self._screen_height)
                    pygame.draw.line(screen, obj.get_color(), s0, s1, 2)

        self._queue_render_task = []

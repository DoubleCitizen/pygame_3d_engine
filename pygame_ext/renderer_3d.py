import pygame
import numpy as np
import my_math
from objects.base_objects import BaseObjects3D
from camera import project_3d_to_2d_linear

class Renderer3D:
    def __init__(self, screen_width, screen_height):
        self._screen_width, self._screen_height = screen_width, screen_height
        self._queue_render_task: list = []

    def add_queue_render_task(self, obj: BaseObjects3D, screen, focal_lenght, camera_pos, angle_yaw, angle_pitch):
        self._queue_render_task.append((obj, screen, focal_lenght, camera_pos, angle_yaw, angle_pitch))

    def draw_objects(self):
        distances_and_id: list[list] = []
        for i, render_task in enumerate(self._queue_render_task):
            obj, screen, focal_lenght, camera_pos, angle_yaw, angle_pitch = render_task
            distance = my_math.get_distance(obj.get_center(), camera_pos)
            distances_and_id.append((i, distance))

        distances_and_id.sort(key=lambda x: x[1], reverse=True)

        for dist_id in distances_and_id:
            
            index, distance = dist_id

            obj, screen, focal_lenght, camera_pos, angle_yaw, angle_pitch = self._queue_render_task[index]

            points2d_coords = []
            point3d_coords = obj.get_pos3d()  # Тессеракт отдаст уже готовые 3D проекции!

            # Проецируем 3D точки на 2D экран камеры
            for point3d_coord in point3d_coords:
                proj_res = project_3d_to_2d_linear(point3d_coord, focal_lenght, self._screen_width, self._screen_height, camera_pos, angle_yaw, angle_pitch)
                points2d_coords.append(proj_res[0])

            faces = obj.get_faces()
            edges = obj.get_edges()
            normals = obj.get_facets_normals()

            # Отрисовка полигонов (если они есть)
            for face, edge, normal in zip(faces, edges, normals):
                p0 = points2d_coords[face[0]]
                p1 = points2d_coords[face[1]]
                p2 = points2d_coords[face[2]]

                # Проверяем, что все точки грани видны на экране
                if (p0 is not None and points2d_coords[face[1]] is not None and 
                    points2d_coords[face[2]] is not None and points2d_coords[face[3]] is not None):
                    
                    # Считаем два 2D-вектора прямо на плоскости экрана
                    # Вектор от первой точки ко второй
                    dx1 = p1[0] - p0[0]
                    dy1 = p1[1] - p0[1]
                    # Вектор от второй точки к третьей
                    dx2 = p2[0] - p1[1] # Опечатка у тебя в индексах face могла быть, берем p2 и p1
                    dx2 = p2[0] - p1[0]
                    dy2 = p2[1] - p1[1]

                    # Косое (векторное) произведение в 2D пространстве экрана
                    # Оно показывает направление закрутки вершин (Winding Order)
                    cross_2d = dx1 * dy2 - dy1 * dx2

                    # Если оно меньше нуля — грань повернута к нам лицевой стороной
                    # (Если куб исчезнет, а изнанка останется — просто поменяй знак на > 0)
                    if cross_2d < 0:
                        pygame.draw.polygon(screen, obj.get_color(), [
                            points2d_coords[face[0]], 
                            points2d_coords[face[1]], 
                            points2d_coords[face[2]], 
                            points2d_coords[face[3]]
                        ])
                # Если у объекта нет граней (только каркас), рисуем линиями
            if not faces:
                for edge in edges:
                    if points2d_coords[edge[0]] is not None and points2d_coords[edge[1]] is not None:
                        pygame.draw.line(screen, obj.get_color(), points2d_coords[edge[0]], points2d_coords[edge[1]], 2)

        self._queue_render_task = []
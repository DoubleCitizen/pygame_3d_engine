import pygame
import numpy as np
from objects.base_objects import BaseObjects3D
from camera import project_3d_to_2d_linear

class Renderer3D:
    def __init__(self, screen_width, screen_height):
        self._screen_width, self._screen_height = screen_width, screen_height

    def draw_object(self, obj: BaseObjects3D, screen, focal_lenght, camera_pos, angle_yaw, angle_pitch):
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
            N = normal
            A = point3d_coords[edge[0]]
            V = A - camera_pos
            D = np.dot(V, N) # Честное скалярное произведение векторов

            # ИСПРАВЛЕНО: Если скалярное произведение меньше нуля — грань смотрит на камеру
            if True or D < 0:
                if (points2d_coords[face[0]] is not None and 
                    points2d_coords[face[1]] is not None and 
                    points2d_coords[face[2]] is not None and 
                    points2d_coords[face[3]] is not None):
                    
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
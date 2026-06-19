import pygame
import numpy as np
import my_math
from objects.base_objects import BaseObjects3D
from objects.cube import Cube
from camera import project_3d_to_2d_linear

class Renderer3D:
    def __init__(self, screen_width, screen_height):
        self._screen_width, self._screen_height = screen_width, screen_height

    def draw_object(self, obj: BaseObjects3D, screen, focal_lenght, camera_pos, angle_yaw, angle_pitch):
        points2d_coords = []
        point3d_coords = obj.get_pos3d()
        for point3d_coord in point3d_coords:
            points2d_coords.append(project_3d_to_2d_linear(point3d_coord, focal_lenght, self._screen_width, self._screen_height, camera_pos, angle_yaw, angle_pitch)[0])

        faces = obj.get_faces()
        edges = obj.get_edges()
        normals = obj.get_facets_normals()
        # for edge, normal in zip(edges, normals):
        #     N = normal
        #     A = point3d_coords[edge[0]]
        #     V = A - camera_pos
        #     D = V @ N

        for face, edge, normal in zip(faces, edges, normals):
            N = normal
            A = point3d_coords[edge[0]]
            V = A - camera_pos
            D = V @ N
            if my_math.rad2grad(D) < 90:
                if points2d_coords[face[0]] is not None and points2d_coords[face[1]] is not None and points2d_coords[face[2]] is not None and points2d_coords[face[3]] is not None:
                    pygame.draw.polygon(screen, obj.get_color(), [points2d_coords[face[0]], points2d_coords[face[1]], points2d_coords[face[2]], points2d_coords[face[3]]])
            else:
                print("I not to draw plane!")
        if not faces:
            for edge in edges:
                if points2d_coords[edge[0]] is not None and points2d_coords[edge[1]] is not None:
                    pygame.draw.line(screen, obj.get_color(), points2d_coords[edge[0]], points2d_coords[edge[1]], 2)
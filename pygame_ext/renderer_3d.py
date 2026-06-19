import pygame
from objects.base_objects import BaseObjects3D
from objects.cube import Cube
from camera import project_3d_to_2d_linear

class Renderer3D:
    def __init__(self, screen_width, screen_height):
        self._screen_width, self._screen_height = screen_width, screen_height

    def draw_object(self, obj: BaseObjects3D, screen, focal_lenght, camera_pos, angle_yaw, angle_pitch):
        points2d_coords = []
        for point3d_coords in obj.get_pos3d():
            points2d_coords.append(project_3d_to_2d_linear(point3d_coords, focal_lenght, self._screen_width, self._screen_height, camera_pos, angle_yaw, angle_pitch)[0])

        for edge in obj.get_edges():
            if points2d_coords[edge[0]] is not None and points2d_coords[edge[1]] is not None:
                pygame.draw.line(screen, obj.get_color(), points2d_coords[edge[0]], points2d_coords[edge[1]], 2)
        for face in obj.get_faces():
            if points2d_coords[face[0]] is not None and points2d_coords[face[1]] is not None and points2d_coords[face[2]] is not None and points2d_coords[face[3]] is not None:
                pygame.draw.polygon(screen, obj.get_color(), [points2d_coords[face[0]], points2d_coords[face[1]], points2d_coords[face[2]], points2d_coords[face[3]]])
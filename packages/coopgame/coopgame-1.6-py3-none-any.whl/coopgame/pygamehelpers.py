import pygame
from coopstructs.geometry import Rectangle
from coopgame.colors import Color
from coopstructs.geometry.vectors.vectorN import Vector2, VectorN
import numpy as np
from typing import List, Dict, Tuple
import logging
from coopgame.label_drawing.pyLabel import TextAlignmentType
import cooptools.geometry_utils.vector_utils as vec
import cooptools.geometry.circles.utils as circ
import math
from cooptools.anchor import Anchor2D, CardinalPosition
from cooptools.matrixManipulation import point_transform_3d
from coopgame.pointdrawing.point_draw_utils import draw_points, DrawPointArgs

def mouse_pos() -> vec.FloatVec:
    return pygame.mouse.get_pos()

def mouse_pos_as_vector() -> Vector2:
    """ Get the global coords of the mouse position and convert them to a Vector2 object"""
    return Vector2(*mouse_pos())

def draw_box(surface: pygame.Surface,
             rect: Rectangle,
             color: Color = None,
             width: int = 0,
             outline_color: Color = None,
             anchor_draw_args: DrawPointArgs=None,
             corner_draw_args: DrawPointArgs=None
             ):

    if color:
        pygame.draw.rect(surface, color.value, (rect.TopLeft[0], rect.TopLeft[1], rect.width, rect.height), width)
    if outline_color:
        pygame.draw.rect(surface, outline_color.value, (rect.TopLeft[0], rect.TopLeft[1], rect.width, rect.height), 1)
    if anchor_draw_args:
        draw_points(
            surface=surface,
            points={rect.anchor.pos(): anchor_draw_args})
    if corner_draw_args:
        draw_points(
            surface=surface,
            points={x: corner_draw_args for x in rect.corner_generator()})

def draw_circle(surface: pygame.Surface,
                center: Vector2 | vec.FloatVec,
                radius: float,
                color: Color,
                width: int = 0,
                outline_color:Color = None):
    if type(center) == Vector2:
        center = center.as_tuple()

    pygame.draw.circle(surface, color.value, center=center, radius=radius, width=width)
    if outline_color:
        pygame.draw.circle(surface, outline_color.value, center=center, radius=radius, width=1)

def draw_polygon(surface: pygame.Surface,
                 points,
                 color: Color,
                 width: int = 0,
                 alpha: int = 255):
    if type(points[0]) in [VectorN, Vector2]:
        points = [point.as_tuple() for point in points]

    minx = min(point[0] for point in points)
    maxx = max(point[0] for point in points)
    miny = min(point[1] for point in points)
    maxy = max(point[1] for point in points)

    points = [(point[0] - minx, point[1] - miny) for point in points]

    s = pygame.Surface((int(maxx - minx), int(maxy - miny)), pygame.SRCALPHA)
    c_with_alpha = (color.value[0], color.value[1], color.value[2], alpha)
    pygame.draw.polygon(s, c_with_alpha, points, width)

    surface.blit(s, (minx, miny))

def draw_arrow(surface: pygame.Surface,
               start: vec.FloatVec,
               end: vec.FloatVec,
               color: Color,
               arrow_height: int = 5,
               leader_line_width: int = 1,
               leader_line: bool = False,
               arrow_width: int = 5):
    if leader_line:
        pygame.draw.line(surface, color.value, start, end, width=leader_line_width)

    if start == end:
        return

    arrow_points = [end, (end[0] - arrow_width / 2, end[1] - arrow_height), (end[0] + arrow_width / 2, (end[1] - arrow_height))]

    unit_backwards = vec.unit_vector(vec.vector_between(end, start))
    unit_backwards = (unit_backwards[0], -unit_backwards[1])  # negative to account for the pygame inverse Y-orientation
    unit_angle = circ.rads_between(unit_backwards)
    adjustment = - math.pi / 2
    rotation_angle = -(unit_angle + adjustment)  # negative to account for the pygame inverse Y-orientation

    rotated_points = []
    for point in arrow_points:
        rotated_points.append(circ.rotated_point(point, (end), rotation_angle))

    pygame.draw.polygon(surface, color.value, rotated_points)

def game_area_coords_from_parent_coords(parent_coords: Vector2, game_area_surface_rectangle: Rectangle) -> Vector2:
    """Converts Global Coords into coords on the game area"""
    return Vector2(parent_coords.x - game_area_surface_rectangle.x, parent_coords.y - game_area_surface_rectangle.y)


def scaled_points_of_a_rect(rect, draw_scale_matrix=None):
    ''' get the rectangle object representing the grid position that was input'''
    return point_transform_3d(
        rect.Corners,
        lh_matrix=draw_scale_matrix
    )

def scaled_points(points: List[Vector2], draw_scale_matrix=None):
    scaled = point_transform_3d([x.as_tuple() for x in points], lh_matrix=draw_scale_matrix)
    return [Vector2.from_tuple(point) for point in scaled]


def viewport_point_on_plane(viewport_point: Vector2, game_area_rect, draw_scale_matrix=None, margin: int = 1):
    points_on_plane = scaled_points_of_a_rect(game_area_rect, draw_scale_matrix)
    point0 = points_on_plane[0]
    point1 = points_on_plane[1]
    point2 = points_on_plane[2]

    vec1 = vec.vector_between(point1, point0)
    vec2 = vec.vector_between(point1, point2)

    normal = np.cross(vec1, vec2)
    a = normal[0]
    b = normal[1]
    c = normal[2]
    d = a * point0[0] + b * point0[1] + c * point0[2]

    z_val = (d - a * viewport_point.x - b * viewport_point.y) / c

    return (viewport_point.x, viewport_point.y, z_val)


def scaled_points_to_normal_points(points: List[Vector2], draw_scale_matrix=None):
    translated_points = [(point.x, point.y, 0, 1) for point in points]
    normal_array = scaled_array_to_normal_array(scaled_array=translated_points, draw_scale_matrix=draw_scale_matrix)
    normal_points = [Vector2(point[0], point[1]) for point in normal_array]

    return normal_points


def scaled_array_to_normal_array(scaled_array, draw_scale_matrix=None):
    if draw_scale_matrix is None:
        draw_scale_matrix = np.identity(4)

    draw_scale_matrix_inv = np.linalg.inv(draw_scale_matrix)
    normal_points = draw_scale_matrix_inv.dot(np.transpose(scaled_array))

    normal_points = np.reshape(normal_points, (-1, 2))

    return normal_points


def normal_points_to_scaled_points(points: List[Vector2], draw_scale_matrix=None):
    return scaled_points(points, draw_scale_matrix)


def mouse_in_plane_point(game_area_rect: Rectangle, draw_scale_matrix=None):
    # test = draw_scale_matrix_inv.dot(draw_scale_matrix)
    """Gets the mouse position and converts it to a grid position"""
    mouse_game_area_coord = game_area_coords_from_parent_coords(parent_coords=mouse_pos_as_vector(),
                                                                game_area_surface_rectangle=game_area_rect)
    mouse_plane_point = viewport_point_on_plane(mouse_game_area_coord, game_area_rect, draw_scale_matrix, margin=1)

    return mouse_plane_point


def normal_mouse_position(game_area_rect: Rectangle, draw_scale_matrix=None) -> Vector2:
    # test = draw_scale_matrix_inv.dot(draw_scale_matrix)
    """Gets the mouse position and converts it to a grid position"""
    # mouse_game_area_coord = game_area_coords_from_parent_coords(parent_coords=mouse_pos_as_vector(), game_area_surface_rectangle=game_area_rect)
    mouse_plane_point = mouse_in_plane_point(game_area_rect, draw_scale_matrix)
    points = np.array([mouse_plane_point[0], mouse_plane_point[1], mouse_plane_point[2], 1])

    normal_array = scaled_array_to_normal_array(points, draw_scale_matrix)

    return Vector2(normal_array[0][0], normal_array[0][1])


# def draw_text(text: str,
#               hud: pygame.Surface,
#               font: pygame.font.Font = None,
#               offset_rect: Rectangle = None,
#               color: Color = None,
#               alignment: TextAlignmentType = None,
#               alpha: float = None):
#     if font is None:
#         font = pygame.font.Font(None, 20)
#
#     if offset_rect is None:
#         offset_rect = Rectangle(anchor=Anchor2D(pt=(0, hud.get_height() - 50),
#                                                 dims=(hud.get_width(), 20),
#                                                 cardinality=CardinalPosition.BOTTOM_LEFT,
#                                                 inverted_y=True))
#
#     if color is None:
#         color = Color.BLUE
#
#     if alignment is None:
#         alignment = TextAlignmentType.TOPLEFT
#
#     rendered_txt = font.render(text, True, color.value)
#
#     if alpha:
#         rendered_txt.set_alpha(alpha * 100)
#
#     try:
#         rect = rendered_txt.get_rect()
#         align_coords = alignment_coords_for_type_rect(alignment, offset_rect)
#         setattr(rect, alignment.value, align_coords)
#         hud.blit(rendered_txt, rect)
#     except Exception as e:
#         logging.error(f"{e}")
#
# def alignment_coords_for_type_rect(alignment: TextAlignmentType, rect: Rectangle) -> Tuple[float, float]:
#     """
#     Note the orientation shift from top to bottom bc of the pygame inversion
#     """
#     switch = {
#         TextAlignmentType.TOPRIGHT:      lambda: rect.BottomRight,
#         TextAlignmentType.TOPLEFT:       lambda: rect.BottomLeft,
#         TextAlignmentType.TOPCENTER:     lambda: rect.BottomCenter,
#         TextAlignmentType.BOTTOMLEFT:    lambda: rect.TopLeft,
#         TextAlignmentType.BOTTOMRIGHT:   lambda: rect.TopRight,
#         TextAlignmentType.RIGHTCENTER:   lambda: rect.RightCenter,
#         TextAlignmentType.BOTTOMCENTER:  lambda: rect.TopCenter,
#         TextAlignmentType.LEFTCENTER:    lambda: rect.LeftCenter,
#         TextAlignmentType.CENTER:        lambda: rect.Center
#     }
#
#     return switch.get(alignment)()


def draw_dict(dict_to_draw: Dict,
              surface: pygame.Surface,
              total_game_time_sec: float,
              font: pygame.font.SysFont = None,
              offset_rectangle: Rectangle = None,
              g_offset: int = 0,
              font_color: Color = None,
              title: str = None):

    if font is None:
        font = pygame.font.SysFont(None, 18)

    if font_color is None:
        font_color = Color.LEMON_CHIFFON

    tracked_time = [(key, val) for key, val in dict_to_draw.items()]
    tracked_time.sort(key=lambda x: x[1], reverse=True)

    txt_lmbda = lambda key, val: f"{key}: {round(val, 2)} sec ({round(val / total_game_time_sec * 100, 1)}%)"

    if offset_rectangle is None:
        max_wid = max(font.size(txt_lmbda(key, val))[0] for key, val in tracked_time)
        offset_rectangle = Rectangle.from_tuple((0, 0, max_wid, font.get_height() + 3))

    y_off = offset_rectangle.y + g_offset
    offset_rectangle.y = y_off
    draw_text(title, surface, color=font_color,
              offset_rect=offset_rectangle, font=font)
    y_off += font.get_height() + 3
    for key, val in tracked_time:
        offset_rectangle.y = y_off
        draw_text(txt_lmbda(key, val), surface, color=font_color,
                       offset_rect=offset_rectangle, font=font, alignment=TextAlignmentType.TOPRIGHT)
        y_off += font.get_height() + 3

    return y_off

# def draw_fps(hud: pygame.Surface,
#              fps: float,
#              font: pygame.font.Font = None,
#              offset_rect: Rectangle = None,
#              color: Color = None,
#              alignment: TextAlignmentType = None):
#     txt = f"FPS: {int(fps)}"
#     draw_text(txt, hud=hud, font=font, offset_rect=offset_rect, color=color, alignment=alignment)

# def draw_mouse_coord(hud: pygame.Surface, font: pygame.font.Font = None, offset_rect: Rectangle = None,
#                      color: Color = None, alignment: TextAlignmentType = None):
#     mouse_pos = mouse_pos_as_vector()
#     txt = f"M:<{int(mouse_pos.x)}, {int(mouse_pos.y)}>"
#     draw_text(txt, hud=hud, font=font, offset_rect=offset_rect, color=color, alignment=alignment)
#
# def draw_game_time(hud: pygame.Surface,
#                    game_time_s: float,
#                    font: pygame.font.Font = None,
#                    offset_rect: Rectangle = None,
#                    color: Color = None,
#                    alignment: TextAlignmentType = None):
#     hrs = int(game_time_s / 3600)
#     min = int((game_time_s - hrs * 3600) / 60)
#     s = round(game_time_s - hrs * 3600 - min * 60, 2)
#     txt = f"GameTime: {hrs} hrs, {min} min, {s} sec"
#     draw_text(txt, hud=hud, font=font, offset_rect=offset_rect, color=color, alignment=alignment)

def calculate_fps(frame_times: List):
    avg_sec_per_frame = sum(frame_times) / len(frame_times) / 1000.0
    fps = 1 / avg_sec_per_frame if avg_sec_per_frame > 0 else 0
    return fps

def init_surface(dims):
    surface = pygame.Surface(dims).convert()
    surface.set_colorkey(Color.BLACK.value)
    return surface

def draw_mouse_pos(args: DrawPointArgs,
                   screen: pygame.Surface):
    draw_points(
        {tuple(int(x) for x in mouse_pos()): args},
        surface=screen,
    )

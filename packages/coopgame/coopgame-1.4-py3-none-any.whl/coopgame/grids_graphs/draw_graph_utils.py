from coopgame.colors import Color
import pygame
from coopgraph.graphs import Graph
from coopstructs.geometry.vectors.vectorN import Vector2
from coopstructs.geometry import Rectangle
import coopgame.pygamehelpers as help
from typing import Callable, Tuple, Dict, Iterable
from coopstructs.geometry.curves.curves import LineCurve, Curve
from cooptools.coopEnum import Directionality
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class GraphDrawArgs:
    coordinate_converter: Callable[[Vector2], Vector2] = None,
    node_color: Color = None,
    node_radius: int = None,
    enabled_edge_color: Color = None,
    disabled_edge_color: Color = None,
    draw_scale_matrix: np.ndarray = None,
    node_label_color: Color = None,
    edge_label_color: Color = None,
    draw_label_font: pygame.font.Font = None,
    articulation_points_color: Color = None,
    directionality_indicators_color: Color = None
    directionality_indicators_size: int = 10

    def with_(self, **kwargs):
        definition = self.__dict__
        for kwarg, val in kwargs.items():
            definition[kwarg] = val

        return type(self)(**definition)

def draw_to_surface(surface: pygame.Surface,
                    graph: Graph,
                    coordinate_converter: Callable[[Vector2], Vector2] = None,
                    node_color: Color = None,
                    node_radius: int = None,
                    enabled_edge_color: Color = None,
                    disabled_edge_color: Color = None,
                    draw_scale_matrix=None,
                    node_label_color: Color = None,
                    edge_label_color: Color = None,
                    draw_label_font: pygame.font.Font = None,
                    articulation_points_color: Color = None,
                    directionality_indicators_color: Color = None,
                    directionality_indicator_size: int = None):
    if not coordinate_converter:
        coordinate_converter = lambda x: x

    if enabled_edge_color or disabled_edge_color or edge_label_color:
        draw_graph_edges(surface,
                               graph=graph,
                               coordinate_converter=coordinate_converter,
                               enabled_color=enabled_edge_color,
                               disabled_color=disabled_edge_color,
                               draw_scale_matrix=draw_scale_matrix,
                               draw_label_color=edge_label_color,
                               draw_label_font=draw_label_font)

    if node_color or node_label_color:
        draw_graph_nodes(surface,
                              graph=graph,
                              coordinate_converter=coordinate_converter,
                              color=node_color,
                              draw_scale_matrix=draw_scale_matrix,
                              draw_label_color=node_label_color,
                              draw_label_font=draw_label_font,
                              radius=node_radius)

    if articulation_points_color:
        draw_articulation_points(surface,
                                      graph,
                                      articulation_points_color,
                                      draw_scale_matrix=draw_scale_matrix)

    if directionality_indicators_color:
        curves = [
            LineCurve(Vector2.from_vectorN(x.start.pos),
                      Vector2.from_vectorN(x.end.pos)) for x in graph.edges
        ]

        draw_directionality_indicators(
            surface=surface,
            curves={x: Directionality.FOREWARD for x in curves},
            indicator_color=directionality_indicators_color,
            size=directionality_indicator_size,
            draw_scale_matrix=draw_scale_matrix
        )

def draw_graph_edges(surface: pygame.Surface,
                      graph: Graph,
                      coordinate_converter: Callable[[Vector2], Vector2] = None,
                      enabled_color: Color = None,
                      disabled_color: Color = None,
                      draw_scale_matrix=None,
                      draw_label_color: Color = None,
                      draw_label_font: pygame.font.Font = None,
                      label_offset: Tuple[int, int] = None,
                      arrow_size: int = 5
                      ):

    if not coordinate_converter:
        coordinate_converter = lambda x: x

    if draw_label_color:
        draw_label_font = draw_label_font if draw_label_font is not None else pygame.font.Font(None, 25)
        label_offset = label_offset if label_offset is not None else (0, 0)

    for edge in graph.edges:
        start = coordinate_converter(edge.start.pos)
        end = coordinate_converter(edge.end.pos)

        width = 3 if graph.edge_between(edge.end, edge.start) is not None else 1

        scaled_pos = help.scaled_points_of_points([start, end], draw_scale_matrix=draw_scale_matrix)
        color = enabled_color if edge.enabled() else disabled_color

        if color:
            help.draw_arrow(surface=surface,
                            color=color,
                            start=(scaled_pos[0][0], scaled_pos[0][1]),
                            end=(scaled_pos[1][0], scaled_pos[1][1]),
                            arrow_height=arrow_size,
                            leader_line_width=width)

        if draw_label_color is not None:
            mid = ((scaled_pos[0][0] + scaled_pos[1][0]) / 2, (scaled_pos[0][1] + scaled_pos[1][1]) / 2)
            help.draw_text(str(edge), surface, draw_label_font,
                           offset_rect=Rectangle.from_tuple((mid[0] + label_offset[0], mid[1] + label_offset[1], 100, 100)),
                           color=draw_label_color)



def draw_graph_nodes(surface: pygame.Surface,
                     graph: Graph,
                     coordinate_converter: Callable[[Vector2], Vector2] = None,
                     color: Color = None,
                     radius: int = None,
                     width: int = None,
                     draw_scale_matrix=None,
                     draw_label_color: Color = None,
                     draw_label_font: pygame.font.Font = None,
                     label_offset: Tuple[int, int] = None):
    if not coordinate_converter:
        coordinate_converter = lambda x: x

    txt_dict = {}
    for node in graph.nodes:
        position = coordinate_converter(node.pos)
        scaled_pos = help.scaled_points([position], draw_scale_matrix=draw_scale_matrix)
        position = (int(scaled_pos[0].x), int(scaled_pos[0].y))

        if color:
            radius = radius if radius is not None else 1
            width = width if width is not None else 0
            pygame.draw.circle(surface, color.value, position, radius, width)

        txt_dict.setdefault(scaled_pos[0], []).append(node.name)

    if draw_label_color is not None:
        draw_label_font = draw_label_font if draw_label_font is not None else pygame.font.Font(None, 25)
        label_offset = label_offset if label_offset is not None else (10, 10)

        for pos, labels in txt_dict.items():
            help.draw_text(",".join(labels), surface, draw_label_font,
                           offset_rect=Rectangle.from_tuple((pos.x + label_offset[0], pos.y + label_offset[1], 100, 100)),
                           color=draw_label_color)


def draw_articulation_points(surface: pygame.Surface,
                             graph: Graph,
                             color: Color = None,
                             draw_scale_matrix=None
                             ):
    if graph is None:
        return

    articulation_points = graph.AP()

    if color is None:
        color = Color.ORANGE

    scaled_pos = help.scaled_points([node.pos for node in articulation_points.keys()],
                                    draw_scale_matrix=draw_scale_matrix)

    for point in scaled_pos:
        pygame.draw.circle(surface, color.value, (int(point.x), int(point.y)), 10, 1)

def draw_directionality_indicators(curves: Dict[Curve, Directionality],
                                    surface: pygame.Surface,
                                    indicator_color: Color,
                                    num_arrows: int = 5,
                                    size: float = 1,
                                    indicator_points_color: Color | Tuple[Color, ...]=None,
                                    draw_scale_matrix=None):
    arrow_ts = [1.0 / (num_arrows - 1) * x for x in range(0, num_arrows)] if num_arrows > 1 else [0.5]


    for curve, direction in curves.items():
        for t in arrow_ts:
            centre = curve.point_at_t(t)

            try:
                # get derivative of curve for drawing
                derivative = curve.derivative_at_t(t)
                d_unit = derivative.unit()
            except:
                # most likely a vertical curve (no derivative), handle by pointing up or down.
                d_unit = (curve.EndPoint - curve.origin).unit()

            if d_unit is None or d_unit.y == 0:
                continue

            d_foreward = d_unit.scaled_to_length(size)
            d_ort_1 = Vector2(1, - d_unit.x / d_unit.y).scaled_to_length(size / 2)
            # d_ort_2 = d_ort_1 * -1

            a = b = c = d = e = f = None
            if direction in [Directionality.FOREWARD, Directionality.BIDIRECTIONAL]:
                a = centre
                b = centre - d_foreward + d_ort_1
                c = centre - d_foreward - d_ort_1

                scaled_polygon_points = help.scaled_points([a, b, c], draw_scale_matrix)

                help.draw_polygon(surface, scaled_polygon_points, color=indicator_color)

            if direction in [Directionality.BACKWARD, Directionality.BIDIRECTIONAL]:
                d = centre
                e = centre + d_foreward + d_ort_1
                f = centre + d_foreward - d_ort_1
                scaled_polygon_points = help.scaled_points([d, e, f], draw_scale_matrix)

                help.draw_polygon(surface, scaled_polygon_points, color=indicator_color)

            if indicator_points_color:
                points = [a, b, c, d, e, f]
                if type(indicator_points_color) == Tuple:
                    points = [(x, indicator_points_color[ii % len(indicator_points_color)]) for ii, x in enumerate(points)]
                else:
                    points = [(x, indicator_points_color) for x in points]

                draw_points(
                    surface=surface,
                    points=points,
                    draw_scale_matrix=draw_scale_matrix
                )

def draw_points(surface: pygame.Surface,
                 points: Iterable[Tuple[Vector2, Color]],
                 draw_scale_matrix=None):
    points = [e for e in points]

    scaled_points = help.scaled_points([x[0] for x in points], draw_scale_matrix)
    for ii in range(len(points)):
        scaled_points = (scaled_points[ii], points[1])

    for point, color in scaled_points:
        if point is not None:
            pygame.draw.circle(surface, color.value, (int(point.x), int(point.y)), 2)
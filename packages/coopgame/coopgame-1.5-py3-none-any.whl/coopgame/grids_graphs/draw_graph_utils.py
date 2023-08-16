from coopgame.colors import Color
import pygame
from coopgraph.graphs import Graph, Edge
from coopstructs.geometry.vectors.vectorN import Vector2
from coopstructs.geometry import Rectangle
import coopgame.pygamehelpers as help
from typing import Callable, Tuple, Dict, Iterable
from coopstructs.geometry.curves.curves import LineCurve, Curve
from cooptools.coopEnum import Directionality
from dataclasses import dataclass, asdict
import numpy as np
from coopgame.pointdrawing import point_draw_utils as putils
from coopgame.label_drawing import label_drawing_utils as lutils
from coopgame.linedrawing import line_draw_utils as nutils
from coopstructs.geometry.lines import Line
from cooptools.matrixManipulation import point_transform_3d
from cooptools.common import flattened_list_of_lists

@dataclass(frozen=True)
class GraphDrawArgs:
    coordinate_converter: Callable[[Vector2], Vector2] = None
    node_color: Color = None
    node_radius: int = None
    enabled_edge_args: nutils.DrawLineArgs = None
    disabled_edge_args: nutils.DrawLineArgs = None
    draw_scale_matrix: np.ndarray = None
    node_label_color: Color = None
    draw_label_font: pygame.font.Font = None
    articulation_points_color: Color = None

    def with_(self, **kwargs):
        definition = self.__dict__
        for kwarg, val in kwargs.items():
            definition[kwarg] = val

        return type(self)(**definition)

    @classmethod
    def from_(cls, args, **kwargs):
        kw = asdict(args)
        kw.update(kwargs)
        return GraphDrawArgs(**kw)

    @property
    def EdgesBaseArgs(self):
        return GraphDrawArgs(
            coordinate_converter=self.coordinate_converter,
            draw_scale_matrix=self.draw_scale_matrix,
            enabled_edge_args=self.enabled_edge_args.BaseArgs,
            disabled_edge_args=self.disabled_edge_args.BaseArgs
        )

    @property
    def EdgesLabelArgs(self):
        return GraphDrawArgs(
            coordinate_converter=self.coordinate_converter,
            draw_scale_matrix=self.draw_scale_matrix,
            enabled_edge_args=self.enabled_edge_args.LabelArgs,
            disabled_edge_args=self.disabled_edge_args.LabelArgs
        )

    @property
    def NodesBaseArgs(self):
        return GraphDrawArgs(
            coordinate_converter=self.coordinate_converter,
            draw_scale_matrix=self.draw_scale_matrix,
            node_color=self.node_color,
            node_radius=self.node_radius
        )

    @property
    def NodesLabelArgs(self):
        return GraphDrawArgs(
            coordinate_converter=self.coordinate_converter,
            draw_scale_matrix=self.draw_scale_matrix,
            node_label_color=self.node_label_color
        )

    @property
    def OverlayArgs(self):
        return GraphDrawArgs(
            coordinate_converter=self.coordinate_converter,
            draw_scale_matrix=self.draw_scale_matrix,
            articulation_points_color=self.articulation_points_color
        )

def draw_to_surface(surface: pygame.Surface,
                    graph: Graph,
                    args: GraphDrawArgs):
    if graph is None:
        return

    if args.enabled_edge_args or args.disabled_edge_args:
        _draw_edges(
            surface=surface,
            edge_draw_args={
                e: args.enabled_edge_args if e.enabled() else args.disabled_edge_args for e in graph.edges
            },
            draw_scale_matrix=args.draw_scale_matrix,
            coordinate_converter=args.coordinate_converter
        )

    if args.node_color or args.node_label_color:
        draw_graph_nodes(surface,
                              graph=graph,
                              coordinate_converter=args.coordinate_converter,
                              color=args.node_color,
                              draw_scale_matrix=args.draw_scale_matrix,
                              draw_label_color=args.node_label_color,
                              draw_label_font=args.draw_label_font,
                              radius=args.node_radius)

    # if args.articulation_points_color:
    #     draw_articulation_points(surface,
    #                                   graph,
    #                                   args.articulation_points_color,
    #                                   draw_scale_matrix=args.draw_scale_matrix)


def _draw_edges(
    surface: pygame.Surface,
    edge_draw_args: Dict[Edge, nutils.DrawLineArgs],
    coordinate_converter: Callable[[Vector2], Vector2] = None,
    draw_scale_matrix=None
):
    if not coordinate_converter:
        coordinate_converter = lambda x: x

    line_args = {Line(coordinate_converter(Vector2.from_tuple(k.start.pos)),
                      coordinate_converter(Vector2.from_tuple(k.end.pos))): v.with_(label_text=str(k))
                 for k, v in edge_draw_args.items()}

    nutils.draw_lines(lines=line_args,
                      surface=surface,
                      draw_scale_matrix=draw_scale_matrix,
                      )

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
        position = coordinate_converter(Vector2.from_tuple(node.pos)).as_tuple()
        scaled_pos = point_transform_3d([position], lh_matrix=draw_scale_matrix)
        position = (int(scaled_pos[0][0]), int(scaled_pos[0][1]))

        if color:
            radius = radius if radius is not None else 1
            width = width if width is not None else 0
            pygame.draw.circle(surface, color.value, position, radius, width)

        txt_dict.setdefault(scaled_pos[0], []).append(node.name)

    if draw_label_color is not None:
        draw_label_font = draw_label_font if draw_label_font is not None else pygame.font.Font(None, 25)
        label_offset = label_offset if label_offset is not None else (10, 10)

        for pos, labels in txt_dict.items():
            lutils.draw_label(
                hud=surface,
                args=lutils.DrawLabelArgs(
                    color=draw_label_color,
                    font=draw_label_font,
                    offset=label_offset
                ),
                pos=pos,
                text=",".join(labels)
            )


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

            ip_color_getter = lambda ii: indicator_points_color[ii % len(indicator_points_color)] \
                if type(indicator_points_color) == tuple \
                else indicator_points_color

            if indicator_points_color:
                points = [a, b, c, d, e, f]
                putils.draw_points(
                    points={
                        x.as_tuple(): putils.DrawPointArgs(
                            color=ip_color_getter,
                            outline_color=None,
                            radius=2
                        ) for ii, x in enumerate(points)
                    },
                    surface=surface,
                    draw_scale_matrix=draw_scale_matrix
                )
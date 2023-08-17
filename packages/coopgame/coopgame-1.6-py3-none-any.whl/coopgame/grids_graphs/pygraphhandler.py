from coopgame.colors import Color
import pygame
from coopgraph.graphs import Graph
import coopgame.pygamehelpers as help
from typing import List
import coopgame.grids_graphs.draw_graph_utils as utils
import coopgame.linedrawing.line_draw_utils as lutils
import coopgame.label_drawing.label_drawing_utils as labutils
from cooptools.coopEnum import CoopEnum
from coopgame.surfaceManager import SurfaceManager, SurfaceDrawCallback
import coopgame.pointdrawing.point_draw_utils as putils

class GraphSurfaceType(CoopEnum):
    EDGES_SURFACE_ID = 'EDGES_SURFACE_ID'
    NODES_SURFACE_ID = 'NODES_SURFACE_ID'
    NODE_LABELS_SURFACE_ID = 'NODE_LABELS_SURFACE_ID'
    EDGE_LABELS_SURFACE_ID = 'EDGE_LABELS_SURFACE_ID'
    OVERLAY_SURFACE_ID = 'OVERLAY_SURFACE_ID'

DEFAULT_DRAW_CONFIG = utils.GraphDrawArgs(
            coordinate_converter= lambda x: x,
            node_draw_args=putils.DrawPointArgs(
                color=Color.DARK_BLUE,
                radius=5,
            ),
            enabled_edge_args=lutils.DrawLineArgs(
                color=Color.ORANGE,
                directionality_draw_args=lutils.DirectionalityIndicatorDrawArgs(
                    color=Color.ORANGE,
                    height=10,
                    width=10
                ),
                draw_label_args=labutils.DrawLabelArgs(
                    color=Color.WHEAT
                )
            ),
            disabled_edge_args=lutils.DrawLineArgs(
                color=Color.BROWN,
                directionality_draw_args=lutils.DirectionalityIndicatorDrawArgs(
                    color=Color.BROWN,
                    height=10,
                    width=10
                ),
                draw_label_args=labutils.DrawLabelArgs(
                    color=Color.BROWN
                )
            ),
            node_label_args=labutils.DrawLabelArgs(
                color=Color.WHEAT
            ),
            articulation_points_args=putils.DrawPointArgs(
                outline_color=Color.PURPLE,
                radius=10,
                outline_width=3
            ),
            sink_node_args=putils.DrawPointArgs(
                color=Color.RED,
                radius=10
            ),
            source_node_args=putils.DrawPointArgs(
                color=Color.GREEN,
                radius=10
            ),
            orphan_node_args=putils.DrawPointArgs(
                outline_color=Color.RED,
                radius=10
            )
        )


class PyGraphHandler:
    def __init__(self,
                 screen: pygame.Surface,
                 graph: Graph,
                 draw_config: utils.GraphDrawArgs = None):
        self.parent_screen = screen
        self.graph = graph
        self._draw_config: utils.GraphDrawArgs = draw_config if draw_config else DEFAULT_DRAW_CONFIG

        self.surface_manager = SurfaceManager(
            surface_draw_callbacks=[
                SurfaceDrawCallback(GraphSurfaceType.EDGES_SURFACE_ID.value, self.redraw_edges_surface),
                SurfaceDrawCallback(GraphSurfaceType.NODES_SURFACE_ID.value, self.redraw_nodes_surface),
                SurfaceDrawCallback(GraphSurfaceType.EDGE_LABELS_SURFACE_ID.value, self.redraw_edge_labels_surface),
                SurfaceDrawCallback(GraphSurfaceType.NODE_LABELS_SURFACE_ID.value, self.redraw_node_labels_surface),
                SurfaceDrawCallback(GraphSurfaceType.OVERLAY_SURFACE_ID.value, self.redraw_overlay_surface),
            ]
        )

    def set_config(self,
                   draw_config: utils.GraphDrawArgs):
        self._draw_config = draw_config

    def redraw_edges_surface(self):
        surf = help.init_surface(self.parent_screen.get_size())
        utils.draw_to_surface(
            surface=surf,
            graph=self.graph,
            args=self._draw_config.EdgesBaseArgs
        )
        return surf

    def redraw_nodes_surface(self):
        surf = help.init_surface(self.parent_screen.get_size())
        utils.draw_to_surface(
            surface=surf,
            graph=self.graph,
            args=self._draw_config.NodesBaseArgs
        )
        return surf

    def redraw_node_labels_surface(self):
        surf = help.init_surface(self.parent_screen.get_size())
        utils.draw_to_surface(
            surface=surf,
            graph=self.graph,
            args=self._draw_config.NodesLabelArgs
        )
        return surf

    def redraw_edge_labels_surface(self):
        surf = help.init_surface(self.parent_screen.get_size())
        utils.draw_to_surface(
            surface=surf,
            graph=self.graph,
            args=self._draw_config.EdgesLabelArgs
        )
        return surf

    def redraw_overlay_surface(self):
        surf = help.init_surface(self.parent_screen.get_size())
        utils.draw_to_surface(
            surface=surf,
            graph=self.graph,
            args=self._draw_config.OverlayArgs
        )
        return surf

    def update(self):
        # No surfaces require redrawing every iteration
        pass

    def invalidate(self):
        self.redraw()

    def redraw(self):
        self.surface_manager.redraw([x.name for x in GraphSurfaceType])

    def render(self,
               surface: pygame.Surface):
        self.update()
        self.surface_manager.render(surface)

    def toggle_surface(self, graphSurfaceTypes: List[GraphSurfaceType]):
        self.surface_manager.toggle_visible([x.value for x in graphSurfaceTypes])

    def show_all(self):
        self.surface_manager.show_all()

    def hide_all(self):
        self.surface_manager.hide_all()

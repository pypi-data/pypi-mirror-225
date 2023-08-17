from cooptools.sectors.grids import RectGrid
from coopstructs.geometry import Rectangle
from typing import  Callable, List, Tuple, Dict, Any
import coopgame.pygamehelpers as help
from coopstructs.geometry.vectors.vectorN import Vector2
import coopgame.grids_graphs.draw_grid_utils as utils
from cooptools.coopEnum import CoopEnum
from cooptools.colors import Color
from coopgame.surfaceManager import SurfaceManager, SurfaceDrawCallback
import pygame

class GridSurfaceType(CoopEnum):
    GRID_SURFACE_ID = 'GRID_SURFACE_ID'
    HIGHLIGHTS_SURFACE_ID = 'HIGHLIGHTS_SURFACE_ID'

GetMouseColorCallback = Callable[[], Color]
PosColorCallback = Callable[[], Dict[Vector2, Color]]
IdxColorCallback = Callable[[], Dict[int, Color]]
AreaRectCallback = Callable[[], Rectangle]
GridProvider = Callable[[], RectGrid]
KeyColorCallback = Callable[[], Dict[str, Color]]
HoverGridChangedCallback = Callable[[Vector2, Vector2], Any]

DEFAULT_DRAW_CONFIG = utils.GridDrawArgs(
            grid_draw_type = utils.GridDrawType.LINES,
            grid_color = Color.CHARCOAL,
            margin = 0,
            draw_scale_matrix = None,
            center_guide_color = Color.DARK_GREY,
            hover_color=Color.YELLOW,
            crosshairs_color=Color.DARK_CYAN
        )

class PyGridHandler:

    def __init__(self,
                 screen: pygame.Surface,
                 grid_provider: GridProvider,
                 get_game_area_rect_callback: AreaRectCallback,
                 get_highlights_callback: PosColorCallback = None,
                 get_outlined_callback: PosColorCallback = None,
                 get_highlighted_rows: IdxColorCallback = None,
                 get_highlighted_cols: IdxColorCallback = None,
                 get_toggled_key_colors: KeyColorCallback = None,
                 draw_config: utils.GridDrawArgs = None,
                 hover_changed_callback: HoverGridChangedCallback = None
                 ):
        super().__init__()
        self.hover_grid_pos = None

        self.parent_screen = screen
        self.grid_provider = grid_provider
        self._get_game_area_rect_callback = get_game_area_rect_callback
        self._get_highlights_callback = get_highlights_callback if get_highlights_callback else lambda: {}
        self._get_outlined_callback = get_outlined_callback if get_outlined_callback else lambda: {}
        self._get_highlighted_rows = get_highlighted_rows if get_highlighted_rows else lambda: {}
        self._get_highlighted_cols = get_highlighted_cols if get_highlighted_cols else lambda: {}
        self._get_toggled_key_colors = get_toggled_key_colors if get_toggled_key_colors else lambda: {}
        self._hover_changed_callback = hover_changed_callback

        self._draw_config: utils.GridDrawArgs = draw_config if draw_config else DEFAULT_DRAW_CONFIG

        self.surface_manager = SurfaceManager(
            surface_draw_callbacks=[
                SurfaceDrawCallback(GridSurfaceType.GRID_SURFACE_ID.value, self._get_grid_surface),
                SurfaceDrawCallback(GridSurfaceType.HIGHLIGHTS_SURFACE_ID.value, self._get_grid_overlay),
            ]
        )

        self._mouse_hover_grid_pos = None

    @property
    def MouseHoverGridPos(self) -> Vector2:
        return self._mouse_hover_grid_pos

    def handle_hover(self):
        mouse_gp = self.mouse_grid_pos()

        if mouse_gp != self._mouse_hover_grid_pos and self._hover_changed_callback:
            self._hover_changed_callback(self._mouse_hover_grid_pos, mouse_gp)
        self._mouse_hover_grid_pos = mouse_gp

    def update(self):
        self.handle_hover()

        self.surface_manager.update_if_visible([
            GridSurfaceType.HIGHLIGHTS_SURFACE_ID.value
        ])

    def invalidate(self):
        self.redraw()

    def redraw(self):
        self.surface_manager.redraw([x.value for x in GridSurfaceType])

    def render(self,
               surface: pygame.Surface):
        self.update()
        self.surface_manager.render(surface)

    def _get_grid_surface(self):
        surf = help.init_surface(self.parent_screen.get_size())
        utils.draw_to_surface(
            surface=surf,
            grid=self.grid_provider(),
            grid_draw_type=self._draw_config.grid_draw_type,
            grid_color=self._draw_config.grid_color,
            margin=self._draw_config.margin,
            draw_scale_matrix=self._draw_config.draw_scale_matrix,
            center_guide_color=self._draw_config.center_guide_color,
            toggled_key_colors=self._get_toggled_key_colors()
        )
        return surf

    def _get_grid_overlay(self):
        surf = help.init_surface(self.parent_screen.get_size())

        hover = (self._mouse_hover_grid_pos, self._draw_config.hover_color)
        if hover[0] == None:
            hover = None

        utils.draw_to_surface(
            surface=surf,
            grid=self.grid_provider(),
            draw_scale_matrix=self._draw_config.draw_scale_matrix,
            highlights=self._get_highlights_callback(),
            hover=hover,
            outlined_grid_cells=self._get_outlined_callback(),
            highlight_rows=self._get_highlighted_rows(),
            highlight_cols=self._get_highlighted_cols(),
            crosshairs_color=self._draw_config.crosshairs_color
        )

        return surf

    def mouse_grid_pos(self) -> Vector2:
        mse = help.mouse_pos_as_vector()
        mouse_gpo = Vector2.from_tuple(utils.get_mouse_grid_pos(mouse_pos=mse,
                                                                 game_area_rect= self._get_game_area_rect_callback(),
                                                                 draw_scale_matrix=None,
                                                                 grid=self.grid_provider()))
        return mouse_gpo


    def toggle_surface(self, gridSurfaceTypes: List[GridSurfaceType]):
        self.surface_manager.toggle_visible([x.value for x in gridSurfaceTypes])

    def show_all(self):
        self.surface_manager.show_all()

    def hide_all(self):
        self.surface_manager.hide_all()

if __name__ == "__main__":
    grid = RectGrid(10, 10)
    grid_pos = Vector2(5, 9)
    game_area_rect = Rectangle.from_tuple((0, 0, 1500, 2000))

    grid_handler = PyGridHandler()
    grid_def = grid_handler.grid_pos_definition(grid, grid_pos, game_area_rect)

    print(grid_def)
    print(grid_def.center)


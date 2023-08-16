from cooptools.matrixManipulation import point_transform_3d, scaled_array
from coopstructs.geometry import Line
import pygame
import numpy as np
from typing import List, Dict
from dataclasses import dataclass, asdict
from cooptools.colors import Color
import coopgame.pointdrawing.point_draw_utils as putils
import coopgame.label_drawing.label_drawing_utils as lutils
from cooptools.coopEnum import Directionality
import coopgame.pygamehelpers as help
from cooptools.coopEnum import CoopEnum, auto
from cooptools.common import property_name

class DirectionalityIndicatorType(CoopEnum):
    ALONG = auto()
    END = auto()

@dataclass(frozen=True)
class DirectionalityIndicatorDrawArgs:
    color: Color = None
    height: int = 10
    width: int = 10
    direction: Directionality = None

@dataclass(frozen=True)
class DrawLineArgs:
    color: Color = None
    width: int = None
    control_point_args: putils.DrawPointArgs = None
    directionality_draw_args: DirectionalityIndicatorDrawArgs = None
    draw_label_args: lutils.DrawLabelArgs = None
    label_text: str = None

    def __post_init__(self):
        if type(self.draw_label_args) == dict:
            object.__setattr__(self, 'draw_label_args', lutils.DrawLabelArgs(**self.draw_label_args))
        if type(self.control_point_args) == dict:
            object.__setattr__(self, 'control_point_args', putils.DrawPointArgs(**self.control_point_args))
        if type(self.directionality_draw_args) == dict:
            object.__setattr__(self, 'directionality_draw_args', DirectionalityIndicatorDrawArgs(**self.directionality_draw_args))

    def with_(self, **kwargs):
        kw = asdict(self)
        kw.update(kwargs)
        return DrawLineArgs(**kw)

    @property
    def BaseArgs(self):
        return DrawLineArgs(
            color=self.color,
            width=self.width,
            directionality_draw_args = self.directionality_draw_args,
        )

    @property
    def LabelArgs(self):
        return DrawLineArgs(
            draw_label_args=self.draw_label_args
        )

    @property
    def OverlayArgs(self):
        return DrawLineArgs(
            control_point_args=self.control_point_args
        )

def draw_lines(lines: Dict[Line, DrawLineArgs],
               surface: pygame.Surface,
               draw_scale_matrix: None):
    for line, args in lines.items():
        if args is None:
            continue

        # Convert Origin/Destination into np.arrays
        origin = np.array([line.origin[0], line.origin[1], 0, 1])
        destination = np.array([line.destination[0], line.destination[1], 0, 1])

        # Translate the points via the scaling matrix
        scaled = scaled_array(
            lst_point_array=np.array([origin, destination]),
            lh_matrix=draw_scale_matrix
        )

        # Draw the lines
        if args.color:
            w = args.width if args.width is not None else 1
            pygame.draw.line(surface,
                             args.color.value,
                             (scaled[0][0], scaled[0][1]),
                             (scaled[1][0], scaled[1][1]),
                             width=w)

        # Draw the points
        if args.control_point_args:
            putils.draw_points(
                points={
                    (x[0], x[1]): args.control_point_args for x in scaled
                },
                surface=surface,
                draw_scale_matrix=draw_scale_matrix
            )

        # Draw Directionality
        if args.directionality_draw_args:
            help.draw_arrow(surface=surface,
                            color=args.directionality_draw_args.color,
                            start=(scaled[0][0], scaled[0][1]),
                            end=(scaled[1][0], scaled[1][1]),
                            arrow_height=args.directionality_draw_args.height,
                            arrow_width=args.directionality_draw_args.width)

        # Draw Label
        if args.draw_label_args is not None and args.label_text is not None:
            mid = ((scaled[0][0] + scaled[1][0]) / 2, (scaled[0][1] + scaled[1][1]) / 2)
            lutils.draw_label(hud=surface,
                              args=args.draw_label_args,
                              pos=mid,
                              text=args.label_text)
from cooptools.coopEnum import CoopEnum
import math
from typing import Tuple, List
from cooptools.geometry.vectors.vectorN import Vector2

class Orientation(CoopEnum):
    UP_LEFT = 3
    UP_RIGHT = 4
    RIGHT_UP = 5
    RIGHT_DOWN = 6
    DOWN_RIGHT = 7
    DOWN_LEFT = 8
    LEFT_DOWN = 9
    LEFT_UP = 10
    UP = 11
    RIGHT = 12
    DOWN = 13
    LEFT = 14

    @classmethod
    def orientation_of(cls, origin, destination) -> List:
        orientation = None
        if origin.x == destination.x and origin.y > destination.y:
            orientation = [Orientation.UP]
        elif origin.x == destination.x and origin.y < destination.y:
            orientation = [Orientation.DOWN]
        elif origin.x < destination.x and origin.y == destination.y:
            orientation = [Orientation.RIGHT]
        elif origin.x > destination.x and origin.y == destination.y:
            orientation = [Orientation.LEFT]
        elif origin.x > destination.x and origin.y > destination.y:
            orientation = [Orientation.UP_LEFT, Orientation.LEFT_UP]
        elif origin.x > destination.x and origin.y < destination.y:
            orientation = [Orientation.DOWN_LEFT, Orientation.LEFT_DOWN]
        elif origin.x < destination.x and origin.y > destination.y:
            orientation = [Orientation.UP_RIGHT, Orientation.RIGHT_UP]
        elif origin.x < destination.x and origin.y < destination.y:
            orientation = [Orientation.DOWN_RIGHT, Orientation.RIGHT_DOWN]
        return orientation

    @classmethod
    def define_arc_radian_start_end(cls, orientation) -> Tuple[float, float]:
        if orientation == Orientation.DOWN_LEFT:
            arc_rad_start = 2 * math.pi
            arc_rad_end = 3 * math.pi / 2
        elif orientation == Orientation.DOWN_RIGHT:
            arc_rad_start = math.pi
            arc_rad_end = 3 * math.pi / 2
        elif orientation == Orientation.LEFT_DOWN:
            arc_rad_start = math.pi / 2
            arc_rad_end = math.pi
        elif orientation == Orientation.LEFT_UP:
           arc_rad_start = 3 * math.pi / 2
           arc_rad_end = math.pi
        elif orientation == Orientation.UP_LEFT:
            arc_rad_start = 0
            arc_rad_end = math.pi / 2
        elif orientation == Orientation.UP_RIGHT:
            arc_rad_start = math.pi
            arc_rad_end = math.pi / 2
        elif orientation == Orientation.RIGHT_DOWN:
            arc_rad_start = math.pi / 2
            arc_rad_end = 0
        elif orientation == Orientation.RIGHT_UP:
            arc_rad_start = 3 * math.pi / 2
            arc_rad_end = 2 * math.pi
        else:
            raise Exception(f"Invalid curve orientation: [{orientation}]")

        return arc_rad_start, arc_rad_end

    @classmethod
    def arc_box(cls, orientation, origin: Vector2, arc_box_dims: Vector2) -> List[float]:
        if orientation == Orientation.DOWN_LEFT:
            ret = [origin.x - arc_box_dims.x, origin.y - arc_box_dims.y / 2,
                    arc_box_dims.x, arc_box_dims.y]
        elif orientation == Orientation.DOWN_RIGHT:
            ret = [origin.x, origin.y - arc_box_dims.y / 2,
                    arc_box_dims.x, arc_box_dims.y]
        elif orientation == Orientation.LEFT_DOWN:
            ret = [origin.x - arc_box_dims.x / 2, origin.y,
                    arc_box_dims.x, arc_box_dims.y]
        elif orientation == Orientation.LEFT_UP:
            ret = [origin.x - arc_box_dims.x / 2, origin.y - arc_box_dims.y,
                    arc_box_dims.x, arc_box_dims.y]
        elif orientation == Orientation.UP_LEFT:
            ret = [origin.x - arc_box_dims.x, origin.y - arc_box_dims.y / 2,
                    arc_box_dims.x, arc_box_dims.y]
        elif orientation == Orientation.UP_RIGHT:
            ret = [origin.x, origin.y - arc_box_dims.y / 2,
                    arc_box_dims.x, arc_box_dims.y]
        elif orientation == Orientation.RIGHT_UP:
            ret = [origin.x - arc_box_dims.x / 2, origin.y - arc_box_dims.y,
                    arc_box_dims.x, arc_box_dims.y]
        elif orientation == Orientation.RIGHT_DOWN:
            ret = [origin.x - arc_box_dims.x / 2, origin.y,
                    arc_box_dims.x, arc_box_dims.y]
        else:
            raise Exception("Incorrect Curve type with orientation")

        return ret

class CurveType(CoopEnum):
    ARC = 1,
    CUBICBEZIER = 2,
    LINE = 3,
    CATMULLROM = 4

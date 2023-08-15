import uuid
from cooptools.coopEnum import CoopEnum, auto
from typing import Dict, List, Protocol, Set
from cooptools.geometry import Rectangle, Vector2
from dataclasses import dataclass
from cooptools.geometry.curves.enums import Orientation
from cooptools.common import divided_length
from cooptools.geometry.vectors import utils as vec

class CurveBoundaryType(CoopEnum):
    HIGHWAY = auto()

@dataclass
class ControlPointArgs:
    distance_between: float
    nested_distance: float
    fixed_beginning_buffer: float
    fixed_ending_buffer: float
    force_to_ends: bool = True

@dataclass
class CurveGenArgs:
    pass

@dataclass
class CurveBoundaryArea:
    rect: Rectangle
    type: CurveBoundaryType
    control_point_args: ControlPointArgs
    curve_gen_args: CurveGenArgs
    orientation: Orientation
    id: str = None

    def __post_init__(self):
        if self.id is None:
            object.__setattr__(self, 'id', uuid.uuid4())

    def __hash__(self):
        return hash(self.id)

def control_points_of_area(rect: Rectangle,
                           orientation: Orientation,
                           args: ControlPointArgs) -> List[Vector2]:
    # verify  supported orientation
    if orientation not in [Orientation.RIGHT, Orientation.LEFT, Orientation.UP, Orientation. DOWN]:
        raise NotImplementedError(f"The given orientation [{orientation}] is not supported")

    se_switch = {
        Orientation.LEFT: (Vector2.from_tuple(rect.RightCenter) - Vector2(args.fixed_beginning_buffer, 0),
                           Vector2.from_tuple(rect.LeftCenter) + Vector2(args.fixed_ending_buffer, 0)),
        Orientation.RIGHT: (Vector2.from_tuple(rect.LeftCenter) + Vector2(args.fixed_beginning_buffer, 0),
                            Vector2.from_tuple(rect.RightCenter) - Vector2(args.fixed_ending_buffer, 0)),
        Orientation.UP: (Vector2.from_tuple(rect.BottomCenter) + Vector2(0, args.fixed_beginning_buffer),
                         Vector2.from_tuple(rect.TopCenter) - Vector2(0, args.fixed_ending_buffer)),
        Orientation.DOWN: (Vector2.from_tuple(rect.TopCenter) - Vector2(0, args.fixed_beginning_buffer),
                           Vector2.from_tuple(rect.BottomCenter) + Vector2(0, args.fixed_ending_buffer)),
    }

    # define start, end and inc
    start, end = se_switch.get(orientation)
    inc = args.distance_between

    # get the divided values
    vals = vec.segmented_vector(inc, start=start.as_tuple(), stop=end.as_tuple(), force_to_ends=args.force_to_ends)

    # convert back to vector2
    ret = [Vector2.from_tuple(x) for x in vals]

    return ret


class CurveBoundaryFactory:
    def __init__(self, areas: Dict[CurveBoundaryArea, Set[CurveBoundaryArea]] = None):
        self.areas = {}
        self.add(areas)

    def add(self, areas: Dict[CurveBoundaryArea, Set[CurveBoundaryArea]]):
        for area, cnxs in areas.items():
            self.areas.setdefault(area, set()).union(cnxs)

if __name__ == "__main__":
    from pprint import pprint
    rect = Rectangle.from_tuple(rect=(0, 0, 100, 200))
    orient = Orientation.RIGHT
    control_pt_args = ControlPointArgs(distance_between=15,
                                       nested_distance=1,
                                       fixed_beginning_buffer=0,
                                       fixed_ending_buffer=0)

    pprint(control_points_of_area(rect, orient, control_pt_args))

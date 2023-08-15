from abc import ABC, abstractmethod
from cooptools.geometry.vectors.vectorN import Vector2
from cooptools.geometry import collinear_points
from typing import List, Callable, Tuple
from cooptools.geometry import Rectangle, Line, Triangle, Circle
from uuid import uuid4
from cooptools.geometry.curves.enums import Orientation
import cooptools.geometry.curves.utils as utils
import cooptools.geometry.circles.utils as circ
from cooptools.common import verify_val, bounding_box_of_points

class Curve(ABC):
    @classmethod
    @abstractmethod
    def from_points(cls, points: List[Vector2], naming_provider: Callable[[], str]) -> (List, List):
        pass

    @classmethod
    def from_json(cls, json: str):
        raise NotImplementedError()

    def __init__(self, origin: Vector2, id: str=None):
        self.origin = origin
        self.id = id or uuid4()

    def __str__(self):
        return f"{type(self).__name__} starting at {self.origin} and terminating at {self.EndPoint} [{self.id}]"

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return self.__str__()

    @abstractmethod
    def _end_point(self):
        raise NotImplementedError()

    @abstractmethod
    def _control_points(self) -> List[Vector2]:
        raise NotImplementedError()

    def point_representation(self, resolution: int = None) -> List[Vector2]:
        if resolution is None:
            resolution = 30
        if resolution < 2:
            return []

        increment = 1 / resolution

        result = []
        t = 0
        for i in range(resolution):
            result.append(self.point_at_t(i))
            t += increment

        return result

    def line_representation(self, resolution: int=None) -> List[Line]:
        b_points = self.point_representation(resolution)
        if b_points is None:
            return None

        ret = []
        for ii in range(0, len(b_points)):
            if ii == 0:
                continue
            else:
                start = Vector2(b_points[ii - 1].x, b_points[ii - 1].y)
                end = Vector2(b_points[ii].x, b_points[ii].y)
                ret.append(Line(start, end))
        return ret

    def bounding_box(self, resolution: int) -> Tuple[float, float, float, float]:
        return bounding_box_of_points([x.as_tuple() for x in self.point_representation(resolution=resolution)])

    @abstractmethod
    def force_continuity(self, next_point: Vector2, close_circuit: bool = False) -> Vector2:
        pass

    @abstractmethod
    def point_at_t(self, t: float) -> Vector2:
        pass

    @abstractmethod
    def tangent_at_t(self, t: float) -> Vector2:
        pass

    def derivative_at_t(self, t: float) -> float:
        tan = self.tangent_at_t(t)
        return tan.y / tan.x

    @property
    def Length(self):
        lines = self.line_representation()
        return sum([x.length for x in lines])

    @property
    def EndPoint(self):
        return self._end_point()

    @property
    def ControlPoints(self) -> List[Vector2]:
        return self._control_points()

    @property
    def MidPoint(self) -> Vector2:
        return self.point_at_t(0.5)

class Arc(Curve):

    @classmethod
    def from_points(cls, points: List[Vector2], naming_provider: Callable[[], str]) -> (List, List):
        curves = []

        if len(points) == 2 and points[0] == points[1]:
            return curves, points

        for ii in range(len(points) - 1):
            orientation = Orientation.orientation_of(points[ii], points[ii + 1])[0]
            if orientation in (Orientation.UP, Orientation.RIGHT, Orientation.DOWN, Orientation.LEFT):
                curves.append(LineCurve(id=naming_provider(), origin=points[ii], destination=points[ii + 1]))
            else:
                curves.append(Arc(orientation, points[ii],
                                  Vector2(abs(points[ii + 1].x - points[ii].x) * 2,
                                          abs(points[ii + 1].y - points[ii].y) * 2),
                                  id=naming_provider())
                              )
        return curves, []

    @classmethod
    def from_json(cls, json: str):
        raise NotImplementedError()

    @classmethod
    def from_arcbox(cls, id: str, orientation: Orientation, origin: Vector2, arc_box_size: Vector2):
        return Arc(orientation, origin, arc_box_size, id=id)

    @classmethod
    def from_origin_and_destination(cls, id: str, orientation: Orientation, origin: Vector2, destination: Vector2):
        return Arc(orientation, origin, Vector2(destination.x - origin.x, destination.y - origin.y) * 2, id=id)

    def __init__(self, orientation: Orientation, origin: Vector2, arc_box_size: Vector2, id: str=None):
        super().__init__(id=id, origin=origin)
        self.orientation = orientation
        self.arc_box_size = arc_box_size
        self.arc_rad_start, self.arc_rad_end = Orientation.define_arc_radian_start_end(self.orientation)
        self._arc_box = Orientation.arc_box(self.orientation, self.origin, self.arc_box_size)
        self.mid_point = Vector2(self._arc_box[0] + self._arc_box[2] / 2.0, self._arc_box[1] + self._arc_box[3] / 2.0)

    def _control_points(self) -> List[Vector2]:
        return [self.origin, self.EndPoint]

    def _end_point(self):
        if self.orientation in (Orientation.DOWN_LEFT, Orientation.LEFT_DOWN):
            return Vector2(int(self.origin.x - self.arc_box_size.x / 2), int(self.origin.y + self.arc_box_size.y / 2))
        elif self.orientation in (Orientation.LEFT_UP, Orientation.UP_LEFT):
            return Vector2(int(self.origin.x - self.arc_box_size.x / 2), int(self.origin.y - self.arc_box_size.y / 2))
        elif self.orientation in (Orientation.UP_RIGHT, Orientation.RIGHT_UP):
            return Vector2(int(self.origin.x + self.arc_box_size.x / 2), int(self.origin.y - self.arc_box_size.y / 2))
        elif self.orientation in (Orientation.RIGHT_DOWN, Orientation.DOWN_RIGHT):
            return Vector2(int(self.origin.x + self.arc_box_size.x / 2), int(self.origin.y + self.arc_box_size.y / 2))
        else:
            raise Exception("Incorrect Curve type with orientation")

    def arc_box_as_rectangle(self) -> Rectangle:
        return Rectangle(x=self._arc_box[0], y=self._arc_box[1], width=self._arc_box[2], height=self._arc_box[3])

    @property
    def Length(self):
        ab = self.arc_box_as_rectangle()
        major = max(ab.height, ab.width) / 2
        minor = min(ab.height, ab.width) / 2
        return circ.arc_length_ramanujans_approx(self.arc_rad_start, self.arc_rad_end, major_radius=major, minor_radius=minor)

    def force_continuity(self, next_point: Vector2, close_circuit: bool = False) -> Vector2:
        if close_circuit:
            raise NotImplementedError(f"Close circuit not implemented for type [{type(self)}]")

        end_point = self.EndPoint
        if self.orientation in (Orientation.UP_LEFT, Orientation.DOWN_LEFT) and next_point.x > end_point.x:
            return Vector2(end_point.x, next_point.y)
        elif self.orientation in (Orientation.UP_RIGHT, Orientation.DOWN_RIGHT) and next_point.x < end_point.x:
            return Vector2(end_point.x, next_point.y)
        elif self.orientation in (Orientation.RIGHT_UP, Orientation.LEFT_UP) and next_point.y > end_point.y:
            return Vector2(next_point.x, end_point.y)
        elif self.orientation in (Orientation.RIGHT_DOWN, Orientation.LEFT_DOWN) and next_point.y < end_point.y:
            return Vector2(next_point.x, end_point.y)
        else:
            return next_point


class CircularArc(Curve):
    @classmethod
    def from_points(cls, points: List[Vector2], naming_provider: Callable[[], str]) -> (List, List):
        leftover_points = []
        leftover_count = (len(points) - 1) % 3 if len(points) >= 3 else len(points)
        leftover_points = points[-leftover_count:] if leftover_count != 0 else leftover_points
        used_points = points[:-leftover_count] if leftover_count != 0 else points

        curves = []

        if len(points) < 3:
            return curves, points

        # A Cubic Bezier requires 4 control points, so operate in blocks of 4 (re-using the last each time)
        for ii in range(0, len(used_points) - 3, 3):
            curves.append(CircularArc(id=naming_provider(),
                                      origin=points[ii],
                                      destination=points[ii + 1],
                                      center=points[ii + 2]))

        return curves, leftover_points

    @classmethod
    def from_3_consecutive_points(cls, a: Vector2, b: Vector2, c: Vector2, naming_provider: Callable[[], str]):

        circle = Circle.from_boundary_points(a, b, c)

        rads_ab = circle.rads_between_points(a, b)
        rads_ac = circle.rads_between_points(a, c)

        if rads_ac > rads_ab:
            ret = CircularArc(id=naming_provider(),
                              origin=a,
                              destination=c,
                              center=circle.Center)
        else:
            ret = CircularArc(id=naming_provider(),
                              origin=c,
                              destination=a,
                              center=circle.Center)

        return ret

    @classmethod
    def from_json(cls, json: str):
        raise NotImplementedError()

    def __init__(self, origin: Vector2, destination: Vector2, center: Vector2, id:str=None):
        """ Create a circle given a center, start, and end. The arc is assumed to be the counter-clockwise movement from origin to
        destination, so enter the o and d appropriately based on which segment between points is required"""

        if origin == center or destination == center or origin == destination:
            raise ValueError(f"Origin, destination and center must all be different. Provided:"
                             f"\no: {origin}"
                             f"\nd: {destination}"
                             f"\nc: {center}")

        centered_o = origin - center
        centered_d = destination - center
        min_length = min(centered_o.length(), centered_d.length())

        scaled_o = centered_o.scaled_to_length(min_length)
        scaled_d = centered_d.scaled_to_length(min_length)

        used_o = center + scaled_o
        used_d = center + scaled_d

        super().__init__(id=id, origin=used_o)
        self.circle = Circle(center, radius=min_length)
        self.destination = used_d

    @property
    def center(self):
        return self.circle.center

    @property
    def angle_rads(self):
        return self.circle.rads_between_points(self.origin.as_tuple(), self.destination.as_tuple())

    @property
    def arc_length(self):
        return self.radius * self.angle_rads

    @property
    def radius(self):
        return self.circle.radius

    @property
    def origin_rads(self):
        return self.circle.rads_of_point(self.origin.as_tuple())

    @property
    def destination_rads(self):
        return self.circle.rads_of_point(self.destination)

    def _end_point(self):
        return self.destination

    def _control_points(self) -> List[Vector2]:
        return [self.origin, self.destination, self.center]

    def line_representation(self) -> List[Line]:
        pass

    def force_continuity(self, next_point: Vector2, close_circuit: bool = False) -> Vector2:
        raise NotImplementedError(f"force_circuit not implemented for type [{type(self)}]")

    def compute_circulararc_points(self, numPoints: int = None):
        if numPoints is None:
            numPoints = 30

        step_size = self.angle_rads / numPoints
        start = self.circle.rads_of_point(self.origin.as_tuple())
        points = []
        for ii in range(0, numPoints):
            point = self.circle.point_at_angle(radians=start + ii * step_size)
            points.append(point)

        return points


class LineCurve(Curve):
    @classmethod
    def from_points(self, points, naming_provider: Callable[[], str]) -> (List, List):
        lines = []
        for ii in range(len(points) - 1):
            lines.append(LineCurve(points[ii], points[ii + 1], id=naming_provider()))
        return lines, []

    @classmethod
    def from_json(cls, json: str):
        raise NotImplementedError()

    def __init__(self, origin: Vector2, destination: Vector2, id: str=None):
        super().__init__(id=id, origin=origin)
        self.destination = destination

    def _control_points(self) -> List[Vector2]:
        return [self.origin, self.EndPoint]

    def line_representation(self, resolution:int=None):
        return [Line(self.origin, self.destination)]

    def _end_point(self):
        return self.destination

    @property
    def Length(self):
        return Line(self.origin, self.destination).length

    def force_continuity(self, next_point: Vector2, close_circuit: bool = False) -> Vector2:
        if close_circuit:
            raise NotImplementedError(f"Close circuit not implemented for type [{type(self)}]")
        return next_point

    def point_at_t(self, t: float):
        if not (0 <= t <= 1):
            raise ValueError(f"t must be between 0 and 1 but {t} was provided")

        line_vector = self.EndPoint - self.origin
        t_vector = line_vector * t

        return self.origin + t_vector

    def tangent_at_t(self, t: float) -> Vector2:
        verify_val(t, low_inc=0, hi_inc=1)
        return (self.EndPoint - self.origin).unit()


class CubicBezier(Curve):

    @classmethod
    def from_json(cls, json: str):
        cps = []
        for pt_data in json['controlPoints']:
            pt = Vector2.from_json(pt_data)
            cps.append(pt)

        return CubicBezier(control_points=cps)

    def point_at_t(self, t: float):
        return Vector2.from_tuple(utils.cubic_bezier_point_at_t(t, [x.as_tuple() for x in self.ControlPoints]))

    def tangent_at_t(self, t: float) -> Vector2:
        return Vector2.from_tuple(utils.cubic_bezier_tangent_at_t(t, [x.as_tuple() for x in self.ControlPoints])).unit()

    @classmethod
    def as_circular_arcs(cls, curve, tolerance: float = 10):
        if not type(curve) == CubicBezier:
            raise TypeError(f"provided value was not of type {CubicBezier}. {type(curve)} provided")

        # find inflection points
        inflection_points = curve.inflection_points()

        # handle inflection points on curve
        if len(inflection_points) > 0:
            sub_divisions = curve.sub_divide_at_t(inflection_points[0][1])
            arcs = [CubicBezier.as_circular_arcs(x, tolerance) for x in sub_divisions]
            return [item for sublist in arcs for item in sublist]

        # handle check if circle is a good approximater
        if curve.origin != curve.EndPoint:
            circle = curve.biarc_circle()
            deviation = cls.max_delta_on_circle(curve, circle) if circle is not None else None
            if circle is None:
                # no arcs for this curve since the circle could not be defined (straight line bezier)
                return []
            elif deviation < tolerance:
                # approximating arc is withing tolerance, return the arc
                return [CircularArc.from_3_consecutive_points(a=circle.known_boundary_points[0],
                                                              b=circle.known_boundary_points[1],
                                                              c=circle.known_boundary_points[2],
                                                              naming_provider=lambda: str(uuid4()))]

            # handle subdivide and try again
            sub_divisions = curve.sub_divide_at_t(0.5)
            arcs = [CubicBezier.as_circular_arcs(x, tolerance) for x in sub_divisions]
            return [item for sublist in arcs for item in sublist]
        else:
            return []

    @classmethod
    def max_delta_on_circle(cls, curve, biarc_circle: Circle):
        max_delta = 0
        for point in curve.cubic_bezier_points([(x.x, x.y) for x in curve.ControlPoints], 10):
            point = Vector2(point[0], point[1])
            dist_from_center = (point - biarc_circle.center).length()
            deviation = abs(biarc_circle.radius - dist_from_center)
            if deviation > max_delta:
                max_delta = deviation

        return max_delta

    @classmethod
    def from_points(cls, points: List[Vector2], naming_provider: Callable[[], str]) -> (List, List):
        leftover_points = []
        leftover_count = (len(points) - 1) % 3 if len(points) >= 4 else len(points)
        leftover_points = points[-leftover_count:] if leftover_count != 0 else leftover_points
        used_points = points[:-leftover_count] if leftover_count != 0 else points

        curves = []

        if len(points) < 4:
            return curves, points

        # A Cubic Bezier requires 4 control points, so operate in blocks of 4 (re-using the last each time)
        for ii in range(0, len(used_points) - 3, 3):
            curves.append(CubicBezier(points[ii:ii + 4], id=naming_provider()))

        return curves, leftover_points

    def __init__(self, control_points: List[Vector2], id: str=None):

        if all(point.distance_from(control_points[0]) < .001 for point in control_points):
            raise ValueError(f"the provided control points are invalid as they are all the same: {control_points[0]}")

        Curve.__init__(self, control_points[0], id)
        self._cps = control_points

    def _control_points(self) -> List[Vector2]:
        return self._cps

    def _end_point(self):
        return self.ControlPoints[-1]

    def force_continuity(self, next_point: Vector2, close_circuit: bool = False) -> Vector2:

        if close_circuit:
            return next_point.project_onto(self.ControlPoints[0], self.ControlPoints[1])
        else:
            return next_point.project_onto(self.ControlPoints[-1], self.ControlPoints[-2])

    def biarc_circle(self) -> (Circle, float):
        p1 = self.ControlPoints[0]
        p4 = self.ControlPoints[3]

        p1_ = p1 + utils.cubic_bezier_tangent_at_t(0, [x.as_tuple() for x in self.ControlPoints])
        p4_ = p4 + utils.cubic_bezier_tangent_at_t(1, [x.as_tuple() for x in self.ControlPoints])

        line1 = Line(origin=p1, destination=p1_)
        line2 = Line(origin=p4, destination=p4_)

        try:
            V = line1.intersection(line2)
        except:
            return None

        if not collinear_points([x.as_tuple() for x in [p1, V, p4]]):
            tri = Triangle(p1.as_tuple(), V, p4.as_tuple())
            incentre = tri.incentre()

            biarc_circ = Circle.from_boundary_points(p1, incentre, p4)
        else:
            return None

        return biarc_circ

    def sub_divide_at_t(self, t: float):
        return [CubicBezier(control_points=[Vector2.from_tuple(p1),
                                            Vector2.from_tuple(r2),
                                            Vector2.from_tuple(r3),
                                            Vector2.from_tuple(point_t)], id=str(uuid4())) for p1, r2, r3, point_t in
                utils.cubic_bezier_sub_divide_at_t(t, [x.as_tuple() for x in self.ControlPoints])]


class CatmullRom(Curve):

    @classmethod
    def from_points(cls, points: List[Vector2], naming_provider: Callable[[], str]) -> (List, List):
        leftover_points = []
        leftover_count = len(points) if len(points) < 4 else 0
        leftover_points = points if leftover_count != 0 else leftover_points
        used_points = points if leftover_count == 0 else []

        curves = []

        if len(used_points) < 4:
            return [], points

        # A Cubic Bezier requires 4 control points, so operate in blocks of 3 (re-using the last each time)
        curves.append(CatmullRom(points, naming_provider()))
        return curves, leftover_points

    @classmethod
    def from_json(cls, json: str):
        raise NotImplementedError()

    def __init__(self, control_points: List[Vector2], id: str = None):
        Curve.__init__(self, control_points[0], id)

        if len(control_points) < 4:
            raise ValueError(
                f"Invalid input for control points. Must have at least 4 values but list of length {len(control_points)} was provided: [{control_points}]")
        self._cps = control_points

    def _control_points(self) -> List[Vector2]:
        return self._cps

    def _end_point(self):
        return self.ControlPoints[-1]

    def force_continuity(self, next_point: Vector2, close_circuit: bool = False) -> Vector2:
        if close_circuit:
            raise NotImplementedError(f"Close circuit not implemented for type [{type(self)}]")
        return next_point

    def point_at_t(self, t: float):
        return utils.catmull_points([x.as_tuple() for x in self.ControlPoints])

    def tangent_at_t(self, t: float) -> Vector2:
        raise NotImplementedError()

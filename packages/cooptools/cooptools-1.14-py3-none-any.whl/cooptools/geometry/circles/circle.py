from typing import List, Tuple, Union
import cooptools.geometry.circles.utils as circ
from cooptools.geometry.vectors.vectorN import VectorN

SupportedLinePointTypes = Union[VectorN, Tuple[float, float]]

def _convert_supported_type_to_tuple(val: SupportedLinePointTypes) -> Tuple[float, float]:
    if issubclass(type(val), VectorN):
        val = val.as_tuple()

    return val



class Circle:

    @classmethod
    def from_boundary_points(cls, point1: SupportedLinePointTypes, point2: SupportedLinePointTypes, point3: SupportedLinePointTypes):
        point1 = _convert_supported_type_to_tuple(point1)
        point2 = _convert_supported_type_to_tuple(point2)
        point3 = _convert_supported_type_to_tuple(point3)

        cent, rad = circ.from_boundary_points(point1, point2, point3)
        return Circle(cent, rad, known_boundary_points=[point1, point2, point3])

    def __init__(self, center: SupportedLinePointTypes, radius: float, known_boundary_points: List[SupportedLinePointTypes] = None):
        if type(radius) != float:
            raise TypeError(f"Radius must be of type float, but type {type(radius)} was provided")

        if issubclass(type(center), VectorN):
            origin = center.as_tuple()

        self.center = center
        self.radius = radius
        self.known_boundary_points = [_convert_supported_type_to_tuple(x) for x in known_boundary_points] if known_boundary_points is not None else []

    def point_at_angle(self, radians: float = None, degrees: float = None) -> Tuple[float, float]:
        return circ.point_at_angle(self.center, self.radius, radians=radians, degrees=degrees)

    def rads_of_point(self, point: Tuple[float, float]) -> float:
        return circ.rads_of_point_around_origin(a=point, origin=self.center)

    def degree_of_point(self, point: Tuple[float, float]) -> float:
        return circ.degrees_of_point_around_origin(a=point, origin=self.center)

    def rads_between_points(self, a: Tuple[float, float], b: Tuple[float, float], minimum_chunk=False) -> float:
        return circ.rads_between(a, b, origin=self.center, minimum_chunk=minimum_chunk)

    def degress_between_points(self, a: Tuple[float, float], b: Tuple[float, float], minimum_chunk=False) -> float:
        return circ.degrees_between(a, b, origin=self.center, minimum_chunk=minimum_chunk)

    @property
    def Center(self):
        return self.center

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"Circle of radius {round(self.radius, 2)} centered at {self.center}"
import cooptools.geometry.lines.utils as utils
from typing import Tuple, Union
from cooptools.common import verify_unique
from cooptools.geometry.vectors.vectorN import VectorN

SupportedLineEndTypes = Union[VectorN, Tuple[float, float]]
LineTuple = Tuple[Tuple[float, float], Tuple[float, float]]

class Line:
    def __init__(self, origin: SupportedLineEndTypes, destination: SupportedLineEndTypes):
        verify_unique([origin, destination], error_msg=utils.LINE_ENPOINT_MATHC_ERROR_MSG)

        if issubclass(type(origin), VectorN):
            origin = origin.as_tuple()

        if issubclass(type(destination), VectorN):
            destination = destination.as_tuple()

        self.origin = origin
        self.destination = destination

    def as_tuple(self):
        return (self.origin, self.destination)

    @property
    def length(self):
        return utils.line_length(self.as_tuple())

    def intersection(self, other_line, extend: bool = False) -> Tuple[float, ...]:
        if not type(other_line) == Line and not type(other_line) == Union[type(self), LineTuple]:
            raise TypeError(f"can not intersect with objects of type {type(other_line)}")

        if type(other_line) == Line:
            other_line = other_line.as_tuple()

        if len(self.origin) > 2:
            raise NotImplementedError(f"Intersection not implemented for a line in dimension > 2")

        return utils.line_intersection_2d(self.as_tuple(), other_line, extend)

if __name__ == "__main__":
    l1 = Line((0, 0), (10, 10))
    l2 = Line((0, 10), (10, -1))

    print(l1.intersection(l2))
    print(l1.length)
    print(l2.length)
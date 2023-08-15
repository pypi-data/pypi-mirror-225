from typing import Tuple
import cooptools.geometry.triangles.utils as tria

class Triangle:
    def __init__(self, a: Tuple[float, float], b: Tuple[float, float], c: Tuple[float, float]):
        tria.verify_triangle_points(a, b, c)
        self.points = [a, b, c]

    @property
    def Area(self):
        return tria.area(self.a, self.b, self.c)

    @property
    def a(self):
        return self.points[0]

    @property
    def b(self):
        return self.points[1]

    @property
    def c(self):
        return self.points[2]

    def incentre(self):
        return tria.incentre(self.a, self.b, self.c)
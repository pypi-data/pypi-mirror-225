from cooptools.geometry.vectors.vectorN import Vector2
from typing import List, Tuple, Dict
import cooptools.geometry as geo
from cooptools.geometry.lines.line import Line
from scipy.spatial import ConvexHull
from shapely.geometry import Polygon, Point
from cooptools.geometry.exceptions import DuplicatePointException
from cooptools.geometry.logger import geomLogger
from cooptools.common import all_indxs_in_lst, bounding_box_of_points


DUMMY_NEXT_ZONE_NAME = "DUMMY"

class PolygonRegion:

    @classmethod
    def from_shapely_polygon(cls, shapely_poly: Polygon):
        x, y = shapely_poly.exterior.coords.xy
        return PolygonRegion([Vector2(x[ii], y[ii]) for ii in range(0, len(x))])

    @classmethod
    def from_json(cls, json):
        boundary_points = [Vector2.from_json(pt) for pt in json['boundaryPoints']]
        return PolygonRegion(boundary_points=boundary_points)


    @classmethod
    def convex_hull(self, points: List[Vector2]):
        if not geo.collinear_points([point.as_tuple() for point in points]):
            hull = ConvexHull([point.as_tuple() for point in points])
            return PolygonRegion([points[ind] for ind in hull.vertices])
        else:
            return PolygonRegion(points)

    def __init__(self, boundary_points: List[Vector2] = None):
        self.boundary_points = boundary_points if boundary_points is not None else []

    def __len__(self):
        return len(self.boundary_points)

    def __str__(self):
        points_txt = '\n' + '\n'.join([str(x) for x in self.boundary_points]) if len(self.boundary_points) > 0 else ""
        return f"Polygon Region with {len(self.boundary_points)} points: {points_txt}"

    def __repr__(self):
        return self.__str__()

    @property
    def as_shapely_polygon(self) -> Polygon:
        return Polygon([p.as_tuple() for p in self.boundary_points])

    @property
    def valid(self):
        # valid if at least 3 points and they are not collinear
        return len(self.boundary_points) >= 3 and not geo.collinear_points([point.as_tuple() for point in self.boundary_points])

    def add_points(self, points: List[Vector2], at_idx: int = None):
        # check if the new point(s) to be added are a duplicate of the last point added
        bndry_pts_init = self.boundary_points and len(self.boundary_points) > 0
        if bndry_pts_init \
                and at_idx \
                and points[0] in self.boundary_points[at_idx-1: at_idx + 1]:
            raise DuplicatePointException(points[0])
        elif bndry_pts_init \
                and points[0] == self.boundary_points[-1]:
            raise DuplicatePointException(points[0])


        if at_idx is None:
            self.boundary_points += points
        else:
            self.boundary_points[at_idx:at_idx] = points

        geomLogger.info(f'Points {points} added at idx: {at_idx}')

    def remove_point(self):
        if len(self.boundary_points) > 0:
            self.boundary_points.pop(-1)

    def intersects(self, other, buffer:float = 0) ->bool:
        if not type(other) == PolygonRegion:
            raise TypeError(f"Cannot find intersection of type {type(self)} with type {type(other)}")


        return Polygon([x.as_tuple() for x in self.boundary_points]).buffer(buffer).intersects(
            Polygon([x.as_tuple() for x in other.boundary_points]).buffer(buffer))

        # intersection = Polygon([x.as_tuple() for x in self.boundary_points]).buffer(buffer).intersection(Polygon([x.as_tuple() for x in other.boundary_points]).buffer(buffer))

        # try:
        #     if intersection is None or intersection.is_empty:
        #         return None
        #     elif intersection.geom_type == "LineString":
        #         x, y = intersection.coords.xy
        #     elif intersection.geom_type == "GeometryCollection":
        #         x, y = intersection.convex_hull.exterior.coords.xy
        #     elif intersection.geom_type == "Point":
        #         x, y = intersection.coords.xy
        #     else:
        #         x, y = intersection.exterior.coords.xy
        # except:
        #     raise Exception(f"Unknown error...")
        #
        # return PolygonRegion([Vector2(x[ii], y[ii]) for ii in range(0, len(x))])

    def buffer(self, buffer: float):
        return PolygonRegion.from_shapely_polygon(self.as_shapely_polygon.buffer(distance=buffer))

    def union(self, other):
        return PolygonRegion.from_shapely_polygon(self.as_shapely_polygon.union(other.as_shapely_polygon))

    @property
    def Center(self) -> Vector2:
        if len(self.boundary_points) == 0:
            return None

        xs = [point.x for point in self.boundary_points]
        ys = [point.y for point in self.boundary_points]
        cx = sum(xs) / len(xs)
        cy = sum(ys) / len(ys)

        return Vector2(cx, cy)

    @property
    def BoundingBox(self) -> Tuple[float, float, float, float]:
        return bounding_box_of_points([x.as_tuple() for x in self.boundary_points])

    def with_additional_point(self,
                              point: Vector2,
                              convex: bool = False,
                              at_idx: int = None):

        new_list = self.boundary_points + [point]

        if convex:
            poly = PolygonRegion.convex_hull(new_list)
        elif at_idx is not None:
            poly = PolygonRegion(boundary_points=self.boundary_points)
            poly.add_points([point], at_idx)
        else:
            poly = PolygonRegion(boundary_points=new_list)

        return poly

    def idxs_of_point(self, points) -> Dict[Vector2, List[int]]:
        ret = {point: all_indxs_in_lst(self.boundary_points, point) for point in points}
        return ret

    def contains_points(self, points: List[Vector2]) -> Dict[Vector2, bool]:
        ret = {}

        shapely_poly = self.as_shapely_polygon
        for point in points:
            ret[point] = shapely_poly.contains(Point(point.x, point.y))

        return ret

    def insersection_boundary_idxs_from_origin(self, point: Vector2, origin: Vector2) -> List[Tuple[int, int]]:
        intersections = []

        ln1 = Line(origin, point)
        for idx in range(len(self.boundary_points) - 1):
            ln2 = Line(self.boundary_points[idx], self.boundary_points[idx + 1])

            if ln1.intersection(ln2):
                intersections.append((idx, idx+1))

        return intersections





if __name__ == "__main__":
    points = [Vector2(0, 0),
              Vector2(10, 0),
              Vector2(10, 10),
              Vector2(0, 10)]

    poly = PolygonRegion(points)

    new = Vector2(11, 4)
    bnds = poly.insersection_boundary_idxs_from_origin(new, Vector2(5, 5))

    poly2 = poly.with_additional_point(new, at_idx=bnds[0])
    print(poly2)


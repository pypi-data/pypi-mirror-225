import time
from cooptools.geometry.curves.curves import Curve
from cooptools.geometry.polygonRegion import PolygonRegion
from cooptools.geometry.vectors.vectorN import Vector2
import cooptools.geometry.circles.utils as circ
from typing import Tuple, List, Dict, Sequence
import math
from dataclasses import dataclass
import cooptools.os_manip as osm
from cooptools.geometry.curves.curve_factory import curve_from_json, curves_from_json
from cooptools.plotting import plot_series
from cooptools.colors import Color

@dataclass
class TraceIter:
    polygon: PolygonRegion
    anchor: Tuple[float, float]
    tangent: Tuple[float, float]

@dataclass
class TraceMeta:
    polygon: PolygonRegion
    traces: Dict[int, TraceIter]
    swimlane: PolygonRegion

def trace_curve_with_polygon(curve: Curve,
                              polygon: PolygonRegion,
                              pivot: Tuple[float, float],
                              increment_fixed: float = None,
                              increment_p: float = None,
                              default_rads: float = None,
                             ) -> Dict[int, TraceIter]:

    if increment_p is None and increment_fixed is None:
        increment_p = 0.05

    if increment_p is None and increment_fixed is not None:
        increment_p = increment_fixed / curve.Length

    if increment_p is not None and increment_fixed is not None:
        increment_p = min(increment_p, increment_fixed / curve.Length)

    if default_rads is None:
        default_rads = math.pi / 2

    # move the poly so that its pivot is at 0, 0
    adjusted_poly = PolygonRegion(boundary_points=[pt - Vector2.from_tuple(pivot) for pt in polygon.boundary_points])

    # determine the convex hull of the adjusted poly
    ch = PolygonRegion.convex_hull(adjusted_poly.boundary_points)

    iter = {}
    t = 0
    ii = 0
    while t < 1:
        # get position and direction
        anchor = curve.point_at_t(t)
        tu = curve.tangent_at_t(t)

        rads = circ.rads_of_point_around_origin(tu.as_tuple()) - default_rads

        # translate ch to position and rotation
        pts = []
        for point in ch.boundary_points:
            rotated_point = circ.rotated_point(point=point.as_tuple(), center=(0, 0), rads=rads)
            adjusted_boundary_point = Vector2.from_tuple(rotated_point) + anchor
            pts.append(adjusted_boundary_point)
            iter[ii] = TraceIter(polygon=PolygonRegion(pts), anchor=anchor.as_tuple(), tangent=tu.as_tuple())

        # increment t
        t += increment_p
        ii += 1

    # convex hull of swim lane verts
    return iter

def create_swimlane(positions: Sequence[PolygonRegion], buffer: float = None) -> PolygonRegion:

    swimlane = None
    for ii, poly in enumerate(positions):
        if ii == 0:
            continue

        points = poly.boundary_points + positions[ii - 1].boundary_points
        hull = PolygonRegion.convex_hull(points)

        if swimlane is None:
            swimlane = hull
        else:
            swimlane = swimlane.union(hull)

    if buffer:
        swimlane = swimlane.buffer(buffer=buffer)

    return swimlane

def trace_from_files(poly_file: str,
                     curves_file: str) -> Dict[Curve, TraceMeta]:

    poly, pivot = traceable_poly_from_file(poly_file)
    curves = curves_from_file(curves_file)

    ret = {}
    for curve in curves:
        traced = trace_curve_with_polygon(curve=curve,
                                          polygon=poly,
                                          pivot=pivot)
        sl = create_swimlane([x.polygon for x in traced.values()], buffer=0.25)
        ret[curve] = TraceMeta(
            polygon=poly,
            traces=traced,
            swimlane=sl
        )

    return ret


def traceable_poly_from_file(poly_file: str) -> Tuple[PolygonRegion, Tuple[float, float]]:
    content = osm.try_load_json_data(poly_file)
    poly = PolygonRegion.from_json(content)
    pivot = Vector2.from_json(content['pivotPoint'])
    return poly, pivot.as_tuple()

def curves_from_file(curves_file: str) -> List[Curve]:
    content = osm.try_load_json_data(curves_file)
    return curves_from_json(content)




def plot_traced_curve(traced_curve: Dict[int, TraceIter],
                      swim_lane: PolygonRegion,
                      ax):
    plot_series(ax=ax, points=[x.as_tuple() for x in swim_lane.boundary_points], series_type='fill')
    for ii, iter in traced_curve.items():
        plot_series(points=[x.as_tuple() for x in iter.polygon.boundary_points],
                    ax=ax,
                    series_type="scatter",
                    )
    plot_series(ax=ax, points=[traced.anchor for ii, traced in traced_curve.items()], series_type='line', color=Color.BLACK)




if __name__ == "__main__":
    import matplotlib.pyplot as plt

    t0 = time.perf_counter()
    traces = trace_from_files(
        r'C:\Users\tburns\PycharmProjects\cooptools\tests\testdata\traceable_poly_data.json',
        r'C:\Users\tburns\PycharmProjects\cooptools\tests\testdata\curves.json'
    )
    print(time.perf_counter() - t0)

    fig, ax = plt.subplots(1, 1)

    for curve, meta in traces.items():
        plot_traced_curve(meta.traces, meta.swimlane, ax)

    plt.show()





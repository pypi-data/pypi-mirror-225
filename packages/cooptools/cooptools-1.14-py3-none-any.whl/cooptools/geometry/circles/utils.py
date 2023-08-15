from typing import Tuple
from cooptools.common import verify_unique, verify_len, rads_to_degrees, degree_to_rads
from cooptools.geometry.vectors.utils import interpolate, orthogonal2x2, vector_between, add_vectors, distance_between, zero_vector
from cooptools.geometry.lines.utils import line_intersection_2d
import math
import random as rnd

def from_boundary_points(a: Tuple[float, float], b: Tuple[float, float], c: Tuple[float, float]) -> Tuple[Tuple[float, float], float]:
    lst = [a, b, c]
    verify_unique(lst)

    # calculate midpoints
    m1 = interpolate(a, b, amount=.5)
    m2 = interpolate(b, c, amount=.5)

    # Generate perpendicular vectors
    perp_m1 = orthogonal2x2(vector_between(a, m1))
    perp_m1_line = (m1, add_vectors([m1, perp_m1]))

    perp_m2 = orthogonal2x2(vector_between(b, m2))
    perp_m2_line = (m2, add_vectors([m2, perp_m2]))

    # Circle center is where perpendicular vectors intersect
    circ_center = line_intersection_2d(line1=perp_m1_line, line2=perp_m2_line, extend=True)

    # Radius is distance from center to one of the boundary points
    rad = distance_between(circ_center, a)

    return circ_center, rad

def point_at_angle(center: Tuple[float, float],
                   radius: float,
                   radians: float = None,
                   degrees: float = None) -> Tuple[float, float]:
    if radians is None and degrees is None:
        raise ValueError(f"Either radians or degress must have a value")

    if radians is None:
        radians = degree_to_rads(degrees)

    x = (radius * math.cos(radians) + center[0])
    y = (radius * math.sin(radians) + center[1])
    return x, y

def rotated_point(point: Tuple[float, float],
                  center: Tuple[float, float] = None,
                  rads: float = None,
                  degrees: float = None) -> Tuple[float, float]:
    if rads is None and degrees is None:
        raise ValueError(f"Either radians or degress must have a value")

    if rads is None:
        rads = degree_to_rads(degrees)

    radius = distance_between(point, center)
    pt_rads = rads_of_point_around_origin(point, center)
    rotated_rads = pt_rads + rads

    return point_at_angle(center=center, radius=radius, radians=rotated_rads)






def rads_of_point_around_origin(a: Tuple[float, float],
                                origin: Tuple[float, float] = None) -> float:
    if origin is None:
        origin = zero_vector(len(a))

    verify_len(a, 2)
    verify_len(origin, 2)

    rads = math.atan2(a[1] - origin[1], a[0] - origin[0])

    if math.isclose(rads, math.pi * 2):
        ret = 0
    elif rads >= 0:
        ret = rads
    else:
        ret = 2 * math.pi + rads

    return ret

def degrees_of_point_around_origin(a: Tuple[float, float],
                                   origin: Tuple[float, float] = None) -> float:
    return rads_to_degrees(rads_of_point_around_origin(a, origin))


def rads_between(v: Tuple[float, float],
                 start: Tuple[float, float] = None,
                 origin: Tuple[float, float] = None,
                 minimum_chunk: bool = False
                 ) -> float:
    rads_start = rads_of_point_around_origin(start, origin) if start is not None else 0
    rads_v = rads_of_point_around_origin(v, origin)

    delta = rads_v - rads_start

    if delta < 0:
        delta += 2 * math.pi

    if minimum_chunk:
        delta = min([delta, math.pi * 2 - delta])

    return delta

def degrees_between(v: Tuple[float, float],
                    start: Tuple[float, float] = None,
                    origin: Tuple[float, float] = None,
                    minimum_chunk: bool = False) -> float:
    return rads_to_degrees(rads_between(v, start, origin, minimum_chunk))


def random_point_on_circle(center: Tuple[float, float], radius: float) -> Tuple[float, float]:
    rads = rnd.uniform(0, math.pi * 2)
    return point_at_angle(center, radius, radians=rads)

def random_point_in_circle(center: Tuple[float, float], radius: float) -> Tuple[float, float]:
    rads = rnd.uniform(0, math.pi * 2)
    pt = point_at_angle(center, radius, radians=rads)
    interp = rnd.random()

    x, y = interpolate(center, pt, interp)

    return x, y

def point_in_circle(center: Tuple[float, float], radius: float, pt: Tuple[float, float]) -> bool:
    return distance_between(center, pt) <= radius

def arc_length_ramanujans_approx(rad_start: float, rad_end: float, major_radius: float, minor_radius: float):
    # https://www.quora.com/How-do-you-compute-arc-length-of-ellipse
    p = math.pi * (3 * major_radius + 3 * minor_radius - math.sqrt((major_radius + 3 * minor_radius) * (minor_radius + 3 * major_radius)))
    rad_delta = rad_start - rad_end

    return p * rad_delta / (2 * math.pi)


if __name__ == "__main__":
    # a = (0,10)
    # b = (1, 0)
    # c = (-1, 0)
    #
    # print(from_boundary_points(a, b, c))

    pts = [
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1)
    ]
    o = (0, 0)

    for pt in pts:
        print(degrees_of_point_around_origin(pt, o))

    a = (0.5, 0.5)
    b = (-0.5, 0.5)
    print(degrees_between(b, a, minimum_chunk=False))
    print(degrees_between(a, b, minimum_chunk=False))
    print(degrees_between(b, a, minimum_chunk=True))
    print(degrees_between(a, b, minimum_chunk=True))
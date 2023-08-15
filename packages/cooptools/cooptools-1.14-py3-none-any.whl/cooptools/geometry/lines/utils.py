from typing import Tuple, List
import math
from cooptools.geometry.vectors.utils import det2x2, bounded_by, distance_between
from cooptools.common import verify_unique, verify_len_match, verify_len, verify

LINE_ENPOINT_MATHC_ERROR_MSG = "lines must have unique start and end points"

def verify_not_collinear(points: List[Tuple[float, float]], error_msg: str = None):
    verify(lambda: not collinear_points(points), f"points are collinear: {points}", error_msg)

def verify_collinear(points: List[Tuple[float, float]], error_msg: str = None):
    verify(lambda: collinear_points(points), f"points are not collinear: {points}", error_msg)

def line_intersection_2d(line1: Tuple[Tuple[float, float], Tuple[float, float]],
                         line2: Tuple[Tuple[float, float], Tuple[float, float]],
                         extend: bool = False):

    verify_unique(line1, LINE_ENPOINT_MATHC_ERROR_MSG)
    verify_unique(line2, LINE_ENPOINT_MATHC_ERROR_MSG)
    verify_len_match(line1, line2)
    verify_len(line1, 2)

    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    # handle meet at ends case:
    if line1[0] in [line2[0], line2[1]]:
        return line1[0]
    elif line1[1] in [line2[0], line2[1]]:
        return line1[1]

    # handle collinear lines
    verify_not_collinear([line1[0], line1[1], line2[0], line2[1]])

    # handle parallel lines
    div = det2x2(xdiff, ydiff)
    if div == 0:
        return None

    # find projected intersection
    d = (det2x2(*line1), det2x2(*line2))
    x = det2x2(d, xdiff) / div
    y = det2x2(d, ydiff) / div

    # handle if dont want to allow extended lines
    if not extend and \
        not all([
            bounded_by((x, y), line1[0], line1[1]),
            bounded_by((x, y), line2[0], line2[1])
        ]):
        return None

    return x, y

def line_length(line1: Tuple[Tuple[float, ...], Tuple[float, ...]]) -> float:
    verify_len_match(line1[0], line1[1])
    return distance_between(line1[0], line1[1])

def collinear_points(points: List[Tuple[float, float]]):

    if len(points) < 3:
        return True

    for ii in range(2, len(points)):
        verify_len(points[ii], 2)

        a = points[ii - 2]
        b = points[ii - 1]
        c = points[ii]
        tri_area = a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1])
        if math.isclose(tri_area, 0):
            continue
        else:
            return False

    return True

if __name__ == "__main__":
    line1 = ((0, 0), (1, 1))
    line2 = ((0, 1), (2, 10))

    print(line_intersection_2d(line1, line2, extend=True))
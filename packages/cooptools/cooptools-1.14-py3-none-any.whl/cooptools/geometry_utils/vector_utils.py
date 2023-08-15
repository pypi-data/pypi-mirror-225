from typing import Tuple, Optional, List
import math
import numpy as np
from cooptools.common import verify_len, verify_len_match, divided_length

FloatVec = Tuple[float, ...]

def homogeneous_vector(dim: int, val: float = None) -> FloatVec:
    if val is None:
        val = 0
    return tuple([val for x in range(dim)])

def identity_vector(dim: int) -> FloatVec:
    return homogeneous_vector(dim, 1)

def zero_vector(dim: int) -> FloatVec:
    return homogeneous_vector(dim)

def vector_between(start: FloatVec, end: FloatVec) -> FloatVec:
    verify_len_match(start, end)

    ret = []
    for idx in range(len(start)):
        ret.append((end[idx] - start[idx]))

    return tuple(ret)


def _add_two_vectors(a: FloatVec, b: FloatVec) -> FloatVec:
    mx = max(len(a), len(b))

    ret = []

    for ii in range(mx):
        if ii < len(a) and ii < len(b):
            ret.append(a[ii] + b[ii])
        elif ii < len(a):
            ret.append(a[ii])
        else:
            ret.append(b[ii])

    return tuple(ret)


def add_vectors(vectors: List[FloatVec], allow_diff_lengths: bool = False) -> FloatVec:
    running_sum = None

    for vec in vectors:
        if running_sum is None:
            running_sum = vec
        else:
            if not allow_diff_lengths:
                verify_len_match(running_sum, vec)

            running_sum = _add_two_vectors(running_sum, vec)

    return running_sum

def subtract_vectors(a: FloatVec, b: FloatVec, allow_diff_lengths: bool = False) -> FloatVec:
    b_calc = tuple(-1 * x for x in b)
    return add_vectors([a, b_calc], allow_diff_lengths=allow_diff_lengths)


def scale_vector_length(a: FloatVec, scale: float) -> FloatVec:
    scale_vector = homogeneous_vector(len(a), scale)
    return hadamard_product(a, scale_vector)


def vector_len(a: FloatVec) -> float:
    sum = 0
    for ii in a:
        sum += ii ** 2
    return math.sqrt(sum)

def distance_between(a: FloatVec, b: FloatVec) -> float:
    verify_len_match(a, b)

    vec_bet = vector_between(a, b)
    return vector_len(vec_bet)

def unit_vector(a: FloatVec) -> Optional[FloatVec]:
    vec_len = vector_len(a)
    if vec_len == 0:
        return None

    ret = []
    for coord in a:
        ret.append(coord / vec_len)
    return tuple(ret)

def scaled_to_length(a: FloatVec, desired_length: float) -> FloatVec:
    u_vec = unit_vector(a)

    if u_vec is None:
        return homogeneous_vector(len(a))

    ret = []
    for ii in range(len(u_vec)):
        ret.append(u_vec[ii] * desired_length)

    return tuple(ret)


def interpolate(a: FloatVec,
                b: FloatVec,
                amount: float = 0.5) -> FloatVec:

    delta_v = vector_between(start=a, end=b)
    scaled_delta_v = scale_vector_length(delta_v, amount)

    return add_vectors([a, scaled_delta_v])

def segmented_vector(inc: float,
                   start: FloatVec,
                   stop: FloatVec,
                   force_to_ends: bool = False) -> List[FloatVec]:

    delta = vector_between(start, stop)
    max_len = vector_len(delta)

    inc_vec = scaled_to_length(a=delta, desired_length=inc)

    ii = start
    vec_bet = vector_between(start, ii)
    vals = []
    while vector_len(vec_bet) <= max_len:
        vals.append(add_vectors([start, vec_bet]))
        ii = add_vectors([ii, inc_vec])
        vec_bet = vector_between(start, ii)

    # force to ends
    if force_to_ends:
        remaining_delta_vec = vector_between(vals[-1], stop)
        divided = scale_vector_length(remaining_delta_vec, 1 / (len(vals) - 1))
        vals = [add_vectors([x, scale_vector_length(divided, ii)]) for ii, x in enumerate(vals)]


    return vals




def absolute(a: FloatVec) -> FloatVec:
    ret = []
    for coord in range(len(a)):
        ret.append(abs(coord))

    return tuple(ret)

def dot(a: FloatVec,
        b: FloatVec) -> float:
    return float(np.dot(a, b))

def cross(a: FloatVec,
          b: FloatVec) -> FloatVec:
    return tuple(np.cross(a, b))


def hadamard_product(a: FloatVec,
                     b: FloatVec,
                     allow_different_lengths: bool = False) -> FloatVec:
    if not allow_different_lengths:
        verify_len_match(a, b)

    mx = max(len(a), len(b))

    ret = []
    for ii in range(mx):
        if ii < len(a) and ii < len(b):
            ret.append(a[ii] * b[ii])
        elif ii < len(a):
            ret.append(a[ii])
        else:
            ret.append(b[ii])

    return tuple(ret)


def hadamard_division(a: FloatVec,
                      b: FloatVec,
                      allow_different_lengths: bool = False) -> FloatVec:
    scale_vector = tuple([1 / val for val in b])
    return hadamard_product(a, scale_vector, allow_different_lengths)

def project_onto(a: FloatVec,
                 b: FloatVec,
                 origin: FloatVec = None) -> FloatVec:

    verify_len_match(a, b)

    if origin is None:
        origin = zero_vector(len(a))

    e1 = vector_between(origin, end=b)
    e2 = vector_between(origin, end=a)

    # https://gamedev.stackexchange.com/questions/72528/how-can-i-project-a-3d-point-onto-a-3d-line
    return add_vectors([origin, scale_vector_length(e1, dot(e2, e1) / dot(e1, e1))])

def pts_in_threshold(a: FloatVec,
                     pts: List[FloatVec],
                     distance_threshold: float = None) -> List[Tuple[FloatVec, float]]:
    if distance_threshold is not None and distance_threshold < 0:
        raise ValueError(f"distance_threshold must be greater than zero, but {distance_threshold} was provided")

    qualifiers = []
    for other in pts:
        distance = distance_between(a, other)
        if distance_threshold is None or distance < distance_threshold:
            qualifiers.append((other, distance))

    return qualifiers

def closest_point(a: FloatVec,
                  pts: List[FloatVec],
                  distance_threshold: float = None) -> Optional[FloatVec]:

    qualifiers = pts_in_threshold(a, pts, distance_threshold=distance_threshold)

    if len(qualifiers) == 0:
        return None

    min_dist = min([x[1] for x in qualifiers])

    return next(iter([x[0] for x in qualifiers if x[1] == min_dist]), None)

def bounded_by(a: FloatVec, b: FloatVec, c: FloatVec) -> bool:

    verify_len_match(a, b)
    verify_len_match(a, c)

    for ii in range(len(a)):
        min_val = min(b[ii], c[ii])
        max_val = max(b[ii], c[ii])

        if not min_val <= a[ii] <= max_val:
            return False

    return True

def point_in_polygon(point: Tuple[float, float], poly: List[Tuple[float, float]]):

    """
    Determine if the point is in the polygon.
    # https://en.wikipedia.org/wiki/Point_in_polygon#:~:text=One%20simple%20way%20of%20finding,an%20even%20number%20of%20times.
    # https://en.wikipedia.org/wiki/Even%E2%80%93odd_rule

    :param point: coordinates of point
    :param poly: a list of tuples [(x, y), (x, y), ...]
    :return: True if the point is in the path or is a corner or on the boundary
    """

    num = len(poly)
    j = num - 1
    c = False
    for i in range(num):
        if (point[0] == poly[i][0]) and (point[1] == poly[i][1]):
            # point is a corner
            return True
        if ((poly[i][1] > point[1]) != (poly[j][1] > point[1])):
            slope = (point[0]- poly[i][0]) * (poly[j][1] - poly[i][1]) - (poly[j][0] - poly[i][0]) * (point[1] - poly[i][1])
            if slope == 0:
                # point is on boundary
                return True
            if (slope < 0) != (poly[j][1] < poly[i][1]):
                c = not c
        j = i
    return c

def det2x2(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    verify_len(a, 2)
    verify_len(b, 2)

    return a[0] * b[1] - a[1] * b[0]

def orthogonal2x2(a: Tuple[float, float]) -> Tuple[float, float]:
    verify_len(a, 2)

    return (-a[1], a[0])

if __name__ == "__main__":
    v1 = (1, 0)
    v2 = (10, 10)

    ret = segmented_vector(1, start=v1, stop=v2, force_to_ends=True)
    print(ret)

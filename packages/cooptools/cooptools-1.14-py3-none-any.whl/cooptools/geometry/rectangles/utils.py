from typing import Tuple, Dict
from cooptools.geometry.vectors.utils import bounded_by, distance_between
from cooptools.coopEnum import CardinalPosition
from functools import partial

def rect_corners(rect: Tuple[float, float, float, float], cardinality: CardinalPosition = CardinalPosition.BOTTOM_LEFT) -> Dict[CardinalPosition, Tuple[float, float]]:
    x, y, w, h = rect

    if cardinality is None:
        cardinality = CardinalPosition.BOTTOM_LEFT

    partial_pos = partial(CardinalPosition.alignment_conversion,  dims=(w, h), anchor=(x, y), from_cardinality=cardinality)

    return {
        CardinalPosition.TOP_LEFT: partial_pos(to_cardinality=CardinalPosition.TOP_LEFT),
        CardinalPosition.TOP_RIGHT: partial_pos(to_cardinality=CardinalPosition.TOP_RIGHT),
        CardinalPosition.BOTTOM_RIGHT: partial_pos(to_cardinality=CardinalPosition.BOTTOM_RIGHT),
        CardinalPosition.BOTTOM_LEFT: partial_pos(to_cardinality=CardinalPosition.BOTTOM_LEFT)
    }

def rect_center(rect: Tuple[float, float, float, float]) -> Tuple[float, float]:
    x, y, w, h = rect
    return CardinalPosition.alignment_from_top_left(dims=(w, h),
                                                    top_left=(x, y),
                                                    cardinality=CardinalPosition.CENTER)

def rect_contains_point(rect: Tuple[float, float, float, float], pt: Tuple[float, float]) -> bool:
    x, y, w, h = rect
    return bounded_by(pt, (x, y), (x + w, y + h))

def overlaps(rect1: Tuple[float, float, float, float],
             rect2: Tuple[float, float, float, float]) -> bool:

    r1_corners = rect_corners(rect1)
    r2_corners = rect_corners(rect2)

    return any(rect_contains_point(rect1, pt) for card, pt in r2_corners.items()) or \
           any(rect_contains_point(rect2, pt) for card, pt in r1_corners.items())

def bounding_circle_radius(rect: Tuple[float, float, float, float]) -> float:
    x, y, w, h = rect
    center = CardinalPosition.alignment_from_top_left(dims=(w, h),
                                                    top_left=(x, y),
                                                    cardinality=CardinalPosition.CENTER)

    return distance_between((x, y), center)

if __name__ == "__main__":
    from pprint import pprint
    rect = 10, 10, 50, 100
    pprint(rect_corners(rect))

from cooptools.geometry.vectors.vectorN import Vector2
from typing import List, Callable, Dict
from cooptools.toggles import EnumToggleable
from cooptools.geometry.curves.enums import Orientation, CurveType
from cooptools.geometry.curves.curves import Curve, Arc, LineCurve, CubicBezier, CatmullRom

class CurveBuilder:

    def __init__(self, id_provider: Callable[[], str]):
        self.curves = {}  # {id: curve}
        self.current_points = []
        self.current_curve_type = EnumToggleable(CurveType)
        self.current_orientation = EnumToggleable(Orientation)
        self.id_provider = id_provider

    def add_curves(self, curves: Dict[str, Curve]):
        self.curves = {**self.curves, **curves}

    def set_curve_type(self, curve_type: CurveType):
        self.current_curve_type.set_value(curve_type)

    def toggle_curve_type(self):
        self.current_curve_type.toggle()
        self.current_points = []

    def saved_and_temp_from_next_points(self, next_points: List[Vector2]):
        curves = [curve for id, curve in self.curves.items()]
        curves += self.curves_from_temp_next_points(next_points)
        return curves

    def save_curve(self):
        new_curves, _ = self.curves_from_points(self.current_curve_type.value, self.current_points)

        new_curve_dict = {}
        for curve in new_curves:
            new_curve_dict[curve.id] = curve
            self.curves[curve.id] = curve
        self.current_points = []

        return new_curve_dict

    def add_point(self, point: Vector2):
        if self.current_curve_type.value == CurveType.CUBICBEZIER or \
            (len(self.current_points) == 0 or
                    (point != self.current_points[-1])):
            self.current_points.append(point)

    def remove_point(self):
        if any(self.current_points):
            self.current_points.pop()

    def curves_from_points(self, curve_type: CurveType, points: List[Vector2]) -> (List[Curve], List[Vector2]):
        # curves = []
        # leftover_points = []
        if len(points) < 2:
            return [], points

        if curve_type == CurveType.LINE:
            curves, leftover_points = LineCurve.from_points(points, self.id_provider)
        elif curve_type == CurveType.ARC:
            curves, leftover_points = Arc.from_points(points, self.id_provider)
        elif curve_type == CurveType.CUBICBEZIER:
            curves, leftover_points = CubicBezier.from_points(points, self.id_provider)
        elif curve_type == CurveType.CATMULLROM:
            curves, leftover_points = CatmullRom.from_points(points, self.id_provider)
        else:
            raise NotImplementedError(f"Curve type {curve_type} has not been implemented for generation from points")

        return curves, leftover_points

    def curves_from_temp_next_points(self, next_points: List[Vector2]):
        all_points = self.current_points + next_points
        points = []
        for i in all_points:
            points.append(i)

        curves, leftovers = self.curves_from_points(self.current_curve_type.value, points)
        return curves

    def force_continuity(self, next_point: Vector2, close_circuit: bool = False):
        curves, leftovers = self.curves_from_points(self.current_curve_type.value, self.current_points)

        if curves is None or len(curves) == 0:
            return next_point

        # Dont need to force a continuity if we are in the middle of a Bezier
        #       For closing a circuit, need to identify the second to last point of 4 points of the Bezier. Since we
        #       progress through a list of cubic beziers, this means that the end of the last curve is point 1, if there
        #       is only one leftover point, it is point 2. Meaning that we will be choosing the 3rd (second to last)
        #       point when there is one leftover point returned from the curve
        if close_circuit and len(leftovers) == 1:
            return curves[0].force_continuity(next_point, close_circuit)
        elif len(leftovers) != 0:
            return next_point
        else:
            return curves[-1].force_continuity(next_point)

if __name__ == "__main__":
    import random as rnd

    builder = CurveBuilder(lambda: "1")

    points = []

    rnd.seed(0)
    for ii in range(10):
        points.append(Vector2(rnd.randint(0, 100), rnd.randint(0, 100)))

    curves, leftover = builder.curves_from_points(curve_type=CurveType.CATMULLROM, points=points)

    curve = curves[0]
    catmullpoints = curve.compute_catmull_points([(x.x, x.y) for x in curve.ControlPoints])
    print(catmullpoints)
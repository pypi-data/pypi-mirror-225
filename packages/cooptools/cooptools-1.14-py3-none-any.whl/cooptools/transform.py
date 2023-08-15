import math
from typing import Tuple, Iterable, List
import cooptools.geometry_utils.vector_utils as vec
import cooptools.geometry_utils.circle_utils as circ
from cooptools.common import rads_to_degrees, degree_to_rads
from cooptools.matrixManipulation import rotateAroundPointMatrix, point_transform_3d

class Rotation:
    def __init__(self,
                 rads: Tuple[float, float, float] = None,
                 rotation_point: Tuple[float, float, float] = None
                 ):
        self._init_rads = rads if rads else (0, 0, 0)
        self._rotation_point = rotation_point if rotation_point else (0., 0., 0.)
        self._rads = None

        self.reset()

    def reset(self):
        self.update(rads=self._init_rads)

    @classmethod
    def from_rotation(cls, rotation):
        return Rotation(rads=rotation.Rads, rotation_point=rotation.RotationPoint)

    def __repr__(self):
        return str(self._rads)

    def update(self,
                rads: Tuple[float, float, float] = None,
                delta_rads: Tuple[float, float, float] = None,
                degrees: Tuple[float, float, float] = None,
                delta_degrees: Tuple[float, float, float] = None,
                rotation_point: Tuple[float, float, float] = None
                ):
        if rads is not None:
            self._rads = rads

        if delta_rads is not None:
            self._rads = tuple(map(lambda i, j: i + j, self._rads, delta_rads))

        # recursive call for degrees
        if degrees is not None or delta_degrees is not None:
            self.update(rads=tuple([degree_to_rads(x) for x in degrees]) if degrees else None,
                        delta_rads=tuple([degree_to_rads(x) for x in delta_degrees]) if delta_degrees else None)

        # set rotation point
        if rotation_point is not None:
            self._rotation_point = rotation_point

    def rotated_points(self, points: Iterable[Tuple[float, ...]], sig_dig: int = None) -> List[Tuple[float, ...]]:
        rM = rotateAroundPointMatrix(self._rotation_point, self._rads)

        return point_transform_3d(
            points=points,
            matrix = rM,
            sig_dig=sig_dig
        )

    @property
    def RotationPoint(self):
        return self._rotation_point

    @property
    def Rads(self):
        return self._rads

    @property
    def Degrees(self):
        return tuple(rads_to_degrees(x) for x in self._rads)

class Translation:
    def __init__(self,
                 init_translation_vector: Tuple[float, float, float] = None):
        self._init_translation_vector = init_translation_vector if init_translation_vector else (0, 0, 0)
        self._translation_vector = None
        self.reset()

    def reset(self):
        self.update(vector=self._init_translation_vector)

    def from_translation(self, translation):
        return Translation(init_translation_vector=translation.Vector)

    def __repr__(self):
        return str(self._translation_vector)

    def update(self,
               vector: Tuple[float, ...] = None,
               delta_vector: Tuple[float, ...] = None):
        if vector is not None:
            self._translation_vector = vector

        if delta_vector is not None:
            self._translation_vector = vec.add_vectors([self._translation_vector, delta_vector], allow_diff_lengths=True)

    @property
    def Vector(self):
        return self._translation_vector

class Scale:
    def __init__(self,
                 init_scale_vector: Tuple[float, float, float] = None
                 ):
        self._init_scale_vector = init_scale_vector if init_scale_vector else (1, 1, 1)
        self._scale_vector = None
        self.reset()

        self._scale_adjustment = (0, 0, 0)

    def from_scale(self, scale):
        return Scale(
            init_scale_vector=scale.Vector
        )

    def __repr__(self):
        return str(self._scale_vector)

    def reset(self):
        self.update(set_scale=self._init_scale_vector)

    def update(self,
               set_scale: Tuple[float, ...] = None,
               scalar: Tuple[float, ...] = None):
        if set_scale:
            self._scale_vector = set_scale

        if scalar is not None:
            self._scale_vector = vec.hadamard_product(self._scale_vector, scalar, allow_different_lengths=True)


    def scaled_points(self, points: Iterable[Tuple[float, ...]]) -> List[Tuple[float, ...]]:
        return [vec.hadamard_product(
            x,
            self._scale_vector,
            allow_different_lengths=True
        ) for x in points]

    @property
    def Vector(self):
        return self._scale_vector


class Transform:
    def __init__(self, translation: vec.FloatVec = None,
                 rotation: vec.FloatVec = None ,
                 scale: vec.FloatVec = None):
        self._translation: Translation = Translation(init_translation_vector=translation)
        self._rotation: Rotation = Rotation(rads=rotation)
        self._scale: Scale = Scale(init_scale_vector=scale)

    @classmethod
    def from_transform(cls, transform):
        return Transform(
            translation=transform.Translation.Vector,
            scale=transform.Scale.Vector,
            rotation=transform.Rotation.Rads
        )

    def translated_points(self, points: Iterable[Tuple[float, ...]]) -> List[Tuple[float, ...]]:
        return [vec.add_vectors(
            vectors=[x,
                    self._translation]
        )
        for x in points]

    def reset(self):
        self._scale.reset()
        self._translation.reset()
        self._rotation.reset()

    @property
    def Translation(self):
        return self._translation

    @property
    def Rotation(self):
        return self._rotation

    @property
    def Scale(self):
        return self._scale

    def __repr__(self):
        return f"T{self.Translation}, R{self.Rotation}, S{self.Scale}"


if __name__ == "__main__":
    s = Scale(init_scale_vector=(2, 2, 2))
    s.update(scalar=(3, 2, 1))
    print(s)

    r = Rotation(rads=(math.pi, 0, 0))
    p = (1, 1, 1)
    print(r.rotated_points([p]))

from typing import Dict, List, Tuple, Any
import cooptools.geometry.vectors.utils as vect
import cooptools.geometry.circles.utils as circ

class VectorN:
    @classmethod
    def from_vectorN(self, vecN):
        raise NotImplementedError()

    @classmethod
    def from_json(self, json):
        coords = {}
        for k, v in json.items():
            coords[k] = float(v)

        return VectorN(coords=coords)

    def __copy__(self):
        raise NotImplementedError()

    def __init__(self, coords: Dict[Any, float] = None):
        if coords is not None:
            self.coords: Dict[Any, float] = coords
        else:
            self.coords: Dict[Any, float] = {}

    def __getitem__(self, item):
        return self.coords[item]

    def __setitem__(self, key, value):
        self.coords[key] = value

    @classmethod
    def zero_of_degree(cls, other):
        new = VectorN()
        for ii, value in other.coords.items():
            new[ii] = 0
        return new

    def with_(self, x: float = None, y: float = None, z: float = None, updates: Dict[str, float] = None):

        cpy = self.__copy__()

        if x is not None:
            cpy.x = x

        if y is not None:
            cpy.y = y

        if z is not None:
            cpy.z = z

        for dim, val in updates.items():
            cpy[dim] = val

        return cpy

    @property
    def x(self):
        return self.coords.get('x', None)

    @x.setter
    def x(self, value):
        if 'x' in self.coords.keys():
            self.coords['x'] = value

    @property
    def y(self):
        return self.coords.get('y', None)

    @y.setter
    def y(self, value):
        if 'y' in self.coords.keys():
            self.coords['y'] = value

    @property
    def z(self):
        return self.coords.get('z', None)

    @z.setter
    def z(self, value):
        if 'z' in self.coords.keys():
            self.coords['z'] = value

    def degree(self):
        return len(self.coords)

    def unit(self):
        uv = vect.unit_vector(self.as_tuple())
        return VectorN(coords={key: uv[i] for i, key in enumerate(self.coords)})

    def length(self):
        return vect.vector_len(self.as_tuple())

    def distance_from(self, other):
        if not isinstance(other, VectorN) and not isinstance(other, Tuple):
            raise TypeError(f"type {other} cannot be distanced from {type(self)}")

        if issubclass(type(other), VectorN):
            other = other.as_tuple()

        return vect.distance_between(self.as_tuple(), other)

    def scaled_to_length(self, desired_length: float):
        scaled = vect.scaled_to_length(self.as_tuple(), desired_length)
        return VectorN(coords={key: scaled[i] for i, key in enumerate(self.coords)})

    def __eq__(self, other) -> bool:
        if not (isinstance(other, type(self)) or issubclass(type(other), type(self)) or issubclass(type(self), type(other))):
            return False


        for ii in self.coords.keys():
            if not self._is_close(self.coords[ii], other.coords[ii]):
                return False

        return True

    def __str__(self, n_digits: int = 2):
        ret = "<"
        ii = 0
        for key in self.coords.keys():
            if ii > 0:
                ret += ", "
            ret += f"{round(float(self.coords[key]), n_digits)}"
            ii +=1

        ret +=">"
        return ret

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(str(self))

    def __add__(self, other):
        if not (isinstance(other, type(self)) or issubclass(type(other), type(self)) or issubclass(type(self),
                                                                                                   type(other))):
            raise TypeError(f"Object of type [{type(other)}] cannot be added to {type(self)}")

        added = vect.add_vectors([self.as_tuple(), other.as_tuple()])
        return VectorN(coords={key: added[i] for i, key in enumerate(self.coords)})


    def __sub__(self, other):
        if not (isinstance(other, type(self)) or issubclass(type(other), type(self)) or issubclass(type(self), type(other))):
            raise TypeError(f"Object of type [{type(other)}] cannot be subtracted from {type(self)}")

        subtracted = vect.vector_between(other.as_tuple(), self.as_tuple())
        return VectorN(coords={key: subtracted[i] for i, key in enumerate(self.coords)})

    def __mul__(self, other):
        if not (isinstance(other, float) or isinstance(other, int)):
            raise TypeError(f"Object of type [{type(other)}] cannot be multiplied to {type(self)}")

        scaled = vect.scale_vector_length(self.as_tuple(), other)
        return VectorN(coords={key: scaled[i] for i, key in enumerate(self.coords)})

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if not (isinstance(other, float) or isinstance(other, int)):
            raise TypeError(f"Object of type [{type(other)}] cannot be divided from {type(self)}")

        scaled = vect.scale_vector_length(self.as_tuple(), 1 / other)
        return VectorN(coords={key: scaled[i] for i, key in enumerate(self.coords)})


    def _is_close(self, a:float, b:float, rel_tol=1e-09, abs_tol=0.0):
        return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

    def dot(self, other):
        if not (isinstance(other, type(self)) or issubclass(type(other), type(self)) or issubclass(type(self), type(other))):
            raise TypeError(f"type {other} cannot be dot multiplied by {type(self)}. Must match type...")

        return vect.dot(self.as_tuple(), other.as_tuple())


    def cross(self, other):
        if not (isinstance(other, type(self))
                or issubclass(type(other), type(self))
                or issubclass(type(self), type(other))
                or self.degree() != other.degree()):
            raise TypeError(f"type {other} cannot be cross multiplied by {type(self)}. Must match type...")

        crossed = vect.cross(self.as_tuple(), other.as_tuple())
        return VectorN({key: crossed[ii] for ii, (key, value) in enumerate(self.coords.items())})


    def degrees_from(self, other = None, origin = None, minimum_chunk = None):
        if not (isinstance(other, type(self)) or issubclass(type(other), type(self)) or issubclass(type(self), type(other)) or other is None):
            raise TypeError(f"type {other} cannot evaluate degrees between by {type(self)}. Must match type...")

        if origin and issubclass(type(origin), type(self)):
            origin = origin.as_tuple()

        if other is not None and issubclass(type(other), type(self)):
            other = other.as_tuple()

        return circ.degrees_between(v=self.as_tuple(), start=other, origin=origin, minimum_chunk=minimum_chunk)

    def rads_from(self, other = None, origin = None, minimum_chunk = None):
        if not (isinstance(other, type(self)) or issubclass(type(other), type(self)) or issubclass(type(self), type(other)) or other is None):
            raise TypeError(f"type {other} cannot evaluate degrees between by {type(self)}. Must match type...")

        if origin and issubclass(type(origin), type(self)):
            origin = origin.as_tuple()

        if other is not None and issubclass(type(other), type(self)):
            other = other.as_tuple()

        return circ.rads_between(v=self.as_tuple(), start=other, origin=origin, minimum_chunk=minimum_chunk)

    def hadamard_product(self, other):
        if type(other) == float or type(other) == int:
            return self.__mul__(other)

        if not (isinstance(other, type(self)) or issubclass(type(other), type(self)) or issubclass(type(self),
                                                                                                   type(other))):
            raise TypeError(f"type {other} cannot be hadamard multiplied by {type(self)}. Must match type...")

        hadp = vect.hadamard_product(self.as_tuple(), other.as_tuple())
        return VectorN({key: hadp[ii] for ii, (key, value) in enumerate(self.coords.items())})

    def hadamard_division(self, other, num_digits=None):
        if type(other) == float or type(other) == int:
            return self.__truediv__(other)

        if not (isinstance(other, type(self)) or issubclass(type(other), type(self)) or issubclass(type(self), type(other))):
            raise TypeError(f"type {type(other)} cannot be hadamard divided by {type(self)}. Must match type...\n"
                            f"{issubclass(type(other), type(self))}\n"
                            f"{issubclass(type(self), type(other))}")

        hadd = vect.hadamard_division(self.as_tuple(), other.as_tuple())
        return VectorN({key: hadd[ii] for ii, (key, value) in enumerate(self.coords.items())})

    def bounded_by(self, a, b) -> bool:
        if not isinstance(a, type(self)) and isinstance(b, type(self)):
            raise TypeError(f"a and b must match vector type: {type(self)}. {type(a)} and {type(b)} were given")

        return vect.bounded_by(self.as_tuple(), a.as_tuple(), b.as_tuple())


    def interpolate(self, other, amount: float = 0.5, interpolate_type: str = "linear" ):
        if not (isinstance(other, type(self)) or issubclass(type(other), type(self)) or issubclass(type(self), type(other))):
            raise TypeError(f"Cannot interpolate between objects of type {type(self)} and {type(other)}")

        if interpolate_type != "linear":
            raise NotImplementedError(f"Unimplemented interpolation type: {interpolate_type}")

        interp = vect.interpolate(self.as_tuple(), other.as_tuple(), amount=amount)
        return VectorN({key: interp[ii] for ii, (key, value) in enumerate(self.coords.items())})

    def absolute(self):
        abs = vect.absolute(self.as_tuple())
        return VectorN({key: abs[ii] for ii, (key, value) in enumerate(self.coords.items())})

    def project_onto(self, other, origin=None):
        if not (isinstance(other, type(self)) or issubclass(type(other), type(self)) or issubclass(type(self),
                                                                                                   type(other))):
            raise TypeError(f"type {other} cannot be projected onto {type(self)}. Must match type...")

        projected = vect.project_onto(self.as_tuple(), other.as_tuple(), origin.as_tuple())
        return VectorN({key: projected[ii] for ii, (key, value) in enumerate(self.coords.items())})

    def closest_within_threshold(self, other_points: List, distance_threshold: float = None):
        qualify = vect.closest_point(self.as_tuple(), [x.as_tuple() for x in other_points], distance_threshold=distance_threshold)

        if qualify is None:
            return None

        return VectorN({key: qualify[ii] for ii, (key, value) in enumerate(self.coords.items())})

    def as_tuple(self) -> Tuple[float, ...]:
        return tuple([v for k, v in self.coords.items()])

class Vector2 (VectorN):
    @classmethod
    def from_vectorN(cls, vecN: VectorN):
        return Vector2(vecN.x, vecN.y)

    @classmethod
    def from_vector3(cls, vec3):
        if not type(vec3) == Vector3:
            raise TypeError(f"input type must be {type(Vector3)} but type [{type(vec3)}] was provided")
        return Vector2(vec3.x, vec3.y)

    @classmethod
    def from_tuple(cls, tup: Tuple[float, float]):
        if len(tup) < 2:
            raise ValueError(f"Can only create a Vector2 from a float tuple of size 2 or more. {tup} provided")

        x = float(tup[0])
        y = float(tup[1])

        return Vector2(x, y)

    def __copy__(self):
        return Vector2(self.x, self.y)

    def __init__(self, x: float, y: float):
        VectorN.__init__(self)
        self.coords['x'] = x
        self.coords['y'] = y

    def in_polygon(self, poly: List[VectorN]):
        return vect.point_in_polygon(self.as_tuple(), [x.as_tuple()[:2] for x in poly])

class Vector3(VectorN):
    @classmethod
    def from_vectorN(cls, vecN: VectorN):
        return Vector3(vecN.x, vecN.y, vecN.z)

    @classmethod
    def from_vector2(cls, vec2: Vector2, z: float = 0):
        if not type(vec2) == Vector2:
            raise TypeError(f"input type must be {type(Vector2)} but type [{type(vec2)}] was provided")

        return Vector3(vec2.x, vec2.y, z)

    @classmethod
    def from_tuple(cls, tup: Tuple[float, float, float]):
        if len(tup) < 3:
            raise ValueError(f"Can only create a Vector3 from a float tuple of size 3 or more. {tup} provided")

        x = float(tup[0])
        y = float(tup[1])
        z = float(tup[2])

        return Vector3(x, y, z)

    def __copy__(self):
        return Vector3(self.x, self.y, self.z)

    def __init__(self, x: float, y: float, z: float):
        VectorN.__init__(self)
        self.coords['x'] = x
        self.coords['y'] = y
        self.coords['z'] = z

if __name__ == "__main__":
    poly = [
        Vector2(2, 2),
        Vector2(3, 3),
        Vector2(2, 3),
        Vector2(3, 2)
    ]

    point = Vector2(2.5, 2.5)

    print(point.in_polygon(poly))

    point = Vector2(1, 1)
    print(point.in_polygon(poly))
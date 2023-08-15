import time

import numpy as np
from typing import Iterable, Tuple, List

def rotation_unit_vector(axis: np.array):
    return axis / (axis ** 2).sum() ** 0.5

def translationMatrix(dx=0, dy=0, dz=0):
    """ Return matrix for translation along vector (dx, dy, dz). """
    return np.array([[1, 0, 0, dx],
                     [0, 1, 0, dy],
                     [0, 0, 1, dz],
                    [0, 0, 0, 1]])

def scaleMatrix(sx=0, sy=0, sz=0):
    """ Return matrix for scaling equally along all axes centred on the point (cx,cy,cz). """

    return np.array([[sx, 0, 0, 0],
                     [0, sy, 0, 0],
                     [0, 0, sz, 0],
                     [0, 0, 0, 1]])


def rotateXMatrix(radians, right_handed: bool = False):
    """ Return matrix for rotating about the x-axis by 'radians' radians """
    c = np.cos(radians)
    s = np.sin(radians)
    arr = np.array([[1, 0, 0, 0],
                     [0, c, -s, 0],
                     [0, s, c, 0],
                     [0, 0, 0, 1]])

    if right_handed:
        arr = np.transpose(arr)

    return arr


def rotateYMatrix(radians, right_handed: bool = False):
    """ Return matrix for rotating about the y-axis by 'radians' radians """
    c = np.cos(radians)
    s = np.sin(radians)
    arr = np.array([[c, 0, s, 0],
                     [0, 1, 0, 0],
                     [-s, 0, c, 0],
                     [0, 0, 0, 1]])

    if right_handed:
        arr = np.transpose(arr)

    return arr


def rotateZMatrix(radians, right_handed: bool = False):
    """ Return matrix for rotating about the z-axis by 'radians' radians """
    c = np.cos(radians)
    s = np.sin(radians)
    arr = np.array([[c, -s, 0, 0],
                     [s, c, 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])

    if right_handed:
        arr = np.transpose(arr)

    return arr


def rotateAroundArbitraryAxis(rotationPoint, rotationAxis, radians, right_handed: bool = False):
    """
    The intent is to generate a matrix that rotate points around an arbitrary axis in space

    :param rotationPoint:
    :param rotationVector:
    :param right_handed:
    :return:
    """

    # http://www.fastgraph.com/makegames/3drotation/
    # https://sites.google.com/site/glennmurray/Home/rotation-matrices-and-formulas/rotation-about-an-arbitrary-axis-in-3-dimensions

    """http://www.fastgraph.com/makegames/3drotation/"""
    c = np.cos(radians)
    s = np.sin(radians)
    t = 1 - np.cos(radians)
    u = rotationAxis[0]
    v = rotationAxis[1]
    w = rotationAxis[2]


    ''' Build the transposes into the matrix'''
    x=rotationPoint[0]
    y=rotationPoint[1]
    z= rotationPoint[2]

    ''' <This is a right-handed matrix> '''
    calculated_matrix = np.array([[u**2 + (v**2 + w**2) * c, u*v*t-w*s,              u*w*t+v*s,              (x*(v**2 + w**2) - u*(y*v + z*w))*t + (y*w-z*v)*s],
                                 [u*v*t + w*s,              v**2 + (u**2 + w**2)*c, v*w*t-u*s,              (y*(u**2 + w**2) - v*(x*u + z*w))*t + (z*u-x*w)*s],
                                 [u*w*t - v*s,              v*w*t + u*s,            w**2 + (u**2 + v**2)*c, (z*(u**2 + v**2) - w*(x*u + y*v))*t + (x*v-y*u)*s],
                                 [0,                        0,                      0,                      1]])

    # do the transpose to align with all the other orientation requirements
    if right_handed:
        calculated_matrix = np.transpose(calculated_matrix)

    return calculated_matrix



# def get_grid_rotation_matrix(rotation_axis_x, rotation_axis_z, x_rot_rads, z_rot_rads):
#     # Rot Z
#     orientation = np.array([0, 0, 1])
#     ruv = rotation_unit_vector(orientation)
#     matrixz = rotateAroundAxis((rotation_axis_x, rotation_axis_z, 0), ruv, z_rot_rads)
#
#     # Rot X
#     orientation = np.array([1, 0, 0])
#     ruv = rotation_unit_vector(orientation)
#     matrixx = rotateAroundAxis((rotation_axis_x, rotation_axis_z, 0), ruv,
#                                   x_rot_rads)
#     matrix = matrixx.dot(matrixz)
#     return matrix


def rotateAroundPointMatrix(rotationPoint, rotationVector, right_handed: bool = False):
    """
    The intent is to generate a matrix that will move to origin, rotateX, rotateY, rotateZ, then move back

    :param rotationPoint:
    :param rotationVector:
    :param right_handed:
    :return:
    """


    translationM = translationMatrix(-rotationPoint[0], -rotationPoint[1], -rotationPoint[2])
    translationMInv = translationMatrix(rotationPoint[0], rotationPoint[1], rotationPoint[2])
    rX = rotateXMatrix(rotationVector[0])
    rY = rotateYMatrix(rotationVector[1])
    rZ = rotateZMatrix(rotationVector[2])


    if right_handed:
        return translationM.dot(rX.dot(rY.dot(rZ.dot(translationMInv))))
    else:
        return translationMInv.dot(rZ.dot(rY.dot(rX.dot(translationM))))


def scaleAroundPointMatrix(point, scalarVector):
    translationM = translationMatrix(-point[0], -point[1], -point[2])
    translationMInv = translationMatrix(point[0], point[1], point[2])
    scaleM = scaleMatrix(*scalarVector)
    matrix = translationMInv.dot(scaleM.dot(translationM))

    with np.printoptions(precision=3, suppress=True):
        print(f"Scalar \n{matrix}")
    return matrix


def rotate2dM(rads):
    return rotateZMatrix(rads)

def point_transform_3d(points: Iterable[Tuple[float, ...]], lh_matrix=None, sig_dig: int = None) -> List[Tuple[float, ...]]:
    """
    The goal here is to perform the following operation lh_Matrix * points = points`

    :param points:
    :param lh_matrix:
    :param sig_dig:
    :return:
    """

    def point_lam(x):
        lst = list(x)

        while len(lst) < 3:
            lst.append(0)

        return tuple(lst)

    np_points = [point_lam(point) for point in points]

    scaled = scaled_array(np.array(np_points),
                          lh_matrix=lh_matrix,
                          sig_dig=sig_dig)

    if scaled.size == 0:
        return []

    ret = [
        tuple(x) for x in scaled[:,:3]
    ]


    return ret

def scaled_array(lst_point_array: np.ndarray,
                 lh_matrix=None,
                 sig_dig = None):
    if len(lst_point_array) == 0:
        return np.array([])

    if lst_point_array.shape[1] < 4:
        lst_point_array = np.hstack((lst_point_array, np.ones(shape=(lst_point_array.shape[0], 1))))

    if lh_matrix is None:
        lh_matrix = np.identity(4)

    '''Multiply the points by the transform matrix for drawing'''
    transformed_points = lh_matrix.dot(
        np.transpose(lst_point_array))  # Transpose the points to appropriately mutiply

    # round
    if sig_dig is not None:
        transformed_points = np.round(transformed_points, sig_dig)


    return np.transpose(transformed_points)[:,
           :3]  # Re-Transpose the points back to remain in a "list of points" format


if __name__ == "__main__":
    import math

    # print(rotateAroundArbitraryAxis((0, 0, 0,), (0, 0, 1), math.pi / 2))
    # print(rotateAroundPointMatrix((0, 0, 0), (math.pi / 2, 0, math.pi / 2)))

    assert point_transform_3d([(1, 0, 0)], lh_matrix=rotateZMatrix(math.pi / 2), sig_dig=0)[0] == (0.0, 1.0, 0.0)
    assert point_transform_3d([(1, 0, 0)], lh_matrix=rotateXMatrix(math.pi / 2), sig_dig=0)[0] == (1.0, 0.0, 0.0)
    assert point_transform_3d([(1, 0, 0)], lh_matrix=rotateYMatrix(math.pi / 2), sig_dig=0)[0] == (0.0, 0.0, -1.0)

    assert point_transform_3d([(0, 1, 0)], lh_matrix=rotateZMatrix(math.pi / 2), sig_dig=0)[0] == (-1, 0.0, 0.0)
    assert point_transform_3d([(0, 1, 0)], lh_matrix=rotateXMatrix(math.pi / 2), sig_dig=0)[0] == (0, 0.0, 1)
    assert point_transform_3d([(0, 1, 0)], lh_matrix=rotateYMatrix(math.pi / 2), sig_dig=0)[0] == (0.0, 1, 0)

    assert point_transform_3d([(0, 0, 1)], lh_matrix=rotateZMatrix(math.pi / 2), sig_dig=0)[0] == (0.0, 0, 1)
    assert point_transform_3d([(0, 0, 1)], lh_matrix=rotateXMatrix(math.pi / 2), sig_dig=0)[0] == (0, -1, 0.0)
    assert point_transform_3d([(0, 0, 1)], lh_matrix=rotateYMatrix(math.pi / 2), sig_dig=0)[0] == (1, 0.0, 0)

    assert np.array_equal(rotateZMatrix(0.5), rotateAroundArbitraryAxis((0, 0, 0,), (0, 0, 1), 0.5))
    assert np.array_equal(rotateXMatrix(0.5), rotateAroundArbitraryAxis((0, 0, 0,), (1, 0, 0), 0.5))
    assert np.array_equal(rotateYMatrix(0.5), rotateAroundArbitraryAxis((0, 0, 0,), (0, 1, 0), 0.5))

from cooptools.common import next_perfect_square_rt
from typing import Tuple

def square_sector_def(n_sectors: int) -> (int, int):
    """
    :param n_sectors: the min number of sectors that must be created
    :return: (rows, cols)
    """
    next_sq_rt = next_perfect_square_rt(n_sectors)
    return (next_sq_rt, next_sq_rt)
import math
import uuid
from typing import List, Union, Tuple, Iterable, Callable, Sequence, Protocol
import itertools
import struct
import imghdr
import numpy as np
import bisect

class Comparable(Protocol):
    def __lt__(self, other):
        pass

    def __gt__(self, other):
        pass

    def __eq__(self, other):
        pass

    def __ge__(self, other):
        pass

    def __le__(self, other):
        pass

    def __ne__(self, other):
        pass

def flattened_list_of_lists(list_of_lists: Iterable[Iterable], unique: bool = False) -> List:
    flat = list(itertools.chain.from_iterable(list_of_lists))

    if unique:
        flat = list(set(flat))

    return flat

def all_indxs_in_lst(lst: List, value) -> List[int]:
    idxs = []
    idx = -1
    while True:
        try:
            idx = lst.index(value, idx + 1)
            idxs.append(idx)
        except ValueError as e:
            break
    return idxs

def next_perfect_square_rt(n: int) -> int:
    int_root_n = int(math.sqrt(n))
    if int_root_n == n:
        return n
    return int_root_n + 1

def try_resolve_guid(id: str) -> Union[str, uuid.UUID]:

    try:
        return uuid.UUID(id)
    except:
        return id

def split_strip(txt: str):
    return [x.strip() for x in txt.split(',')]

def duplicates_in_list(lst: Iterable) -> List:
    res = list(set([ele for ele in lst
                    if list(lst).count(ele) > 1]))
    return res


def verify(verify_func: Callable, msg: str=None, msg_sub: str=None, block: bool=True):
    if msg_sub is not None:
        msg += f"\n\t{msg_sub}"

    result = verify_func()

    if not result and block:
        raise ValueError(msg)
    elif not result:
        print(msg)

    return result

def verify_val(val: Comparable,
               low: Comparable = None,
               low_inc: Comparable = None,
               hi: Comparable = None,
               hi_inc: Comparable = None,
               error_msg: str = None,
               block: bool = True) -> bool:

    if low_inc is not None:
        low_tst = lambda: val >= low_inc
        low_txt = f"{low_inc} <="
    elif low is not None:
        low_tst = lambda: val > low
        low_txt = f"{low} <"
    else:
        low_tst = lambda: True
        low_txt = f""

    if hi_inc is not None:
        hi_tst = lambda: val <= hi_inc
        hi_txt = f"<= {hi_inc}"
    elif hi is not None:
        hi_tst = lambda: val < hi
        hi_txt = f"< {hi}"
    else:
        hi_tst = lambda: True
        hi_txt = ""

    tst = lambda:  low_tst() and hi_tst()

    msg = f"invalid value: {low_txt} {val} {hi_txt} is not valid"
    return verify(tst, msg, msg_sub=error_msg, block=block)




def verify_unique(lst: Iterable, error_msg: str = None):
    dups = duplicates_in_list(lst)

    tst = lambda: len(dups) == 0
    msg = f"All the values are not unique. Dups: {dups}"
    verify(tst, msg, error_msg)

def verify_len_match(iterable1, iterable2, error_msg: str = None):
    msg = f"{iterable1} and {iterable2} do not have the same length ({len(iterable1)} vs {len(iterable2)})"

    tst = lambda: len(iterable1) == len(iterable2)
    verify(tst, msg, error_msg)


def verify_len(iterable, length: int, error_msg: str = None):
    msg = f"{iterable} does not have len {length} ({len(iterable)})"

    tst = lambda: len(iterable) == length
    verify(tst, msg, error_msg)

def degree_to_rads(degrees: float) -> float:
    return degrees * math.pi / 180

def rads_to_degrees(rads: float) -> float:
    return rads * 180 / math.pi


def bounding_box_of_points(pts: Sequence[Tuple[float, float]]) -> Tuple[float, float, float, float]:
    min_x = min([p[0] for p in pts])
    max_x = max([p[0] for p in pts])
    min_y = min([p[1] for p in pts])
    max_y = max([p[1] for p in pts])

    w = max_x - min_x
    h = max_y - min_y

    return (min_x, min_y, w, h)

def divided_length(inc: float,
                   start: float = None,
                   start_inc: float = None,
                   stop: float = None,
                   stop_inc: float = None,
                   force_to_ends: bool = False) -> List[float]:
    vals = []

    s = start or start_inc
    e = stop or stop_inc

    if s <= e:
        tst = lambda val: verify_val(val, low=start, low_inc=start_inc, hi=stop, hi_inc=stop_inc, block=False)
    else:
        tst = lambda val: verify_val(val, low=stop, low_inc=stop_inc, hi=start, hi_inc=start_inc, block=False)
        inc *= -1

    ii = s
    while tst(ii):
        vals.append(ii)
        ii += inc

    # force to ends
    if force_to_ends:
        remaining_delta = abs(e - vals[-1])
        vals = [x + remaining_delta / (len(vals) - 1) * (ii) for ii, x in enumerate(vals)]

    return vals

def property_name(prop:str):
    return prop.split('=')[0].replace('self.', '').replace('cls.', '')

def get_image_size(fname):
    '''Determine the image type of fhandle and return its size.
    from draco'''
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return
            width, height = struct.unpack('>ii', head[16:24])
        elif imghdr.what(fname) == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        elif imghdr.what(fname) == 'jpeg':
            try:
                fhandle.seek(0)  # Read 0xff next
                size = 2
                ftype = 0
                while not 0xc0 <= ftype <= 0xcf:
                    fhandle.seek(size, 1)
                    byte = fhandle.read(1)
                    while ord(byte) == 0xff:
                        byte = fhandle.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', fhandle.read(2))[0] - 2
                # We are at a SOFn block
                fhandle.seek(1, 1)  # Skip `precision' byte.
                height, width = struct.unpack('>HH', fhandle.read(4))
            except Exception:  # IGNORE:W0703
                return
        else:
            return
        return width, height

def geo_mean(iterable: Iterable):
    a = np.array(iterable)
    return a.prod() ** (1.0 / len(a))

def from_schema(schema, **kwargs):
    definition = schema.__dict__
    for kwarg, val in kwargs.items():
        definition[kwarg] = val

    return type(schema)(**definition)

def insert_sorted_list(list, n):
    bisect.insort(list, n)
    return list

def cross_apply(items: Iterable[Iterable]) -> Iterable[Tuple]:
    return [x for x in itertools.product(*items)]






if __name__ == "__main__":
    # print(bucket_datestamp([datetime.datetime.now()], grouping_method=DateGroupingType.YEAR))
    pass

    items = [
        ['a', 'b', 'c'],
        [1, 2],
        ["hello", "fresh"]
    ]
    print(cross_apply(items))
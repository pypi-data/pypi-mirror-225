import os
import shutil
import logging
import json
from enum import Enum
from typing import List, Tuple, Union, Callable
import ntpath
import struct
import imghdr

LOCALAPP_ROOT = 'LOCALAPPDATA'
logger = logging.getLogger('cooptools.os_manip')

class FileType(Enum):
    JSON = ".json"
    TXT = ".txt"
    CSV = ".csv"
    INI = ".ini"


def files_at_dir(directory):
    # iterate over files in
    # that directory
    ret = []
    for filename in os.scandir(directory):
        if filename.is_file():
            ret.append(rf"{directory}\{filename.name}")
    return ret

filePathProvider = Union[str, Callable[[], str]]

def resolve_absolute_filepath(file_path: filePathProvider):
    if file_path is None:
        return None

    fp = None
    if type(file_path) == str:
        fp = file_path
    else:
        try:
            fp = file_path()
        except Exception as e:
            logger.error(f"Unable to resolve the file path: {e}")
            raise e

    afp = os.path.abspath(fp)
    logger.debug(f"The resolved absolute filepath to be used: {afp}")
    return afp



def check_file_exists(file_path: filePathProvider):
    fp = resolve_absolute_filepath(file_path)
    return fp is not None and os.path.exists(fp)

def verify_file_exists(file_path: filePathProvider):
    # verify path exists
    if not check_file_exists(file_path):
        raise Exception(f"No valid file at {resolve_absolute_filepath(file_path)}")


def path_and_file(filepath: str):
    head, tail = ntpath.split(filepath)
    tail = tail or ntpath.basename(head)
    return head, tail

def copy_file_from_to(filepath_to_copy: str, to_filepath: str):
    shutil.copy2(filepath_to_copy, to_filepath)


def write_data(data, file_path, make_dir: bool = True):
    if make_dir:
        check_and_make_dirs(os.path.dirname(file_path))

    with open(file_path, 'w') as outfile:
        ret = outfile.write(data)
        return ret


def read_data(file_path, lines: bool=False):
    with open(file_path, 'r+') as outfile:
        if lines:
            ret = outfile.readlines()
        else:
            ret = outfile.read()
        return ret


def try_write_data(data, file_path):
    ret = None
    try:
        ret = write_data(data=data, file_path=file_path)
    except Exception as e:
        logging.error(f"Unable to write file: {file_path}: {e}")

    return ret


def try_read_data(file_path):
    ret = None
    try:
        ret = read_data(file_path)
    except Exception as e:
        logging.error(f"Unable to read file: {file_path}: {e}")
    return ret

def rename_files(filepaths: List[str],
                 replace: List[Tuple[str, str]] = None,
                 remove_spaces: bool = False):
    for path in filepaths:
        src = path
        path, filename = path_and_file(path)

        new = filename
        for rep in replace or []:
            new = new.replace(rep[0], rep[1])

        if remove_spaces:
            new = new.replace(' ', '')

        os.rename(src=src, dst=fr"{path}\{new}")

def check_and_make_new_proj_localapp(app_root, proj_name):
    """ Verifies that the app_root exists at LOCALAPPDATA and then verifies that a subfolder exists at that directory
    for the proj_name.
    :return the full directory path to the proj_name
    """
    root = check_and_make_localapp_application_path_dir(app_root)
    return check_and_make_proj_path_dir(root, proj_name)


def root_and_name(root, name):
    """ Combines the root with the provided name to create a new directory or filepath
    :return string of the new directory or filepath"""
    return f"{root}\\{name}"


def check_and_make_proj_path_dir(root, proj_name):
    """Verifies that the directory at the provided root and proj_name exist
    :return the directory path"""
    proj_dir = root_and_name(root, proj_name)
    check_and_make_dirs(proj_dir)

    return proj_dir


def localapp_root(app_name):
    """ Returns the string of the directory that would be in the LOCALAPPDATA for the given app name"""
    local_app_data = os.getenv(LOCALAPP_ROOT)
    return f"{local_app_data}\\{app_name}"


def localapp_root_exists(app_name):
    """ Checks if the directory exists for the app_name in the LOCALAPPDATA"""
    dir = localapp_root(app_name)
    return os.path.isdir(dir)


def proj_dir(app_name, proj_name):
    """ Returns the string for a subfolder in the app root within LOCALAPPDATA"""
    app_root = localapp_root(app_name)
    return root_and_name(app_root, proj_name)


def proj_exists(app_name, proj_name):
    """ Checks if the directory exists for a subfolder within the app_name folder in LOCALAPPDATA"""
    return os.path.isdir(proj_dir(app_name, proj_name))


def check_and_make_dirs(dir):
    """ Checks if a directory exists, if not creates it
    :return the path to the directory
    """
    chk = os.path.isdir(dir)
    if not chk:
        os.makedirs(dir)
    return dir


def check_and_make_localapp_application_path_dir(application_root):
    """ Verifies the application_root folder exists in the LOCALAPPDATA
    :return path to the verified root
    """
    la_root = localapp_root(application_root)
    check_and_make_dirs(la_root)
    return la_root


def clean_file_type(file_path, file_type: FileType = None):
    if file_type is not None:
        split_string = file_path.split('.', 1)
        file_path = split_string[0] + str(file_type.value)

    return file_path

def create_file(file_path, file_type: FileType = None, lines: List = None):
    if file_type is not None:
        file_path = clean_file_type(file_path, file_type)

    with open(file_path, 'w') as outfile:
        try:
            if lines:
                outfile.writelines(lines)
        except Exception as e:
            logging.error(f"Unable to write file: {file_path}: {e}")

def read_file(file_path, as_lines: bool=False):
    with open(file_path, 'r') as readable:
        try:
            if as_lines:
                ret = readable.readlines()
            else:
                ret = readable.read()
            return ret
        except Exception as e:
            logging.error(f"Unable to read file: {file_path}: {e}")

def filepath_at_check_and_make_dir(dir, file_name, file_type: FileType = None):
    check_and_make_dirs(dir)
    file_path = f"{dir}\\{file_name}"
    return clean_file_type(file_path, file_type)


def filepath_at_dir(app_root,
                    file_name,
                    proj_name=None,
                    file_type: FileType = None,
                    make_dirs: bool = True,
                    make_file: bool = True):

    # get the local app root with app root
    path = localapp_root(app_root)

    # append proj name dir if provided
    if proj_name is not None:
        path = root_and_name(path, proj_name)

    # make proj dir
    if make_dirs:
        check_and_make_dirs(path)

    # clean the filename
    clean_filename = clean_file_type(file_name, file_type)

    # get full path
    path = root_and_name(path, clean_filename)

    # make file
    if make_file:
        create_file(path, file_type=file_type)

    return path

def filepath_at_check_and_make_app_dir(app_root, file_name, file_type: FileType = None):
    app_path = localapp_root(app_root)
    return filepath_at_check_and_make_dir(app_path, file_name, file_type)


def filepath_at_check_and_make_app_proj_dir(app_root, proj_name, file_name, file_type: FileType = None):
    proj_path = check_and_make_new_proj_localapp(app_root, proj_name)
    return filepath_at_check_and_make_dir(proj_path, file_name, file_type)

def try_save_jsonable_data(my_jsonable_data, file_path, cls: json.JSONEncoder = None):
    accepted_method_names = ['toJson', 'to_json', 'tojson']
    to_json_method = next(iter(getattr(my_jsonable_data, x, None) for x in accepted_method_names), None)
    if to_json_method and callable(to_json_method):
        data = to_json_method()
    else:
        data = json.dumps(my_jsonable_data, indent=4, cls=cls)

    return try_write_data(data, file_path)


def load_json_data_to_dict(file_path, cls: json.JSONEncoder = None):
    data = read_data(file_path)
    ret = json.loads(data, cls=cls)
    return ret


def try_load_json_data_to_dict(file_path, cls: json.JSONEncoder = None):
    data = try_read_data(file_path)
    ret = None
    if data is not None:
        ret = json.loads(data, cls=cls)

    return ret

def save_application_json(my_jsonable_data, app_root, filename: str):
    file_path = filepath_at_check_and_make_app_dir(app_root, filename, file_type=FileType.JSON)
    return try_save_jsonable_data(my_jsonable_data, file_path)


def save_project_json(my_jsonable_data, app_root, project_name, filename: str):
    file_path = filepath_at_check_and_make_app_proj_dir(app_root, project_name, filename, file_type=FileType.JSON)
    return try_save_jsonable_data(my_jsonable_data, file_path)


def load_application_json(app_root, filename):
    file_path = filepath_at_check_and_make_app_dir(app_root, filename, file_type=FileType.JSON)
    return try_load_json_data_to_dict(file_path)


def load_project_json(app_root, project, filename):
    proj_dir = check_and_make_new_proj_localapp(app_root, project)
    file_path = f"{proj_dir}\\{filename}.json"
    return try_load_json_data_to_dict(file_path)



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

if __name__ == "__main__":


    files = files_at_dir(r'C:\Users\tburns\Downloads\zombiefiles\png\male')
    rename_files(filepaths=files, replace=[('(', '__0'),
                                           (')', ''),
                                           ('010', '10'),
                                           ('011', '11'),
                                           ('012', '12'),
                                           ('013', '13'),
                                           ('014', '14'),
                                           ('015', '15')], remove_spaces=True)

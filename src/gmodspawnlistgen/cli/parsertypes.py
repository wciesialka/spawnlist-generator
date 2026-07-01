from gmodspawnlistgen.exceptions import InvalidPathException
from os import access, R_OK, W_OK, X_OK

def existing_directory_path(path: Path):
    if not isinstance(path, Path):
        try:
            path = Path(path)
        except:
            raise TypeError(f"Must be type Path, not {type(path)}")
        else:
            return readable_directory_path(path)
    if not path.exists():
        raise InvalidPathException(path, "Does not exist")
    if not path.is_dir():
        raise InvalidPathException(path, "Is not a directory")
    return path

def existing_file_path(path: Path):
    if not isinstance(path, Path):
        try:
            path = Path(path)
        except:
            raise TypeError(f"Must be type Path, not {type(path)}")
        else:
            return readable_directory_path(path)
    if not path.exists():
        raise InvalidPathException(path, "Does not exist")
    if not path.is_file():
        raise InvalidPathException(path, "Is not a file")
    return path

def existing_readable_file_path(path: Path):
    if not isinstance(path, Path):
        try:
            path = Path(path)
        except:
            raise TypeError(f"Must be type Path, not {type(path)}")
        else:
            return readable_directory_path(path)
    if not path.exists():
        raise InvalidPathException(path, "Does not exist")
    if not path.is_file():
        raise InvalidPathException(path, "Is not a file")
    if not access(path, R_OK):
        raise InvalidPathException(path, "Is not readable")
    return path

def readable_writeable_path(path: Path):
    if not isinstance(path, Path):
        try:
            path = Path(path)
        except:
            raise TypeError(f"Must be type Path, not {type(path)}")
        else:
            return readable_directory_path(path)
    if not access(path, W_OK):
        raise InvalidPathException(path, "Is not writeable")
    if not access(path, R_OK) and path.exists():
        raise InvalidPathException(path, "Exists but is not readable")
    return path
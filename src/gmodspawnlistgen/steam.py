import os
import sys
import platform
from shutil import which
from pathlib import Path
from gmodspawnlistgen.exceptions import InvalidSteamPathException, NoSteamRootException
from gmodspawnlistgen.valvetable import ValveTableFile

class SteamFileHandler:

    def __init__(self, root_path: Path):
        self.__root = None
        self.root = root_path
    
    @property
    def root(self):
        return self.__root
    
    @root.setter
    def root(self, new_path):
        if new_path is None:
            self.__executable_path = None
            return
        if not isinstance(new_path, Path):
            raise TypeError(f"Executable Path must be type Path, not {type(new_path)}")
        if not new_path.exists():
            raise InvalidSteamPathException(new_path, "Given root directory path does not exist.")
        if not new_path.is_dir():
            raise InvalidSteamPathException(new_path, "Given root directory path is not a directory.")

    def _requires_root(func):
        '''
        This decorator function marks a function as requiring a root path.
         
        :raise NoSteamRootException: If no root path exists, trying to call the function will raise a NoSteamRootException.
        '''
        def wrapper(self, *args, **kwargs):
            if not self.root:
                raise NoSteamRootException(func)
            func(self, *args, **kwargs)
        return wrapper

    @_requires_root
    def get_all_library_paths(self) -> dict[Path, list[int]]:
        '''
        Get a list of all Steam library paths from libraryfolders.vdf

        :return: A dictionary with Steam Library paths as a key, and a list of appids installed in that path as values.
        :rtype: dict[Path, list[int]]
        :raise SteamInvalidPathException: Raises SteamInvalidPathException if the library file path cannot be found.
        '''
        library_file_path = self.root / "steamapps" / "libraryfolders.vdf"
        if not library_file_path.exists():
            raise InvalidSteamPathException(library_file_path, "Path does not exist")
        with ValveTableFile(library_file_path, "r") as vtf:
            _, libraryfolders = vtf.read()
        libraries = {}
        for libraryfolder in libraryfolders.values():
            library_path = Path(libraryfolder['path'])
            library_apps = [int(key) for key in libraryfolder['apps'].keys()]
            libraries[library_path] = library_apps
        return libraries
    
    @_requires_root
    def get_library_containing_app(self, app_id: int) -> Path:
        '''
        Get the path of the library containing the specified app.

        :param app_id: The app's Steam app id.
        :type app_id: int
        :return: The path of the library containing the game, or None if it was not found.
        :rtype: Path
        '''
        libraries = self.get_all_library_paths()
        for library_path, library_apps in libraries.items():
            if app_id in library_apps:
                return library_path
        return None

    @_requires_root
    def get_app_manifest_filepath(self, app_id: int) -> Path:
        '''
        Get the filepath pointing to the app manifest file for a given Steam app by it's App ID

        :param app_id: Steam App ID
        :type app_id: int
        :return: Filepath for the manifest file for the specified app. Returns None if it doesn't exist.
        :rtype: SteamHandler.AppManifestFile
        '''
        library_path = self.get_library_containing_app(app_id)
        if library_path is None:
            return None
        manifest_path = library_path / "steamapps" / f"appmanifest_{app_id}.acf"
        if manifest_path.exists():
            return manifest_path
        return None
    
    @_requires_root
    def get_app_install_path(self, app_id: int) -> Path:
        '''
        Get the path of the directory the specified Steam app is installed in.

        :param app_id: Steam App ID
        :type app_id: int
        :return: The path containing the installed app, or None if it doesn't exist.
        :rtype: Path
        '''
        manifest_path = self.get_app_manifest_filepath(app_id)
        if manifest_path is None:
            return None
        with ValveTableFile(manifest_path) as vtf:
            _, manifest = vtf.read()
        installdir = manifest['installdir']
        install_path = manifest_path.parent / "common" / installdir
        if install_path.exists():
            return install_path
        return None

    @staticmethod
    def get_default_steam_path(self) -> Path:
        '''
        Get the default Steam path, platform-specific. Not guaranteed to exist.

        :return: The directory containing the Steam install.
        :rtype: Path
        '''
        if platform.system() == "Windows":
            # Windows
            candidates = [
                Path.home() / "Appdata" / "Local" / "Steam",
                Path("C:/Program Files (x86)/Steam"),
                Path("C:/Program Files/Steam")
            ]
        elif platform.system() == "Darwin":
            # macOS
            candidates = [
                Path.home() / 'Library' / 'Application Support' / 'Steam',
            ]
        else:
            candidates = [
                Path.home() / ".steam" / "steam",
                Path.home() / '.steam' / 'root',
                Path.home() / '.local' / 'share' / 'Steam',
            ]
        for path in candidates:
            if path.exists():
                return path.resolve()
        return None
    
    
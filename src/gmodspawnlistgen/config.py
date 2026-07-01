import os
import sys
import configparser
import platform
from pathlib import Path
from gmodspawnlistgen import APP_NAME
from os import access, R_OK, W_OK, X_OK

class SpawnlistGeneratorConfig:

    def __init__(self, config_path: Path):
        self.__config_path = config_path.resolve()
        self.__steam_path = None
        self.__gmod_path = None    

    @property
    def steam_path(self):
        return self.__steam_path

    @steam_path.setter
    def steam_path(self, new_path: Path):
        if not isinstance(new_path, Path):
            raise TypeError(f"{new_path=} should be type Path, not type {type(new_path)}.")
        if not new_path.exists():
            raise InvalidSteamPathException(new_path, "Does not exist")
        if not new_path.is_dir():
            raise InvalidSteamPathException(new_path, "Not a directory")
        self.__steam_path = new_path
    
    @property
    def gmod_path(self):
        return self.__gmod_path

    @gmod_path.setter
    def gmod_path(self, new_path: Path):
        if not isinstance(new_path, Path):
            raise TypeError(f"{new_path=} should be type Path, not type {type(new_path)}.")
        if not new_path.exists():
            raise InvalidGarrysModPathException(new_path, "Does not exist")
        if not new_path.is_dir():
            raise InvalidGarrysModPathException(new_path, "Not a directory")
        self.__gmod_path = new_path
    
    def config_file_readable(self):
        if not self.__config_path.exists():
            return False
        if not access(self.__config_path, R_OK):
            return False
        return True

    def read(self):
        if not self.config_file_readable():
            raise RuntimeError("Cannot read from non-existent or non-readable config file.")
        config = config.ConfigParser()
        with open(self.__config_path, "r", encoding="utf-8") as config_file:
            config.read_file(config_file)
        self.steam_path = Path(config['Steam']['InstallPath'])
        self.gmod_path = Path(config["Garry's Mod"]['InstallPath'])
    
    def write(self):
        config = configparser.ConfigParser()
        config['Steam']['InstallPath'] = self.steam_path
        config["Garry's Mod"]['InstallPath'] = self.gmod_path
        with open(self.__config_path, "w", encoding="utf-8") as config_file:
            config.write(config_file)

    @staticmethod
    def get_default_dir() -> Path:
        '''
        Get the default path to the directory where configuration files will be stored.

        :return: Directory for the config files.
        :rtype: Path
        '''
        if platform.system() == "Windows":
            # Windows
            return Path.home() / "AppData" / "Local" / APP_NAME
        elif platform.system() == "Darwin":
            # macOS
            return Path.home() / "Library" / "Application Support" / APP_NAME
        else:
            # Linux and others
            config_home = os.getenv('XDG_CONFIG_HOME')
            if config_home:
                return Path(config_home) / APP_NAME
            else:
                return Path.home() / ".config" / APP_NAME

    @staticmethod
    def get_default_filepath(config_name: str = "config") -> Path:
        '''
        Return the path to the config file. Not guaranteed to point to an existing file.

        :return: The path to the config file. 
        :rtype: Path
        '''
        return get_config_dir() / f"{config_name}.ini"
import argparse
from gmodspawnlistgen.cli.parsertypes import *
from gmodspawnlistgen import APP_NAME

class SpawnlistGeneratorArgParser:

     def __init__(self):
          self.__parser = argparse.ArgumentParser()
          self.__parser.add_argument(
                                   "--steam-path", 
                                   dest="steam_path", 
                                   metavar="STEAM_INSTALL_PATH", 
                                   help="Specify this flag to explicitly tell the app where "\
                                        "Steam's executable file can be found. "\
                                        "If not provided, the app will use config settings "\
                                        "or attempt to find Steam on it's own. "\
                                        "Will overwrite config setting if provided.",
                                   type=existing_file_path
                                   )
          self.__parser.add_argument(
                                   "--gmod-path", 
                                   dest="gmod_path", 
                                   metavar="GARRYS_MOD_INSTALL_PATH", 
                                   help="Specify this flag to explicitly tell the app where "\
                                        "Garry's Mod's executable file can be found. "\
                                        "If not provided, the app will use config settings "\
                                        "or attempt to find Steam on it's own. "\
                                        "Will overwrite config setting if provided.",
                                   type=existing_file_path
                                   )
          self.__parser.add_argument(
                                   "--config-file",
                                   dest="config_path",
                                   metavar="CONFIG_FILE_PATH",
                                   help="Specify this flag to explicitly tell the app where "\
                                        "to read and write it's own config file. "\
                                        f"If not provided, defaults to the {APP_NAME} directory "\
                                        "in your platform's default configuration file directory.",
                                   type=readable_writeable_path
          )

     def parse_args(self, args = None, namespace = None):
          return self.__parser.parse_args(args, namespace)
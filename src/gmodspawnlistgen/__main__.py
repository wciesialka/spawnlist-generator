from gmodspawnlistgen.valvetable import ValveTableFile
from gmodspawnlistgen.config import SpawnlistGeneratorConfig
from gmodspawnlistgen.steam import SteamFileHandler
from gmodspawnlistgen.cli.argparser import SpawnlistGeneratorArgParser

def main():
    parser = SpawnlistGeneratorArgParser()
    args = parser.parse_args()
    
    config_path = args.config_path
    # If no config path provided, fallback on default.
    if config_path is None:
        config_path = SpawnlistGeneratorConfig.get_default_filepath()
    config = SpawnlistGeneratorConfig(config_path)
    if config.config_file_readable():
        config.read()
    
    steam_path = args.steam_path
    if steam_path:
        # If steam path provided, overwrite config.
        config.steam_path = steam_path
        config.write()
        # Else, check if config has a path already.
        # If it doesn't, go searching.
    elif config.steam_path is None:
        steam_path = SteamFileHandler.get_default_steam_path()
    else:
        steam_path = config.steam_path
    
    gmod_path = args.gmod_path
    if gmod_path:
        # If gmod path provided, overwrite config.
        config.gmod_path = gmod_path
        config.write()
    elif config.gmod_path is None:
        # If config doesn't have a path, and no path provided,
        # then we need to go hunting.
        # To do that, we need a SteamFileHandler.
        # For that, we need a steam_path. If it doesn't exist,
        # then we need to raise an error.
        if steam_path is None:
            raise RuntimeError("Could not find Steam or Garry's Mod. Please provide at least one using the --steam-path or --gmod-path flags.")
        sfh = SteamFileHandler(steam_path)
        gmod_path = sfh.get_app_install_path(4000) # Garry's Mod is appid 4000.
        if gmod_path:
            # If we found it, then we need to update it in the config.
            config.gmod_path = gmod_path
            config.write()
        else:
            raise RuntimeError("Could not find Garry's Mod. Please provide the install path using the --gmod-path flag.")
    
    target_vpk = args.target_vpk


if __name__ == "__main__":
    main()
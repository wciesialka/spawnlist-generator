# Garry's Mod Spawnlist Generator

Create GMod Spawnlists for any mountable Source game.

## Getting Started

### Prerequisites

- Python 3.13+
- [Python VPK Libary](https://github.com/ValvePython/vpk)

### Installing

- Clone the repository
- Enter the directory with `cd spawnlist-generator`
- Create a virtual environment using `python3 -m venv env/`
- Activate the environment using `source env/bin/activate`
- Install using `pip install .`

### Running

```
usage: gmod-spawnlist-gen [-h] [--steam-path STEAM_INSTALL_PATH]
                          [--gmod-path GARRYS_MOD_INSTALL_PATH]
                          [--config-file CONFIG_FILE_PATH]
                          SPAWNLIST_NAME PATH_TO_VPK

Create Garry's Mod spawnlists directly from mountable games' .vpk files.

positional arguments:
  SPAWNLIST_NAME        The base name for your new spawnlist.
  PATH_TO_VPK           The file path for the _dir.vpk file you wish to
                        generate a spawnlist with. This is typically found in
                        the 'appname' folder in the game's install path. For
                        example, Garry's Mod's is located in
                        "../garrysmod/garrysmod_dir.vpk". Some games may have
                        more than one _dir.vpk file.

options:
  -h, --help            show this help message and exit
  --steam-path STEAM_INSTALL_PATH
                        Specify this flag to explicitly tell the app where
                        Steam's root directory can be found. If not provided,
                        the app will use config settings or attempt to find
                        Steam on it's own. Will overwrite config setting if
                        provided.
  --gmod-path GARRYS_MOD_INSTALL_PATH
                        Specify this flag to explicitly tell the app where the
                        Garry's Mod's root directory can be found. If not
                        provided, the app will use config settings or attempt
                        to use Steam to find it on it's own. Will overwrite
                        config setting if provided.
  --config-file CONFIG_FILE_PATH
                        Specify this flag to explicitly tell the app where to
                        read and write it's own config file. If not provided,
                        defaults to the gmod-spawnlist-generator directory in
                        your platform's default configuration file directory.

The default location for the configuration file is dependent on your operating
system.
```

## Authors

- Willow Ciesialka

## Thanks to

- VPK Library Team

## License

This project is licensed under GNU General Public License v3.0 - see [LICENSE](LICENSE) for details.

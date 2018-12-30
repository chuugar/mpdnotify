import argparse
import configparser
import pathlib
from os import environ
from sys import exit


"""Get user preferences
Priority : command-line argument > config > environment > hardcoded
"""

__preferences__ = {
        "config": 'mpdnotifyrc',
        "host": 'localhost',
        "port": '6600',
        "appname": 'mpd',
        "musicdir": '',
        }


class GlobalParser(object):
    def __init__(self):
        for _ in __preferences__:
            setattr(self, _, '')

        # self.empty_pref will help us to save the unset preferences
        self.empty_pref = []
        # first check if the preferences are set from within the CLI
        args = self._parsing_arguments()
        for _ in __preferences__:
            if getattr(args, _):
                setattr(self, _, getattr(args, _))
            else:
                self.empty_pref.append(_)

        # then looks at the config file, if any, to fill the missing arguments
        # as they are read from self.empty_pref
        config = self._parsing_config()
        if config:
            for _ in self.empty_pref[:]:
                try:
                    setattr(self, _, config.get("mpdnotify", _))
                except configparser.NoOptionError:
                    self.empty_pref.append(_)
                else:
                    self.empty_pref.remove(_)

        # last try with default options (corresponding to __preferences__'
        # items)
        for _ in self.empty_pref[:]:
            if __preferences__.get(_) != '':
                setattr(self, _, __preferences__.get(_))
                self.empty_pref.remove(_)
            else:
                self.empty_pref.append(_)

        # special case since always defined from within the CLI
        self.oneshot = args.oneshot

        # try to guess mpd's music folder
        if not self.musicdir:
            try:
                environ["XDG_MUSIC_DIR"]
            except KeyError:
                pass
            else:
                self.musicdir = environ.get("XDG_MUSIC_DIR")
                self.empty_pref.remove("musicdir")

        # if some preference cannot be filled : exit
        if self.empty_pref:
            for i in self.empty_pref:
                print("{} must be specified".format(i))
            self._exit("All requierement are not satisfied", 2)

    def _exit(self, msg, error):
        print(msg)
        exit(error)

    def _parsing_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
                "-a",
                "--appname",
                metavar="mpd"
                )
        parser.add_argument(
                "-c",
                "--config",
                metavar="mpdnotifyrc"
                )
        parser.add_argument(
                "--host",
                metavar="localhost",
                type=str
                )
        parser.add_argument(
                "-m",
                "--musicdir",
                metavar="/path/to/your/mpd/dir"
                )
        parser.add_argument(
                "-p",
                "--port",
                metavar="6600",
                type=int
                )
        parser.add_argument(
                "-o",
                "--oneshot",
                action="store_true"
                )
        return parser.parse_args()

    def _parsing_config(self):
        """
        :type returns: dict
        """
        def _is_file(_file):
            if isinstance(_file, pathlib.PosixPath):
                return _file.is_file()
            if pathlib.Path(_file).is_file():
                return True

        cwd_config = pathlib.Path.cwd().joinpath("mpdnotifyrc")
        # first looks at args
        if not _is_file(cwd_config) and self.config != '':
            if not isinstance(self.config, pathlib.Path):
                self.config = pathlib.Path(self.config)
        # else try to find the config file in the current dir
        elif _is_file(cwd_config) and self.config == '':
            self.config = cwd_config
        # finally try to looks at the config directory
        else:
            try:
                config_home = pathlib.Path(environ.get("XDG_CONFIG_HOME"))\
                        .expanduser()
            except KeyError:
                config_home = pathlib.Path("~/.config").expanduser()
            finally:
                config_list = (
                        pathlib.Path(config_home).joinpath("mpdnotifyrc"),
                        pathlib.Path(config_home).joinpath("mpdnotify")
                                                 .joinpath("mpdnotifyrc")
                )
                for _ in config_list:
                    if _.exists():
                        self.config = _

        if self.config:
            config = configparser.ConfigParser()
            try:
                config.read(self.config.__str__())
            except configparser.ParsingError:
                self._exit("Error while parsing the configuration file", 3)
            else:
                if "mpdnotify" in config.sections():
                    return config
                else:
                    self._exit("No [mpdnotify] within the config file", 3)

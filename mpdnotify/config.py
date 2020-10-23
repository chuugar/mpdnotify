from os import environ
from sys import exit

import argparse
import configparser
import pathlib


"""Get user preferences
Priority : command-line argument > config > environment > hardcoded
"""

__preferences__ = {
  "appname": "mpd",
  "config": "mpdnotifyrc",
  "titleformat": "{title}",
  "bodyformat": "{album} ({artist})",
  "host": "localhost",
  "musicdir": "",
  "port": "6600",
  "timeout": "3500"
}


class GlobalParser(object):
  def __init__(self):
    for pref in __preferences__:
      setattr(self, pref, "")

    # self.empty_pref will help us to save the unset preferences
    self.empty_pref = []
    # first check if the preferences are set from within the CLI
    args = self._parsing_arguments()
    for pref in __preferences__:
      if getattr(args, pref):
        setattr(self, pref, getattr(args, pref))
      else:
        self.empty_pref.append(pref)

    # then looks at the config file, if any, to fill the missing arguments
    # as they are read from self.empty_pref
    config = self._parsing_config()
    if config:
      for pref in self.empty_pref[:]:
        try:
          setattr(self, pref, config.get("mpdnotify", pref))
        except configparser.NoOptionError:
          self.empty_pref.append(pref)
        else:
          self.empty_pref.remove(pref)

    # last try with default options (corresponding to __preferences__ items)
    for pref in self.empty_pref[:]:
      if __preferences__.get(pref) != "":
        setattr(self, pref, __preferences__.get(pref))
        self.empty_pref.remove(pref)
      else:
        self.empty_pref.append(pref)

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
      self._exit("All requirement are not satisfied", 2)

  def _exit(self, msg, error):
    print(msg)
    exit(error)

  def _parsing_arguments(self):
    parser = argparse.ArgumentParser()

    parser.add_argument("-a", "--appname",     metavar=__preferences__["appname"])
    parser.add_argument("-c", "--config",      metavar=__preferences__["config"])

    parser.add_argument("-f", "--titleformat", metavar=__preferences__["titleformat"])
    parser.add_argument("-b", "--bodyformat",  metavar=__preferences__["bodyformat"])

    parser.add_argument("--host", type=str,    metavar=__preferences__["host"])
    parser.add_argument("-m", "--musicdir",    metavar=__preferences__["musicdir"])
    parser.add_argument("-p", "--port",        metavar=__preferences__["port"], type=int)
    parser.add_argument("-o", "--oneshot", action="store_true")
    parser.add_argument("-t", "--timeout",     metavar=__preferences__["timeout"], type=int)

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
    if not _is_file(cwd_config) and self.config != "":
      if not isinstance(self.config, pathlib.Path):
        self.config = pathlib.Path(self.config)
    # else try to find the config file in the current dir
    elif _is_file(cwd_config) and self.config == "":
      self.config = cwd_config
      # finally try to looks at the config directory
    else:
      try:
        config_home = pathlib.Path(environ.get("XDG_CONFIG_HOME")).expanduser()
      # If XDG_CONFIG_HOME doesn't exist, pathlib.Path will throw a TypeError
      except (KeyError, TypeError):
        config_home = pathlib.Path("~/.config").expanduser()
      finally:
        config_list = (
          pathlib.Path(config_home).joinpath("mpdnotifyrc"),
          pathlib.Path(config_home)
            .joinpath("mpdnotify")
            .joinpath("mpdnotifyrc"),
        )

        for config in config_list:
          if config.exists():
            self.config = config

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

import pathlib
from PIL import Image

from tempfile import NamedTemporaryFile
from subprocess import run
from mpd import MPDClient


class MPD():
    def __init__(self, host, port, music_dir, appname="mpd"):
        self.host = host
        self.port = port
        self.appname = appname
        self.music_dir = music_dir

        self.mpd = MPDClient()
        self.mpd.connect(self.host, self.port)

        self.title = self.get_title()
        self.artist = self.get_artist()
        self.album = self.get_album()
        self.file = self.get_file()

        self.body, self.notify_run = "", "",
        self.garbagecover = []

        #  generates a list of cover name as they are usually found
        self.cover_list = []
        for name in ("album", "front", "cover"):
            for ext in (".jpg", ".png"):
                self.cover_list.append(name + ext)
                self.cover_list.append(name + ext.upper())
                self.cover_list.append(name.upper() + ext)
                self.cover_list.append(name.upper() + ext.upper())
                self.cover_list.append(name.capitalize() + ext)
                self.cover_list.append(name.capitalize() + ext.upper())

    def clean_covers(self, limit=20, force=False):
        """ Clean useless covers' files
        since resized covers' images are saved within a named temporary file
        it's necessary to delete it when they are not in use anymore
        NB : if the cover image is delete too fast the notification pop-up
        might lose its icon
        """
        if force:
            for _ in self.garbagecover:
                _.unlink()
        else:
            mid = limit // 2
            if len(self.garbagecover) > limit:
                for _ in self.garbagecover[0:mid]:
                    _.unlink()
                    self.garbagecover.remove(_)

    def get_artist(self):
        return self.mpd.currentsong().get('artist')

    def get_album(self):
        return self.mpd.currentsong().get('album')

    def get_cover(self):
        try:
            # without .expanduser(), pathlib doesn't work right with '~'
            # cf. https://bugs.python.org/issue19776
            music_dir = pathlib.Path(self.music_dir).expanduser()
            parent = music_dir.joinpath(self.file).parent
        except TypeError:
            return ''
        else:
            for _ in parent.iterdir():
                if _.name in self.cover_list:
                    return parent.joinpath(_.name)

    def get_file(self):
        return self.mpd.currentsong().get('file')

    def get_title(self):
        return self.mpd.currentsong().get('title')

    def sendnotify(self, cover=False):
        self.body = "{} ({})".format(self.artist, self.album)
        if self.cover:
                self.notify_run = \
                    ["notify-send", "-a", self.appname, "-i",
                     self.cover.__str__(), self.title, self.body]
        else:
            self.notify_run = \
                ["notify-send", "-a", self.appname, self.title, self.body]
        try:
            run(self.notify_run)
        except TypeError:
            pass

    def resize_cover(self):
        im = Image.open(self.cover)
        im = im.resize((96, 96))

        with NamedTemporaryFile(
                suffix=".png",
                prefix="mpdnotify-",
                delete=False
                ) as resize_cover:
            p = pathlib.Path(resize_cover.name)
            im.save(p, 'png')

        self.garbagecover.append(p)
        self.cover = p

    def watch(self):
        old_title = self.title
        while True:
            self.clean_covers()
            self.mpd.idle()

            self.title = self.get_title()
            self.album = self.get_album()
            self.artist = self.get_artist()
            self.file = self.get_file()

            self.cover = self.get_cover()
            if self.cover:
                self.resize_cover()

            # prevent multiple undesired notification
            if old_title != self.title:
                break

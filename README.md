# mpdnotify

Notifies when mpd's song changes.

![mpdnotify](https://raw.githubusercontent.com/chuugar/mpdnotify/master/screenshot.png)

## Installation

It has been test on Debian 9.5, it shall work on any other Linux distribution with Python >= 3.2.
Please let me now if it works on OSX.

### PyPa

For now, *mpdnotify* is not a PyPa's package.

### Manual

#### Requirements

* `notify-send`
* Python >= 3.2
* [Pillow](https://github.com/python-pillow/Pillow)
* [python-mpd2](https://github.com/Mic92/python-mpd2)

#### Installation

```
git clone https://github.com/chuugar/mpdnotify.git
cd mpdnotify
pip3 install -r requirements.txt -e .
```

## Usage

A few arguments can be passed to mpdnotify :
* **-a / --appname** : specifies the app name for notify-send.
* **-c / --config** : path to the configuration file.
* **--host** : mpd's address.
* **-m / --musicdir** : path to mpd's music library folder.
* **-p / --port** : mpd's server port.
* **-o / --oneshot** : send a notification and exit immediately.

All this arguments can be save in a configuration file, please see `mpdnotifyrc.sample` for further informations.

**Once running, `mpdnotify` will wait for the next song to send a notification** (unless **-o / --oneshot** has been passed).
Cover is used as notification icon if a file (cover/front/album).(png/jpg) is find in the same folder as the music file.

## TODO

* Add a test suite.
* Allow user to change the notification format.
* If cover cannot be found as an image, look at the tags.

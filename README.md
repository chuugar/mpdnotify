# mpdnotify

Notifies when mpd's song changes.

![mpdnotify](https://raw.githubusercontent.com/chuugar/mpdnotify/master/screenshot.png)

## Installation

It has been tested on Debian 9.5, it shall work on any other Linux distribution with Python >= 3.2.
Please let me now if it works on OSX.

### PyPa

You can install `mpdnotify` in a single command:
`pip install mpdnotify`

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

A few arguments can be passed to mpdnotify:

* **-a / --appname** : specifies the app name for notify-send.
* **-c / --config** : path to the configuration file.
* **-h / --host** : mpd's address.
* **-m / --musicdir** : path to mpd's music library folder.
* **-p / --port** : mpd's server port.
* **-o / --oneshot** : send a notification and exit immediately.
* **-t / --timeout** : amount of milliseconds for which notification will be shown

All of these arguments can be save in a configuration file, please see [`mpdnotifyrc.sample`](https://github.com/chuugar/mpdnotify/blob/master/mpdnotifyrc.sample) for further informations.

**Once running, `mpdnotify` will wait for the next song to send a notification** (unless **-o / --oneshot** has been passed).
Cover is used as notification icon if a file (cover/front/album).(png/jpg) is find in the same folder as the music file.

## TODO

* Add a test suite.
* Allow the user to change the notification format.
* If cover cannot be found as an image, look at the tags.

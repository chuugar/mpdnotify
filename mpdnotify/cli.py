from mpdnotify import config, notify


def main():
    pref = config.GlobalParser()
    mpd = notify.MPD(pref.host, pref.port, pref.musicdir)

    if pref.oneshot:
        mpd.sendnotify()
    else:
        try:
            while True:
                mpd.clean_covers()
                mpd.watch()
                mpd.sendnotify()
        except KeyboardInterrupt:
            print("\nBye !")
        finally:
            mpd.clean_covers(force=True)


if __name__ == "__main__":
    main()

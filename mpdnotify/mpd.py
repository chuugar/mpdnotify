import socket


class MPDClient(object):
    def __init__(self, host="localhost", port=6600):
        self.host = host
        self.port = port
        self.timeout = None
        self._sock = None

        self._fetched = ("currentsong", "status")
        self._notfetched = ("idle")

    def _write(self, cmd, arg=""):
        self._wfile.write("{}\t{}\n".format(cmd, arg))
        self._wfile.flush()

    def _fetch(self, cmd, arg=""):
        """
        return : dictionary
        """

        d = {}
        if not cmd in self._fetched:
            raise AttributeError("'{}' is not a valid value".format(cmd))
        self._write(cmd, arg)
        for l in self._rfile:
            if l.startswith("OK"):
                break
            else:
                ds = l.rstrip("\n").split(": ")
                ds[0] = ds[0].lower()
                ds[0] = "".join([i for i in ds[0] if i.isalpha()])
                ds[0] = "".join([i for i in ds[0] if i.isascii()])
                d.update({ds[0]: ds[1]})
        return d

    def _no_fetch(self, cmd, arg=""):
        if not cmd in self._notfetched:
            raise AttributeError("'{}' is not a valid value".format(cmd))
        self._write(cmd, arg)
        self._rfile.readline()

    def _mpd_command(self, cmd, arg=""):
        if cmd in self._fetched:
            return self._fetch(cmd, arg)
        elif cmd in self._notfetched:
            return self._no_fetch(cmd, arg)
        else:
            raise AttributeError("{} is not a valid command".format(cmd))

    def _connect_tcp(self, host, port):
        if not host:
            host = self.host
        if not port:
            port = self.port

        try:
            flags = socket.AI_ADDRCONFIG
        except AttributeError:
            flags = 0

        for res in socket.getaddrinfo(
            self.host,
            self.port,
            socket.AF_UNSPEC,
            socket.SOCK_STREAM,
            socket.IPPROTO_TCP,
            flags,
        ):
            af, socktype, proto, canonname, sa = res

            sock = None
            try:
                sock = socket.socket(af, socktype, proto)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                sock.settimeout(self.timeout)
                sock.connect(sa)
                return sock
            except socket.error:
                sock.close()

    def _connect_unix(self, path):
        if not hasattr(socket, "AF_UNIX"):
            raise ConnectionError(
                "Unix domain sockets not supported on this platform"
            )
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(path)
        return sock

    def connect(self, host=None, port=None):
        if not host:
            host = self.host
        if not port:
            port = self.port
        if self._sock is not None:
            raise ConnectionError("Already connected")
        if host.startswith("/"):
            self._sock = self._connect_unix(host)
        else:
            self._sock = self._connect_tcp(host, port)

        self._rfile = self._sock.makefile("r", encoding="utf-8", newline="\n")
        self._wfile = self._sock.makefile("w", encoding="utf-8", newline="\n")
        self._rfile.readline()

    def status_to_attr(self, d):
        """create attribute from dictionnarie"""
        for k in d:
            setattr(self, k, d[k])

import socket


class MPDClient(object):
  def __init__(self, host="localhost", port=6600):
    self.host = host
    self.port = port
    self.timeout = None
    self._sock = None

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
      raise ConnectionError("Unix domain sockets not supported on this platform")

    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(path)
    return sock

  def _hello(self):
    self._rfile.readline()

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
    self._hello()

  def idle(self):
    self._wfile.write("idle\tplayer\n")
    self._wfile.flush()
    self._rfile.readline()

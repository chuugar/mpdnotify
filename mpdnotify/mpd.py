import socket

class MPDClient(object):
    def __init__(self, host="localhost", port=6600, use_unicode=False):
        self.host = host
        self.port = port
        self.timeout = 10
        self.use_unicode = use_unicode

        self._sock = self._connect_tcp()
        self._rfile = self._sock.makefile(encoding="utf-8", newline="\n")


    def _connect_tcp(self):
        try:
            flags = socket.AI_ADDRCONFIG
        except AttributeError:
            flags = 0

        for res in socket.getaddrinfo(self.host, self.port, socket.AF_UNSPEC,
                                      socket.SOCK_STREAM, socket.IPPROTO_TCP,
                                      flags):
            af, socktype, proto, canonname, sa = res

            sock = None
            try:
                sock = socket.socket(af, socktype, proto)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                sock.settimeout(self.timeout)
                sock.connect(sa)
                return sock
            except socket.error as e:
                err = e
                if sock is not None:
                    sock.close()

    def _print_socket(self):
        return self._sock.recv(1024)

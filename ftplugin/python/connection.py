import socket


class ServerConnection(object):

    def __init__(self, *a, **k):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(1.)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._connection = None

    def connect(self):
        self._socket.bind((socket.gethostbyname(socket.gethostname()), 50007))
        self._socket.listen(1)
        self._connection, _address = self._socket.accept()
        self._connection.setblocking(1)

    def disconnect(self):
        self._socket.close()
        self._connection = None

    def _ensure_has_connection(self):
        if self._connection is None:
            self.connect()
        return self._connection is not None

    def send(self, message):
        if self._ensure_has_connection():
            self._connection.sendall(message)

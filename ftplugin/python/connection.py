import socket


class ServerConnection(object):

    def __init__(self, *a, **k):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(1.)

    def connect(self):
        self._socket.connect(
            (socket.gethostbyname(socket.gethostname()), 50007)
        )

    def disconnect(self):
        self._socket.close()

    def send(self, message):
        self._socket.sendall(message)

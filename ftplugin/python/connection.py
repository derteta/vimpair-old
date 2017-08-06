import socket


class ServerConnection(object):

    def __init__(self, *a, **k):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(1.)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._connection = None
        try:
            self._socket.bind(
                (socket.gethostbyname(socket.gethostname()), 50007)
            )
        except:
            pass

    def connect(self):
        try:
            self._socket.listen(1)
            self._connection, _address = self._socket.accept()
            self._connection.setblocking(1)
        except socket.timeout:
            pass

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


class ClientConnection(object):

    def __init__(
        self,
        message_queue,
        socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM),
        *a, **k
    ):
        self._socket = socket
        self._socket.settimeout(3.)
        self._message_queue = message_queue

    def connect(self):
        import time; time.sleep(1)
        self._socket.connect(
            (socket.gethostbyname(socket.gethostname()), 50007)
        )

    def disconnect(self):
        self._socket.close()

    def retrieve(self):
        try:
            new_message = str(self._socket.recv(1024))
            self._message_queue.put(new_message)
        except socket.timeout:
            pass

import socket
import vim
import time
import threading


class VimpairServer(object):

    def __init__(self, *a, **k):
        self._socket = socket.socket()
        self._socket.settimeout(1.)
        self._thread = threading.Thread(target=self._send_buffer_contents)

    def start(self):
        self._thread.start()

    def stop(self):
        self._thread.join()

    def _send_buffer_contents(self):
        time.sleep(.5)
        try:
            self._socket.connect((socket.gethostbyname(socket.gethostname()), 50007))
            buffer_contents = reduce(lambda s1, s2: s1 + '\n' + s2, vim.current.buffer[:])
            self._socket.sendall(buffer_contents)
        finally:
            self._socket.close()

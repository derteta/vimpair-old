import socket
import vim
import time
import threading
import Queue


class VimpairServer(object):

    def __init__(self, *a, **k):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(1.)
        self._thread = threading.Thread(target=self._serve)
        self._queue = Queue.Queue()

    def start(self):
        self._is_serving = True
        self._thread.start()
        self.update()

    def stop(self):
        self._is_serving = False
        self._thread.join()

    def update(self):
        buffer_contents = reduce(
            lambda s1, s2: s1 + '\n' + s2,
            vim.current.buffer[:]
        )
        self._queue.put_nowait(buffer_contents)

    def _run_serve_loop(self):
        while (self._is_serving):
            try:
                self._socket.sendall(self._queue.get(block=True, timeout=1))
            except Queue.Empty:
                pass

    def _serve(self):
        time.sleep(.5)
        try:
            self._socket.connect(
                (socket.gethostbyname(socket.gethostname()), 50007)
            )
            self._run_serve_loop()
        finally:
            self._socket.close()

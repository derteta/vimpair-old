import vim
import time
import threading
import Queue

from connection import ServerConnection
from vim_interface import VimInterface


class VimpairServer(object):

    def __init__(self, *a, **k):
        self._editor_interface = VimInterface(vim=vim)
        self._connection = ServerConnection()
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
        self._queue.put_nowait(self._editor_interface.current_contents)

    def _run_serve_loop(self):
        while (self._is_serving):
            try:
                self._connection.send(self._queue.get(block=True, timeout=1))
            except Queue.Empty:
                pass

    def _serve(self):
        time.sleep(.5)
        try:
            self._connection.connect()
            self._run_serve_loop()
        finally:
            self._connection.disconnect()

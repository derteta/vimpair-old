import vim
import Queue

from connection import ServerConnection
from runloop import Runloop
from vim_interface import VimInterface

class VimpairServer(object):

    def __init__(self, *a, **k):
        self._editor_interface = VimInterface(vim=vim)
        self._connection = ServerConnection()
        self._runloop = Runloop(
            setup=self._connection.connect,
            process=self._serve,
            cleanup=self._connection.disconnect
        )
        self._queue = Queue.Queue()

    def start(self):
        self._runloop.start()
        self.update()

    def stop(self):
        self._runloop.stop()

    def update(self):
        self._queue.put_nowait(self._editor_interface.current_contents)

    def _serve(self):
        try:
            self._connection.send(self._queue.get(block=True, timeout=1))
        except Queue.Empty:
            pass

import vim

from connection import ServerConnection
from editor_controller import EditorController
from runloop import Runloop
from vim_interface import VimInterface

class VimpairServer(object):

    def __init__(self, *a, **k):
        connection = ServerConnection()
        self._editor_controller = EditorController(
            editor_interface=VimInterface(vim=vim),
            process_callback=connection.send
        )
        self._runloop = Runloop(
            setup=connection.connect,
            process=self._editor_controller.process_next,
            cleanup=connection.disconnect
        )

    def start(self):
        self._runloop.start()
        self.update()

    def stop(self):
        self._runloop.stop()

    def update(self):
        self._editor_controller.content_changed()

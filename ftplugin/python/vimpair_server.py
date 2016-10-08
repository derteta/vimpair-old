import vim

from connection import ServerConnection
from editor_controller import EditorController
from runloop import Runloop
from vim_interface import VimInterface


class VimpairServer(object):

    def __init__(self, editor_controller=None, runloop=None, *a, **k):
        self._editor_controller = editor_controller
        self._runloop = runloop

    def start(self):
        self._runloop.start()
        self.update()

    def stop(self):
        self._runloop.stop()

    def update(self):
        self._editor_controller.content_changed()


def create_server():
    connection = ServerConnection()
    editor_controller = EditorController(
        editor_interface=VimInterface(vim=vim),
        process_callback=connection.send
    )
    runloop = Runloop(
        setup=connection.connect,
        process=editor_controller.process_next,
        cleanup=connection.disconnect
    )
    return VimpairServer(editor_controller=editor_controller, runloop=runloop)

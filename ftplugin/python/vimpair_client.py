import vim
from Queue import Queue, Empty

from connection import ClientConnection
from editor_controller import EditorController
from runloop import Runloop
from vim_interface import VimInterface


class VimpairClient(object):

    def __init__(
        self,
        editor_controller=None,
        message_queue=None,
        runloop=None,
        *a, **k
    ):
        self._message_queue = message_queue
        self._editor_controller = editor_controller

        self.start = runloop.start
        self.stop = runloop.stop

    def on_timer(self):
        try:
            while True:
                new_message = self._message_queue.get(block=False)
                self._editor_controller.set_current_contents(new_message)
        except Empty:
            pass


def create_client():
    message_queue = Queue(maxsize=100)
    connection = ClientConnection(message_queue)
    editor_controller = EditorController(
        editor_interface=VimInterface(vim=vim),
        process_callback=lambda _: None,
    )
    runloop = Runloop(
        setup=connection.connect,
        process=connection.retrieve,
        cleanup=connection.disconnect,
    )
    return VimpairClient(
        editor_controller=editor_controller,
        message_queue=message_queue,
        runloop=runloop,
    )

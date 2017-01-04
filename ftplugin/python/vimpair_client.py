import vim
import socket

from editor_controller import EditorController
from runloop import Runloop
from vim_interface import VimInterface


class VimpairClient(object):

    def __init__(self, editor_controller=None):
        self._editor_controller = editor_controller
        self._runloop = Runloop(
            setup=self.connect,
            process=self.retrieve,
            cleanup=self.disconnect,
        )

        self.start = self._runloop.start
        self.stop = self._runloop.stop

    def connect(self):
        import time; time.sleep(1)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(3.)
        self.client_socket.connect(
            (socket.gethostbyname(socket.gethostname()), 50007)
        )

    def retrieve(self):
        try:
            new_message = str(self.client_socket.recv(1024))
            self._editor_controller.set_current_contents(new_message)
        except socket.timeout:
            pass

    def disconnect(self):
        self.client_socket.close()


def create_client():
    editor_controller = EditorController(
        editor_interface=VimInterface(vim=vim),
        process_callback=lambda _: None,
    )
    return VimpairClient(editor_controller=editor_controller)

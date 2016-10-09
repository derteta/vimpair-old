import threading


class Runloop(object):

    def __init__(self, setup=None, process=None, cleanup=None, *a, **k):
        self._setup = setup
        self._process = process
        self._cleanup = cleanup
        self._thread = threading.Thread(target=self._run)

    def start(self):
        self._is_serving = True
        self._thread.start()

    def stop(self):
        self._is_serving = False
        self._thread.join()

    def _run(self):
        try:
            self._setup()
            while (self._is_serving):
                self._process()
        finally:
            self._cleanup()

import Queue


class EditorController(object):

    def __init__(
        self,
        editor_interface=None,
        process_callback=None,
        processing_should_block=True,
        *a, **k
    ):
        self._editor_interface = editor_interface
        self._process_callback = process_callback
        self._queue = Queue.Queue()
        self._processing_should_block = processing_should_block

    def content_changed(self):
        self._queue.put_nowait(
            dict(
                content=self._editor_interface.current_contents,
                cursor=self._editor_interface.cursor_position,
            )
        )

    def process_next(self):
        try:
            self._process_callback(
                self._queue.get(block=self._processing_should_block, timeout=1)
            )
        except Queue.Empty:
            pass

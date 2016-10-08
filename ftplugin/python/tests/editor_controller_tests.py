import unittest
from ..editor_controller import EditorController


class EditorInterfaceStub(object):

    current_contents = "Test Content"


class EditorControllerTests(unittest.TestCase):

    def setUp(self):
        self.last_processed_message = None
        self.editor_interface = EditorInterfaceStub()
        self.controller = EditorController(
            editor_interface=self.editor_interface,
            process_callback=self.process,
            processing_should_block=False,
        )

    def process(self, message):
        self.last_processed_message = message


    def test_nothing_is_processed_when_processing_without_changes(self):
        self.controller.process_next()

        self.assertIsNone(self.last_processed_message)

    def test_changed_content_is_not_processed_immediately(self):
        self.controller.content_changed()

        self.assertIsNone(self.last_processed_message)

    def test_changed_content_is_processed_next(self):
        self.controller.content_changed()

        self.controller.process_next()

        self.assertEqual(self.last_processed_message, "Test Content")

    def test_processed_content_reflects_editor_content(self):
        self.editor_interface.current_contents += ", now with changes"
        self.controller.content_changed()

        self.controller.process_next()

        self.assertEqual(
            self.last_processed_message,
            "Test Content, now with changes",
        )

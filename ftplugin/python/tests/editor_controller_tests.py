import unittest
from ..editor_controller import EditorController


class EditorInterfaceStub(object):

    current_contents = "Test Content"
    cursor_position = (0,0)


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

    def assertHasItem(self, key, value):
        self.assertEqual(self.last_processed_message[key], value)

    def assertHasContent(self, expected):
        self.assertHasItem('content', expected)

    def assertHasCursorPosition(self, expected):
        self.assertHasItem('cursor', expected)


    def test_nothing_is_processed_when_processing_without_changes(self):
        self.controller.process_next()

        self.assertIsNone(self.last_processed_message)

    def test_changed_content_is_not_processed_immediately(self):
        self.controller.content_changed()

        self.assertIsNone(self.last_processed_message)

    def test_changed_content_is_processed_next(self):
        self.controller.content_changed()

        self.controller.process_next()

        self.assertHasContent("Test Content")

    def test_processed_content_reflects_editor_content(self):
        self.editor_interface.current_contents += ", now with changes"
        self.controller.content_changed()

        self.controller.process_next()

        self.assertHasContent("Test Content, now with changes")

    def test_content_of_editor_can_be_set(self):
        self.controller.set_current_contents("Some other content")

        self.assertEqual(self.editor_interface.current_contents, "Some other content")

    def test_changed_content_is_processed_next_with_cursor_position(self):
        self.controller.content_changed()

        self.controller.process_next()

        self.assertHasCursorPosition((0,0))

    def test_processed_content_reflects_editor_cursor_position(self):
        self.editor_interface.cursor_position = (33,33)
        self.controller.content_changed()

        self.controller.process_next()

        self.assertHasCursorPosition((33,33))

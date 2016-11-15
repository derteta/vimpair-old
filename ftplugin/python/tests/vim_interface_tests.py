import unittest
from mock import Mock

from ..vim_interface import VimInterface


def create_mock_vim(contents):
    mock_vim = Mock()
    mock_vim.current = Mock()
    mock_vim.current.buffer = contents
    mock_vim.current.window = Mock()
    mock_vim.current.window.cursor = (1,0)
    return mock_vim


class VimInterfaceTests(unittest.TestCase):

    def test_returns_single_line_string_if_buffer_has_one_line(self):
        interface = VimInterface(vim=create_mock_vim(['Only one line']))

        self.assertEqual(interface.current_contents, 'Only one line')

    def test_returns_multi_line_string_if_buffer_has_more_than_one_line(self):
        interface = VimInterface(vim=create_mock_vim(
            ['This is the first line.', 'This is the second line.'])
        )

        self.assertEqual(
            interface.current_contents,
            'This is the first line.\nThis is the second line.'
        )

    def test_buffer_content_can_be_set_via_property(self):
        mock_vim = create_mock_vim(['Always has one line'])
        interface = VimInterface(vim=mock_vim)

        interface.current_contents = 'First line\nSecond line'

        self.assertEqual(mock_vim.current.buffer, ['First line', 'Second line'])

    def test_returns_normalised_cursor_position(self):
        mock_vim = create_mock_vim(['Only one line'])
        interface = VimInterface(vim=mock_vim)

        self.assertEqual(interface.cursor_position, (0, 0))

    def test_updates_cursor_position(self):
        mock_vim = create_mock_vim(['Only one line'])
        interface = VimInterface(vim=mock_vim)

        mock_vim.current.window.cursor = (11, 10)

        self.assertEqual(interface.cursor_position, (10, 10))

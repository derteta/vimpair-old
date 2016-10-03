import unittest
from mock import Mock

from ..vim_interface import VimInterface


def create_mock_vim(contents):
    mock_vim = Mock()
    mock_vim.current = Mock()
    mock_vim.current.buffer = contents
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

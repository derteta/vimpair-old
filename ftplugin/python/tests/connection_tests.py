import unittest
from mock import ANY, call, patch, Mock

import socket
from ..connection import ServerConnection


def fake_accept(self):
    return Mock(), 0

def fake_accept_with_real_socket(self):
    return socket.socket(), 0


class ServerConnectionTests(unittest.TestCase):

    @patch('socket.socket.setsockopt')
    def test_makes_soacket_address_reusable(self, setsockopt_mock):
        ServerConnection()

        setsockopt_mock.assert_called_with(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )

    @patch('socket.socket.accept', new_callable=lambda: fake_accept)
    @patch('socket.socket.bind')
    def test_binds_socket_to_an_address_in_connect(self, bind_mock, _):
        connection = ServerConnection()

        connection.connect()

        bind_mock.assert_called_with(ANY)

    @patch('socket.socket.accept', new_callable=lambda: fake_accept)
    @patch('socket.socket.bind')
    @patch('socket.socket.close')
    def test_closes_socket_in_disconnect(self, close_mock, _bind, _accept):
        connection = ServerConnection()
        connection.connect()

        connection.disconnect()

        close_mock.assert_called()

    @patch(
        'socket.socket.accept',
        new_callable=lambda: fake_accept_with_real_socket
    )
    @patch('socket.socket.bind')
    @patch('socket.socket.sendall')
    def test_calls_sendall_in_send(self, sendall_mock, _bind, _accept):
        connection = ServerConnection()
        connection.connect()

        connection.send('<message>')

        sendall_mock.assert_called_with('<message>')

    @patch('socket.socket.accept', new_callable=lambda: fake_accept)
    def test_send_calls_connect_implicitely_if_no_connection_established(self, _):
        connection = ServerConnection()
        connection.connect = Mock()

        connection.send('<message>')

        self.assertEqual(connection.connect.mock_calls, [call()])

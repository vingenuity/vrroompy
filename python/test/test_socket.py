#!/usr/bin/env python3
# pylint: disable=missing-function-docstring

"""
Contains unit tests for the module vrroompy.socket.
"""

import socket
import unittest
from unittest.mock import MagicMock, Mock, patch
from vrroompy.socket import Socket


class TestSocket(unittest.TestCase):
    """
    Unit tests the class vrroompy.Socket.
    """
    TEST_ADDRESS = "127.0.0.1"
    TEST_PORT = 2222

    def test_init_raises(self):
        """
        Tests that all Socket arguments are required at init.
        """
        with self.assertRaises(TypeError):
            Socket()
        with self.assertRaises(TypeError):
            Socket(self.TEST_ADDRESS)
        with self.assertRaises(TypeError):
            Socket(port=self.TEST_PORT)
        # Should not raise
        test_socket = Socket(self.TEST_ADDRESS, self.TEST_PORT)
        test_socket.close()

    def test_context_manager(self):
        socket_mock = Mock(spec=socket.socket)
        socket_mock.fileno = -1  # Simulate socket.socket closed
        with patch('socket.socket', return_value=socket_mock):

            with Socket(self.TEST_ADDRESS, self.TEST_PORT):
                socket_mock.fileno = 1  # Simulate socket.socket open
            socket_mock.connect.assert_called_once_with(
                (self.TEST_ADDRESS, self.TEST_PORT))
            socket_mock.close.assert_called_once()

    def test_socket_closed(self):
        socket_mock = Mock(spec=socket.socket)
        with patch('socket.socket', return_value=socket_mock):
            test_socket = Socket(self.TEST_ADDRESS, self.TEST_PORT)

            socket_mock.fileno = -1  # Simulate socket.socket closed
            self.assertTrue(test_socket.closed())

            socket_mock.fileno = 1  # Simulate socket.socket open
            self.assertFalse(test_socket.closed())

    def test_socket_close(self):
        socket_mock = Mock(spec=socket.socket)
        with patch('socket.socket', return_value=socket_mock):
            test_socket = Socket(self.TEST_ADDRESS, self.TEST_PORT)

            socket_mock.fileno = 1  # Simulate socket.socket open
            test_socket.close()
            socket_mock.close.assert_called_once()

            # close should not be called again if the socket is closed
            socket_mock.fileno = -1  # Simulate socket.socket closed
            test_socket.close()
            socket_mock.close.assert_called_once()

    def test_socket_connect(self):
        socket_mock = Mock(spec=socket.socket)
        with patch('socket.socket', return_value=socket_mock):
            test_socket = Socket(self.TEST_ADDRESS, self.TEST_PORT)

            socket_mock.fileno = -1  # Simulate socket.socket closed
            test_socket.connect()
            socket_mock.connect.assert_called_once_with(
                (self.TEST_ADDRESS, self.TEST_PORT))

            # Socket should not call connect() if already open
            socket_mock.fileno = 1  # Simulate socket.socket open
            test_socket.connect()
            socket_mock.connect.assert_called_once_with(
                (self.TEST_ADDRESS, self.TEST_PORT))

    def test_send_raw_command(self):
        socket_mock = Mock(spec=socket.socket)
        socket_mock.recv = Mock(return_value=b'inseltx1 3\r\n')
        with patch('socket.socket', return_value=socket_mock):
            test_socket = Socket(self.TEST_ADDRESS, self.TEST_PORT)

            test_socket.send_raw_command("get opmode")
            socket_mock.send.assert_called_once_with(b'get opmode\n')
            socket_mock.recv.assert_called_once()

            test_socket.send_raw_command("get inseltx0\n")
            socket_mock.send.assert_called_with(b'get inseltx0\n')

            test_response = test_socket.send_raw_command("get inseltx1\n")
            self.assertTrue(test_response == "inseltx1 3")


if __name__ == '__main__':
    unittest.main()  # pragma: no cover

#!/usr/bin/env python3
# pylint: disable=missing-function-docstring

"""
Contains unit tests for base commands in vrroompy.commands.
"""

import unittest
from unittest.mock import MagicMock, patch
from vrroompy.commands import get_command_base, set_command_base
from vrroompy.commands.input import Input

class TestBaseCommands(unittest.TestCase):
    """
    Unit tests the base command free functions.
    """

    @patch('socket.socket')
    def test_get_command_base_str(self, test_socket):
        # Simulate successful send and receive on test socket
        test_socket.sendall = MagicMock(return_value=None)
        test_socket.recv = MagicMock(return_value=b'opmode 2\r\n')

        command_output = get_command_base(
            test_socket,
            "opmode",
            ["[0-4]"],
            [str])

        test_socket.sendall.assert_called_once_with(b'get opmode\n')
        test_socket.recv.assert_called_once()
        self.assertEqual(command_output, ["2"])

    @patch('socket.socket')
    def test_get_command_base_custom(self, test_socket):
        # Simulate successful send and receive on test socket
        test_socket.sendall = MagicMock(return_value=None)
        test_socket.recv = MagicMock(return_value=b'insel 2 0\r\n')

        command_output = get_command_base(
            test_socket,
            "insel",
            [Input.pattern(), Input.pattern()],
            [Input.from_string, Input.from_string])

        test_socket.sendall.assert_called_once_with(b'get insel\n')
        test_socket.recv.assert_called_once()
        self.assertEqual(command_output, [Input.RX2, Input.RX0])

    @patch('socket.socket')
    def test_set_command_base_output_str(self, test_socket):
        # Simulate successful send and receive on test socket
        test_socket.sendall = MagicMock(return_value=None)
        test_socket.recv = MagicMock(return_value=b'opmode 1\r\n')

        set_command_base(
            test_socket,
            "opmode",
            "1",
            ["[0-4]"],
            [str])

        test_socket.sendall.assert_called_once_with(b'set opmode 1\n')
        test_socket.recv.assert_called_once()

    @patch('socket.socket')
    def test_set_command_base_output_custom(self, test_socket):
        # Simulate successful send and receive on test socket
        test_socket.sendall = MagicMock(return_value=None)
        test_socket.recv = MagicMock(return_value=b'insel 0 4\r\n')

        set_command_base(
            test_socket,
            "insel",
            [Input.RX0, Input.FOLLOW],
            [Input.pattern(), Input.pattern()],
            [Input.from_string, Input.from_string])

        test_socket.sendall.assert_called_once_with(b'set insel 0 4\n')
        test_socket.recv.assert_called_once()

    @patch('socket.socket')
    def test_set_command_base_raises(self, test_socket):
        with self.assertRaises(ValueError):
            # Simulate successful send, but with unexpected response
            test_socket.sendall = MagicMock(return_value=None)
            test_socket.recv = MagicMock(return_value=b'insel 0 2\r\n')

            set_command_base(
                test_socket,
                "insel",
                [Input.RX0, Input.FOLLOW],
                [Input.pattern(), Input.pattern()],
                [Input.from_string, Input.from_string])

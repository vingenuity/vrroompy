#!/usr/bin/env python3
# pylint: disable=missing-function-docstring

"""
Contains unit tests for enums & functions within vrroompy.commands.input.
"""

import unittest
from unittest.mock import MagicMock, patch
from vrroompy.commands.input import *

class TestInput(unittest.TestCase):
    """
    Unit tests the Input enumeration.
    """

    def test_str(self):
        self.assertEqual(str(Input.RX0), "0")
        self.assertEqual(str(Input.RX1), "1")
        self.assertEqual(str(Input.RX2), "2")
        self.assertEqual(str(Input.RX3), "3")
        self.assertEqual(str(Input.FOLLOW), "4")

    def test_from_string(self):
        self.assertEqual(Input.from_string("0"), Input.RX0)
        self.assertEqual(Input.from_string("1"), Input.RX1)
        self.assertEqual(Input.from_string("2"), Input.RX2)
        self.assertEqual(Input.from_string("3"), Input.RX3)
        self.assertEqual(Input.from_string("4"), Input.FOLLOW)
    
    def test_pattern(self):
        self.assertEqual(Input.pattern(), "[0-4]")


class TestInputCommands(unittest.TestCase):
    """
    Unit tests the free functions for setting inputs.
    """

    @patch('socket.socket')
    def test_get_selected_inputs(self, test_socket):
        # Simulate successful send and receive on test socket
        test_socket.sendall = MagicMock(return_value=None)
        test_socket.recv = MagicMock(return_value=b'insel 2 3\r\n')

        self.assertEqual(get_selected_inputs(test_socket), [Input.RX2, Input.RX3])
        test_socket.sendall.assert_called_once_with(b'get insel\n')
        test_socket.recv.assert_called_once()

    @patch('socket.socket')
    def test_set_selected_inputs(self, test_socket):
        # Simulate successful send and receive on test socket
        test_socket.sendall = MagicMock(return_value=None)
        test_socket.recv = MagicMock(return_value=b'insel 0 4\r\n')

        set_selected_inputs(test_socket, Input.RX0, Input.FOLLOW)
        test_socket.sendall.assert_called_once_with(b'set insel 0 4\n')
        test_socket.recv.assert_called_once()

    @patch('socket.socket')
    def test_get_selected_input_tx0(self, test_socket):
        # Simulate successful send and receive on test socket
        test_socket.sendall = MagicMock(return_value=None)
        test_socket.recv = MagicMock(return_value=b'inseltx0 0\r\n')

        self.assertEqual(get_selected_input_tx0(test_socket), Input.RX0)
        test_socket.sendall.assert_called_once_with(b'get inseltx0\n')
        test_socket.recv.assert_called_once()

    @patch('socket.socket')
    def test_set_selected_input_tx0(self, test_socket):
        # Simulate successful send and receive on test socket
        test_socket.sendall = MagicMock(return_value=None)
        test_socket.recv = MagicMock(return_value=b'inseltx0 2\r\n')

        set_selected_input_tx0(test_socket, Input.RX2)
        test_socket.sendall.assert_called_once_with(b'set inseltx0 2\n')
        test_socket.recv.assert_called_once()

    @patch('socket.socket')
    def test_get_selected_input_tx1(self, test_socket):
        # Simulate successful send and receive on test socket
        test_socket.sendall = MagicMock(return_value=None)
        test_socket.recv = MagicMock(return_value=b'inseltx1 3\r\n')

        self.assertEqual(get_selected_input_tx1(test_socket), Input.RX3)
        test_socket.sendall.assert_called_once_with(b'get inseltx1\n')
        test_socket.recv.assert_called_once()

    @patch('socket.socket')
    def test_set_selected_input_tx1(self, test_socket):
        # Simulate successful send and receive on test socket
        test_socket.sendall = MagicMock(return_value=None)
        test_socket.recv = MagicMock(return_value=b'inseltx1 4\r\n')

        set_selected_input_tx1(test_socket, Input.FOLLOW)
        test_socket.sendall.assert_called_once_with(b'set inseltx1 4\n')
        test_socket.recv.assert_called_once()
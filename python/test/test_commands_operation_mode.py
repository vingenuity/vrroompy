#!/usr/bin/env python3
# pylint: disable=missing-function-docstring

"""
Contains unit tests for enums & functions within vrroompy.commands.operation_mode.
"""

import unittest
from unittest.mock import MagicMock, patch
from vrroompy.commands.operation_mode import *

class TestOperationMode(unittest.TestCase):
    """
    Unit tests the OperationMode enumeration.
    """

    def test_str(self):
        self.assertEqual(str(OperationMode.SPLITTER_VRR), "0")
        self.assertEqual(str(OperationMode.SPLITTER_UPSCALE), "1")
        self.assertEqual(str(OperationMode.MATRIX_TMDS), "2")
        self.assertEqual(str(OperationMode.MATRIX_TMDS_DOWNSCALE), "3")
        self.assertEqual(str(OperationMode.MATRIX_FRL5_TMDS), "4")

    def test_from_string(self):
        self.assertEqual(OperationMode.from_string("0"), OperationMode.SPLITTER_VRR)
        self.assertEqual(OperationMode.from_string("1"), OperationMode.SPLITTER_UPSCALE)
        self.assertEqual(OperationMode.from_string("2"), OperationMode.MATRIX_TMDS)
        self.assertEqual(OperationMode.from_string("3"), OperationMode.MATRIX_TMDS_DOWNSCALE)
        self.assertEqual(OperationMode.from_string("4"), OperationMode.MATRIX_FRL5_TMDS)
    
    def test_pattern(self):
        self.assertEqual(OperationMode.pattern(), "[0-4]")


class TestOperationModeCommands(unittest.TestCase):
    """
    Unit tests the free functions for setting operation modes.
    """

    @patch('socket.socket')
    def test_get_operation_mode(self, test_socket):
        # Simulate successful send and receive on test socket
        test_socket.sendall = MagicMock(return_value=None)
        test_socket.recv = MagicMock(return_value=b'opmode 2\r\n')

        self.assertEqual(get_operation_mode(test_socket), OperationMode.MATRIX_TMDS)
        test_socket.sendall.assert_called_once_with(b'get opmode\n')
        test_socket.recv.assert_called_once()

    @patch('socket.socket')
    def test_set_operation_mode(self, test_socket):
        # Simulate successful send and receive on test socket
        test_socket.sendall = MagicMock(return_value=None)
        test_socket.recv = MagicMock(return_value=b'opmode 0\r\n')

        set_operation_mode(test_socket, OperationMode.SPLITTER_VRR)
        test_socket.sendall.assert_called_once_with(b'set opmode 0\n')
        test_socket.recv.assert_called_once()
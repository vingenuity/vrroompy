#!/usr/bin/env python3
# pylint: disable=missing-function-docstring

"""
Contains unit tests for enums & functions within vrroompy.commands.actions.
"""

import unittest
from unittest.mock import MagicMock, patch
from vrroompy.commands.actions import *


class TestResetDataType(unittest.TestCase):
    """
    Unit tests the ResetDataType enumeration.
    """

    def test_str(self):
        self.assertEqual(str(ResetDataType.RESET_SETTINGS), "1")
        self.assertEqual(str(ResetDataType.RESET_EDID_TABLES), "2")
        self.assertEqual(str(ResetDataType.RESET_ALL), "3")

    def test_from_string(self):
        self.assertEqual(ResetDataType.from_string("1"), ResetDataType.RESET_SETTINGS)
        self.assertEqual(
            ResetDataType.from_string("2"), ResetDataType.RESET_EDID_TABLES
        )
        self.assertEqual(ResetDataType.from_string("3"), ResetDataType.RESET_ALL)

    def test_pattern(self):
        self.assertEqual(ResetDataType.pattern(), "[1-3]")


class TestFactoryResetCommand(unittest.TestCase):
    """
    Unit tests the free function to factory reset the switch.
    """

    @patch("socket.socket")
    def test_factory_reset_all(self, test_socket):
        # Simulate successful send and receive on test socket
        test_socket.sendall = MagicMock(return_value=None)
        test_socket.recv = MagicMock(return_value=b"factoryreset 3\r\n")

        factory_reset(test_socket, ResetDataType.RESET_ALL)
        test_socket.sendall.assert_called_once_with(b"set factoryreset 3\n")
        test_socket.recv.assert_called_once()

    @patch("socket.socket")
    def test_factory_reset_edid_tables(self, test_socket):
        # Simulate successful send and receive on test socket
        test_socket.sendall = MagicMock(return_value=None)
        test_socket.recv = MagicMock(return_value=b"factoryreset 2\r\n")

        factory_reset(test_socket, ResetDataType.RESET_EDID_TABLES)
        test_socket.sendall.assert_called_once_with(b"set factoryreset 2\n")
        test_socket.recv.assert_called_once()

    @patch("socket.socket")
    def test_factory_reset_settings(self, test_socket):
        # Simulate successful send and receive on test socket
        test_socket.sendall = MagicMock(return_value=None)
        test_socket.recv = MagicMock(return_value=b"factoryreset 1\r\n")

        factory_reset(test_socket, ResetDataType.RESET_SETTINGS)
        test_socket.sendall.assert_called_once_with(b"set factoryreset 1\n")
        test_socket.recv.assert_called_once()


class TestHotplugCommand(unittest.TestCase):
    """
    Unit tests the free function to issue a hotplug event to the switch's inputs.
    """

    @patch("socket.socket")
    def test_hotplug(self, test_socket):
        # Simulate successful send and receive on test socket
        test_socket.sendall = MagicMock(return_value=None)
        test_socket.recv = MagicMock(return_value=b"hotplug\r\n")

        hotplug(test_socket)
        test_socket.sendall.assert_called_once_with(b"set hotplug\n")
        test_socket.recv.assert_called_once()


class TestRebootCommand(unittest.TestCase):
    """
    Unit tests the free function to reboot the switch.
    """

    @patch("socket.socket")
    def test_set_reboot(self, test_socket):
        # Simulate successful send and receive on test socket
        test_socket.sendall = MagicMock(return_value=None)
        test_socket.recv = MagicMock(return_value=b"reboot\r\n")

        reboot(test_socket)
        test_socket.sendall.assert_called_once_with(b"set reboot\n")
        test_socket.recv.assert_called_once()

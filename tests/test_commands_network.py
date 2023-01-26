#!/usr/bin/env python3

"""
Contains unit tests for enums & functions within vrroompy.commands.network.
"""

from re import fullmatch
import unittest
from unittest.mock import MagicMock, patch
from vrroompy.commands.network import *


class TestIpAddressV4(unittest.TestCase):
    """
    Unit tests the IpAddressV4 enumeration.
    """

    def test_str(self):
        self.assertEqual(str(IpAddressV4("192.168.1.1")), "192.168.1.1")

    def test_from_string(self):
        self.assertEqual(
            IpAddressV4.from_string("192.168.1.1"), IpAddressV4("192.168.1.1")
        )

    def test_pattern(self):
        self.assertIsNotNone(fullmatch(IpAddressV4.pattern(), "192.168.1.1"))
        self.assertIsNotNone(fullmatch(IpAddressV4.pattern(), "0.0.0.0"))
        self.assertIsNotNone(fullmatch(IpAddressV4.pattern(), "255.255.255.255"))
        self.assertIsNone(fullmatch(IpAddressV4.pattern(), "256.0.0.0"))
        self.assertIsNone(fullmatch(IpAddressV4.pattern(), "0.0.0.256"))


class TestTcpPort(unittest.TestCase):
    """
    Unit tests the TcpPort class.
    """

    def test_str(self):
        self.assertEqual(str(TcpPort(2222)), "2222")

    def test_from_string(self):
        self.assertEqual(TcpPort.from_string("80"), TcpPort(80))

    def test_pattern(self):
        self.assertIsNone(fullmatch(TcpPort.pattern(), "0"))
        self.assertIsNotNone(fullmatch(TcpPort.pattern(), "1"))
        self.assertIsNotNone(fullmatch(TcpPort.pattern(), "65535"))
        self.assertIsNone(fullmatch(TcpPort.pattern(), "65536"))
        self.assertIsNone(fullmatch(TcpPort.pattern(), "99999"))
        self.assertIsNone(fullmatch(TcpPort.pattern(), "655350"))


class TestMacAddress(unittest.TestCase):
    """
    Unit tests the MacAddress class.
    """

    def test_str(self):
        self.assertEqual(str(MacAddress("19:AC:B5:D3:22:F4")), "19:AC:B5:D3:22:F4")

    def test_from_string(self):
        self.assertEqual(
            MacAddress.from_string("19:AC:B5:D3:22:F4"), MacAddress("19:AC:B5:D3:22:F4")
        )

    def test_pattern(self):
        # Pattern allows for hyphenated form, even though it's not what the VRROOM sends.
        self.assertIsNotNone(fullmatch(MacAddress.pattern(), "19:AC:B5:D3:E2:F4"))
        self.assertIsNotNone(fullmatch(MacAddress.pattern(), "19-AC-B5-D3-E2-F4"))
        # Ensure that lowercase also works
        self.assertIsNotNone(fullmatch(MacAddress.pattern(), "19:ac:b5:d3:e2:f4"))
        self.assertIsNotNone(fullmatch(MacAddress.pattern(), "19-ac-b5-d3-e2-f4"))
        # Verify that the length must be correct
        self.assertIsNone(fullmatch(MacAddress.pattern(), "19:AC:B5:D3:22"))
        self.assertIsNone(fullmatch(MacAddress.pattern(), "19:AC:B5:D3:22:F4:BB"))
        # Verify that each section must be exactly two hexadecimal numbers
        self.assertIsNone(fullmatch(MacAddress.pattern(), "19:AC:B5:D3D:22:F4:BB"))
        self.assertIsNone(fullmatch(MacAddress.pattern(), "1:AC:B5:D3:22:F4:BB"))


class TestIpCommands(unittest.TestCase):
    """
    Unit tests the free functions for getting/setting IP addresses.
    """

    @patch("socket.socket")
    def test_get_ip_address(self, test_socket):
        # Simulate successful send and receive on test socket
        test_socket.sendall = MagicMock(return_value=None)
        test_socket.recv = MagicMock(return_value=b"ipaddr 192.168.1.128\r\n")

        self.assertEqual(get_ip_address(test_socket), IpAddressV4("192.168.1.128"))
        test_socket.sendall.assert_called_once_with(b"get ipaddr\n")
        test_socket.recv.assert_called_once()

    @patch("socket.socket")
    def test_set_ip_address(self, test_socket):
        # Simulate successful send and receive on test socket
        test_socket.sendall = MagicMock(return_value=None)
        test_socket.recv = MagicMock(return_value=b"ipaddr 208.67.222.222\r\n")

        set_ip_address(test_socket, IpAddressV4("208.67.222.222"))
        test_socket.sendall.assert_called_once_with(b"set ipaddr 208.67.222.222\n")
        test_socket.recv.assert_called_once()

    @patch("socket.socket")
    def test_get_ip_network_mask(self, test_socket):
        # Simulate successful send and receive on test socket
        test_socket.sendall = MagicMock(return_value=None)
        test_socket.recv = MagicMock(return_value=b"ipmask 255.255.255.0\r\n")

        self.assertEqual(get_ip_network_mask(test_socket), IpAddressV4("255.255.255.0"))
        test_socket.sendall.assert_called_once_with(b"get ipmask\n")
        test_socket.recv.assert_called_once()

    @patch("socket.socket")
    def test_set_ip_network_mask(self, test_socket):
        # Simulate successful send and receive on test socket
        test_socket.sendall = MagicMock(return_value=None)
        test_socket.recv = MagicMock(return_value=b"ipmask 255.0.0.0\r\n")

        set_ip_network_mask(test_socket, IpAddressV4("255.0.0.0"))
        test_socket.sendall.assert_called_once_with(b"set ipmask 255.0.0.0\n")
        test_socket.recv.assert_called_once()

    @patch("socket.socket")
    def test_get_ip_gateway(self, test_socket):
        # Simulate successful send and receive on test socket
        test_socket.sendall = MagicMock(return_value=None)
        test_socket.recv = MagicMock(return_value=b"ipgw 192.168.1.1\r\n")

        self.assertEqual(get_ip_gateway(test_socket), IpAddressV4("192.168.1.1"))
        test_socket.sendall.assert_called_once_with(b"get ipgw\n")
        test_socket.recv.assert_called_once()

    @patch("socket.socket")
    def test_set_ip_gateway(self, test_socket):
        # Simulate successful send and receive on test socket
        test_socket.sendall = MagicMock(return_value=None)
        test_socket.recv = MagicMock(return_value=b"ipgw 208.67.222.220\r\n")

        set_ip_gateway(test_socket, IpAddressV4("208.67.222.220"))
        test_socket.sendall.assert_called_once_with(b"set ipgw 208.67.222.220\n")
        test_socket.recv.assert_called_once()


class TestIpOnOffCommands(unittest.TestCase):
    """
    Unit tests the IP free functions using on/off switches.
    """

    @patch("socket.socket")
    def test_get_dhcp_enabled(self, test_socket):
        # Simulate successful send and receive on test socket
        test_socket.sendall = MagicMock(return_value=None)
        test_socket.recv = MagicMock(return_value=b"dhcp off\r\n")

        self.assertEqual(get_dhcp_enabled(test_socket), False)
        test_socket.sendall.assert_called_once_with(b"get dhcp\n")
        test_socket.recv.assert_called_once()

    @patch("socket.socket")
    def test_set_dhcp_enabled(self, test_socket):
        # Simulate successful send and receive on test socket
        test_socket.sendall = MagicMock(return_value=None)
        test_socket.recv = MagicMock(return_value=b"dhcp on\r\n")

        set_dhcp_enabled(test_socket, True)
        test_socket.sendall.assert_called_once_with(b"set dhcp on\n")
        test_socket.recv.assert_called_once()

    @patch("socket.socket")
    def test_get_ip_interrupts_enabled(self, test_socket):
        # Simulate successful send and receive on test socket
        test_socket.sendall = MagicMock(return_value=None)
        test_socket.recv = MagicMock(return_value=b"ipinterrupt off\r\n")

        self.assertEqual(get_ip_interrupts_enabled(test_socket), False)
        test_socket.sendall.assert_called_once_with(b"get ipinterrupt\n")
        test_socket.recv.assert_called_once()

    @patch("socket.socket")
    def test_set_ip_interrupts_enabled(self, test_socket):
        # Simulate successful send and receive on test socket
        test_socket.sendall = MagicMock(return_value=None)
        test_socket.recv = MagicMock(return_value=b"ipinterrupt on\r\n")

        set_ip_interrupts_enabled(test_socket, True)
        test_socket.sendall.assert_called_once_with(b"set ipinterrupt on\n")
        test_socket.recv.assert_called_once()


class TestTcpPortCommand(unittest.TestCase):
    """
    Unit tests the free function using TCP ports.
    """

    @patch("socket.socket")
    def test_get_tcp_port(self, test_socket):
        # Simulate successful send and receive on test socket
        test_socket.sendall = MagicMock(return_value=None)
        test_socket.recv = MagicMock(return_value=b"tcpport 2222\r\n")

        self.assertEqual(get_tcp_port(test_socket), TcpPort(2222))
        test_socket.sendall.assert_called_once_with(b"get tcpport\n")
        test_socket.recv.assert_called_once()

    @patch("socket.socket")
    def test_set_tcp_port(self, test_socket):
        # Simulate successful send and receive on test socket
        test_socket.sendall = MagicMock(return_value=None)
        test_socket.recv = MagicMock(return_value=b"tcpport 80\r\n")

        set_tcp_port(test_socket, TcpPort(80))
        test_socket.sendall.assert_called_once_with(b"set tcpport 80\n")
        test_socket.recv.assert_called_once()


class TestMacAddressCommand(unittest.TestCase):
    """
    Unit tests the free function for MAC addresses.
    """

    @patch("socket.socket")
    def test_get_mac_address(self, test_socket):
        # Simulate successful send and receive on test socket
        test_socket.sendall = MagicMock(return_value=None)
        test_socket.recv = MagicMock(return_value=b"mac 19:AC:B5:D3:22:F4\r\n")

        self.assertEqual(get_mac_address(test_socket), MacAddress("19:AC:B5:D3:22:F4"))
        test_socket.sendall.assert_called_once_with(b"get mac\n")
        test_socket.recv.assert_called_once()

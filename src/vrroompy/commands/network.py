#!/usr/bin/env python3

"""
Contains free functions for getting/setting VRROOM network settings.
"""

import socket
from typing import Any
from . import get_command_base, set_command_base
from .enums import OnOffSwitch, Target


class IpAddressV4:
    """
    Defines valid IPv4 addresses.
    """

    def __init__(self, address: str) -> None:
        self.__address = address

    def __eq__(self, obj: Any) -> bool:
        return isinstance(obj, IpAddressV4) and (self.__address == obj.__address)

    def __str__(self) -> str:
        return self.__address

    @staticmethod
    def from_string(string: str) -> "IpAddressV4":
        """
        Converts a string into an instance of this class, if valid.
        """
        return IpAddressV4(string)

    @staticmethod
    def pattern() -> str:
        """
        Returns a valid regex pattern for this class.
        """
        return "((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])"


__VALUE_CONVERTERS_IP_ADDRESS = [IpAddressV4.from_string]
__VALUE_PATTERNS_IP_ADDRESS = [IpAddressV4.pattern()]


def get_ip_address(socket: socket) -> IpAddressV4:
    """
    Gets the current IP address of the switch.
    """
    returned_values = get_command_base(
        socket,
        Target.IP_ADDRESS,
        __VALUE_PATTERNS_IP_ADDRESS,
        __VALUE_CONVERTERS_IP_ADDRESS,
    )
    return returned_values[0]


def set_ip_address(socket: socket, address: IpAddressV4) -> None:
    """
    Sets the IP address of the switch.
    """
    set_command_base(
        socket,
        Target.IP_ADDRESS,
        [address],
        __VALUE_PATTERNS_IP_ADDRESS,
        __VALUE_CONVERTERS_IP_ADDRESS,
    )


def get_ip_network_mask(socket: socket) -> IpAddressV4:
    """
    Gets the current IP network mask of the switch.
    """
    returned_values = get_command_base(
        socket,
        Target.IP_NETWORK_MASK,
        __VALUE_PATTERNS_IP_ADDRESS,
        __VALUE_CONVERTERS_IP_ADDRESS,
    )
    return returned_values[0]


def set_ip_network_mask(socket: socket, address: IpAddressV4) -> None:
    """
    Sets the IP network mask of the switch.
    """
    set_command_base(
        socket,
        Target.IP_NETWORK_MASK,
        [address],
        __VALUE_PATTERNS_IP_ADDRESS,
        __VALUE_CONVERTERS_IP_ADDRESS,
    )


def get_ip_gateway(socket: socket) -> IpAddressV4:
    """
    Gets the current IP gateway of the switch.
    """
    returned_values = get_command_base(
        socket,
        Target.IP_GATEWAY,
        __VALUE_PATTERNS_IP_ADDRESS,
        __VALUE_CONVERTERS_IP_ADDRESS,
    )
    return returned_values[0]


def set_ip_gateway(socket: socket, address: IpAddressV4) -> None:
    """
    Sets the IP gateway of the switch.
    """
    set_command_base(
        socket,
        Target.IP_GATEWAY,
        [address],
        __VALUE_PATTERNS_IP_ADDRESS,
        __VALUE_CONVERTERS_IP_ADDRESS,
    )


__VALUE_CONVERTERS_ONOFF = [OnOffSwitch.from_string]
__VALUE_PATTERNS_ONOFF = [OnOffSwitch.pattern()]


def get_dhcp_enabled(socket: socket) -> bool:
    """
    Gets whether DHCP is enabled on the switch.
    """
    returned_values = get_command_base(
        socket,
        Target.DHCP_ENABLED,
        __VALUE_PATTERNS_ONOFF,
        __VALUE_CONVERTERS_ONOFF,
    )
    return OnOffSwitch.to_bool(returned_values[0])


def set_dhcp_enabled(socket: socket, enabled: bool) -> None:
    """
    Enables/disables DHCP on the switch.
    """
    set_command_base(
        socket,
        Target.DHCP_ENABLED,
        [OnOffSwitch.from_bool(enabled)],
        __VALUE_PATTERNS_ONOFF,
        __VALUE_CONVERTERS_ONOFF,
    )


def get_ip_interrupts_enabled(socket: socket) -> bool:
    """
    Gets whether IP interrupts are enabled on the switch.
    """
    returned_values = get_command_base(
        socket,
        Target.IP_INTERRUPTS_ENABLED,
        __VALUE_PATTERNS_ONOFF,
        __VALUE_CONVERTERS_ONOFF,
    )
    return OnOffSwitch.to_bool(returned_values[0])


def set_ip_interrupts_enabled(socket: socket, enabled: bool) -> None:
    """
    Enables/disables IP interrupts on the switch.
    """
    set_command_base(
        socket,
        Target.IP_INTERRUPTS_ENABLED,
        [OnOffSwitch.from_bool(enabled)],
        __VALUE_PATTERNS_ONOFF,
        __VALUE_CONVERTERS_ONOFF,
    )


class TcpPort:
    """
    Defines valid TCP ports.
    """

    def __init__(self, port: int) -> None:
        self.__port = port

    def __eq__(self, obj: Any) -> bool:
        return isinstance(obj, TcpPort) and (self.__port == obj.__port)

    def __str__(self) -> str:
        return str(self.__port)

    @staticmethod
    def from_string(string: str) -> "TcpPort":
        """
        Converts a string into an instance of this class, if valid.
        """
        return TcpPort(int(string))

    @staticmethod
    def pattern() -> str:
        """
        Returns a valid regex pattern for this class.
        """
        return "([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])"


__VALUE_CONVERTERS_TCP_PORT = [TcpPort.from_string]
__VALUE_PATTERNS_TCP_PORT = [TcpPort.pattern()]


def get_tcp_port(socket: socket) -> TcpPort:
    """
    Gets what TCP port is being used for commands on the switch.
    """
    returned_values = get_command_base(
        socket,
        Target.TCP_PORT,
        __VALUE_PATTERNS_TCP_PORT,
        __VALUE_CONVERTERS_TCP_PORT,
    )
    return returned_values[0]


def set_tcp_port(socket: socket, port: TcpPort) -> None:
    """
    Sets what TCP port is being used for commands on the switch.
    """
    set_command_base(
        socket,
        Target.TCP_PORT,
        [port],
        __VALUE_PATTERNS_TCP_PORT,
        __VALUE_CONVERTERS_TCP_PORT,
    )


class MacAddress:
    """
    Defines valid MAC addresses.
    """

    def __init__(self, mac: str) -> None:
        self.__mac = mac

    def __eq__(self, obj: Any) -> bool:
        return isinstance(obj, MacAddress) and (self.__mac == obj.__mac)

    def __str__(self) -> str:
        return str(self.__mac)

    @staticmethod
    def from_string(string: str) -> "MacAddress":
        """
        Converts a string into an instance of this class, if valid.
        """
        return MacAddress(string)

    @staticmethod
    def pattern() -> str:
        """
        Returns a valid regex pattern for this class.
        """
        return "([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})"


__VALUE_CONVERTERS_MAC_ADDRESS = [MacAddress.from_string]
__VALUE_PATTERNS_MAC_ADDRESS = [MacAddress.pattern()]


def get_mac_address(socket: socket) -> MacAddress:
    """
    Gets the MAC address of the switch.
    """
    returned_values = get_command_base(
        socket,
        Target.MAC_ADDRESS,
        __VALUE_PATTERNS_MAC_ADDRESS,
        __VALUE_CONVERTERS_MAC_ADDRESS,
    )
    return returned_values[0]

#!/usr/bin/env python3

"""
Contains free functions for executing actions on the VRROOM switch.
"""

from enum import IntEnum
import socket

from . import set_command_base
from .enums import Target


class ResetDataType(IntEnum):
    """
    Enumerates the types of data that can be reset on the VRROOM switch.
    """

    RESET_SETTINGS = 1
    RESET_EDID_TABLES = 2
    RESET_ALL = 3

    def __str__(self):
        return str(self.value)

    @staticmethod
    def from_string(string: str) -> "ResetDataType":
        """
        Converts a string into a value of this enumeration, if possible.
        """
        return ResetDataType(int(string))

    @staticmethod
    def pattern() -> str:
        """
        Returns a regex pattern that matches values of this enumeration.
        """
        return f"[{ResetDataType.RESET_SETTINGS}-{ResetDataType.RESET_ALL}]"


def factory_reset(socket: socket.socket, reset_data: ResetDataType) -> None:
    """
    Resets the requested data on the VRROOM switch.
    """
    set_command_base(
        socket,
        Target.ACTION_FACTORY_RESET,
        [reset_data],
        [ResetDataType.pattern()],
        [ResetDataType.from_string],
    )


def hotplug(socket: socket.socket) -> None:
    """
    Sends a hotplug event to the sources on the VRROOM switch.
    """
    set_command_base(socket, Target.ACTION_HOTPLUG, [], [], [])


def reboot(socket: socket.socket) -> None:
    """
    Reboots the VRROOM switch.
    """
    set_command_base(socket, Target.ACTION_REBOOT, [], [], [])

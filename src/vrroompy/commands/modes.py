#!/usr/bin/env python3

"""
Contains free functions for getting/setting various VRROOM modes.
"""

from enum import IntEnum
import socket
from . import get_command_base, set_command_base
from .enums import OnOffSwitch, Target


class OperationMode(IntEnum):
    """
    Enumerates the operation modes of the VRROOM switch.
    """

    SPLITTER_VRR = 0
    SPLITTER_UPSCALE = 1
    MATRIX_TMDS = 2
    MATRIX_TMDS_DOWNSCALE = 3
    MATRIX_FRL5_TMDS = 4

    def __str__(self):
        return str(self.value)

    @staticmethod
    def from_string(string: str) -> "OperationMode":
        """
        Converts a string into a value of this enumeration, if possible.
        """
        return OperationMode(int(string))

    @staticmethod
    def pattern() -> str:
        """
        Returns a regex pattern that matches values of this enumeration.
        """
        return f"[{OperationMode.SPLITTER_VRR}-{OperationMode.MATRIX_FRL5_TMDS}]"


__VALUE_CONVERTERS_MODE_OPERATION = [OperationMode.from_string]
__VALUE_PATTERNS_MODE_OPERATION = [OperationMode.pattern()]


def get_operation_mode(socket: socket) -> OperationMode:
    """
    Gets the current operation mode of the switch.
    """
    returned_values = get_command_base(
        socket,
        Target.OPERATION_MODE,
        __VALUE_PATTERNS_MODE_OPERATION,
        __VALUE_CONVERTERS_MODE_OPERATION,
    )
    return returned_values[0]


def set_operation_mode(socket: socket, op_mode: OperationMode) -> None:
    """
    Sets the operation mode of the switch.
    """
    set_command_base(
        socket,
        Target.OPERATION_MODE,
        [op_mode],
        __VALUE_PATTERNS_MODE_OPERATION,
        __VALUE_CONVERTERS_MODE_OPERATION,
    )


__VALUE_CONVERTERS_MODE_AUTOSWITCH = [OnOffSwitch.from_string]
__VALUE_PATTERNS_MODE_AUTOSWITCH = [OnOffSwitch.pattern()]


def get_autoswitch_enabled(socket: socket) -> bool:
    """
    Gets whether automatic input switching is enabled on the switch.
    """
    returned_values = get_command_base(
        socket,
        Target.AUTO_SWITCHING,
        __VALUE_PATTERNS_MODE_AUTOSWITCH,
        __VALUE_CONVERTERS_MODE_AUTOSWITCH,
    )
    return OnOffSwitch.to_bool(returned_values[0])


def set_autoswitch_enabled(socket: socket, enabled: bool) -> None:
    """
    Enables/disables automatic input switching on the switch.
    """
    set_command_base(
        socket,
        Target.AUTO_SWITCHING,
        [OnOffSwitch.from_bool(enabled)],
        __VALUE_PATTERNS_MODE_AUTOSWITCH,
        __VALUE_CONVERTERS_MODE_AUTOSWITCH,
    )

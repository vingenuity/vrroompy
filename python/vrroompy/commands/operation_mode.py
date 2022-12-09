#!/usr/bin/env python3

"""
Contains free functions for getting/setting VRROOM operation modes.
"""

from enum import IntEnum
import socket
from . import get_command_base, set_command_base


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


__TARGET_OPMODE = "opmode"
__VALUE_CONVERTERS_OPMODE = [OperationMode.from_string]
__VALUE_PATTERNS_OPMODE = [OperationMode.pattern()]


def get_operation_mode(socket: socket) -> OperationMode:
    """
    Gets the current operation mode of the switch.
    """
    returned_values = get_command_base(
        socket, __TARGET_OPMODE, __VALUE_PATTERNS_OPMODE, __VALUE_CONVERTERS_OPMODE
    )
    return returned_values[0]


def set_operation_mode(socket: socket, op_mode: OperationMode) -> None:
    """
    Sets the operation mode of the switch.
    """
    set_command_base(
        socket,
        __TARGET_OPMODE,
        [op_mode],
        __VALUE_PATTERNS_OPMODE,
        __VALUE_CONVERTERS_OPMODE,
    )

#!/usr/bin/env python3

"""
Contains free functions for getting/setting VRROOM inputs.
"""

from enum import IntEnum
import socket
from typing import List
from . import get_command_base, set_command_base


class Input(IntEnum):
    """
    Enumerates the selectable inputs on the VRROOM switch.
    """
    RX0 = 0
    RX1 = 1
    RX2 = 2
    RX3 = 3
    FOLLOW = 4

    def __str__(self):
        return str(self.value)

    @staticmethod
    def from_string(string: str) -> "Input":
        """
        Converts a string into a value of this enumeration, if possible.
        """
        return Input(int(string))

    @staticmethod
    def pattern() -> str:
        """
        Returns a regex pattern that matches values of this enumeration.
        """
        return "[{0}-{1}]".format(Input.RX0, Input.FOLLOW)


__TARGET_SELECTED_INPUTS = "insel"
__VALUE_CONVERTERS_SELECTED_INPUTS = [Input.from_string, Input.from_string]
__VALUE_PATTERNS_SELECTED_INPUTS = [Input.pattern(), Input.pattern()]

def get_selected_inputs(socket: socket.socket) -> List[Input]:
    """
    Gets the currently selected inputs of the switch.
    """
    return get_command_base(
        socket,
        __TARGET_SELECTED_INPUTS,
        __VALUE_PATTERNS_SELECTED_INPUTS,
        __VALUE_CONVERTERS_SELECTED_INPUTS)

def set_selected_inputs(socket: socket.socket, 
                        input_tx0: Input,
                        input_tx1: Input) -> None:
    """
    Sets the currently selected inputs of the switch.
    """
    set_command_base(
        socket,
        __TARGET_SELECTED_INPUTS,
        [input_tx0, input_tx1],
        __VALUE_PATTERNS_SELECTED_INPUTS,
        __VALUE_CONVERTERS_SELECTED_INPUTS)


__TARGET_SELECTED_INPUT_TX0 = "inseltx0"
__TARGET_SELECTED_INPUT_TX1 = "inseltx1"
__VALUE_CONVERTERS_SELECTED_INPUT_TXN = [Input.from_string]
__VALUE_PATTERNS_SELECTED_INPUT_TXN = [Input.pattern()]

def get_selected_input_tx0(socket: socket.socket) -> List[Input]:
    """
    Gets the currently selected inputs of the switch.
    """
    return get_command_base(
        socket,
        __TARGET_SELECTED_INPUT_TX0,
        __VALUE_PATTERNS_SELECTED_INPUT_TXN,
        __VALUE_CONVERTERS_SELECTED_INPUT_TXN)

def get_selected_input_tx1(socket: socket.socket) -> List[Input]:
    """
    Gets the currently selected inputs of the switch.
    """
    return get_command_base(
        socket,
        __TARGET_SELECTED_INPUT_TX1,
        __VALUE_PATTERNS_SELECTED_INPUT_TXN,
        __VALUE_CONVERTERS_SELECTED_INPUT_TXN)

def set_selected_input_tx0(socket: socket.socket, input: Input) -> None:
    """
    Sets the currently selected inputs of the switch.
    """
    set_command_base(
        socket,
        __TARGET_SELECTED_INPUT_TX0,
        [input],
        __VALUE_PATTERNS_SELECTED_INPUT_TXN,
        __VALUE_CONVERTERS_SELECTED_INPUT_TXN)

def set_selected_input_tx1(socket: socket.socket, input: Input) -> None:
    """
    Sets the currently selected inputs of the switch.
    """
    set_command_base(
        socket,
        __TARGET_SELECTED_INPUT_TX1,
        [input],
        __VALUE_PATTERNS_SELECTED_INPUT_TXN,
        __VALUE_CONVERTERS_SELECTED_INPUT_TXN)

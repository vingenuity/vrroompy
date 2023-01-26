#!/usr/bin/env python3

import socket
from typing import Any, Callable, List

from ..codec import Codec
from ..exceptions import InvalidTargetError, ValueNotChangedError
from .enums import Target

"""
Contains base free functions used by specific getter/setter commands.
"""

DEFAULT_RECEIVE_BUFFER_SIZE = 256


def get_command_base(
    socket: socket.socket,
    target: str,
    value_patterns: List[str],
    value_converters: List[Callable],
) -> List[Any]:
    """
    Base VRROOM command function used by specific getter commands.

    Raises InvalidTargetError if an invalid command target is specified.
    """
    if not Target.is_valid(target):
        raise InvalidTargetError(
            f"Invalid target '{target}' was passed to get command!"
        )
    socket.sendall(Codec.encode_command_get(target))
    response = socket.recv(DEFAULT_RECEIVE_BUFFER_SIZE)
    return Codec.decode_response(response, target, value_patterns, value_converters)


def set_command_base(
    socket: socket.socket,
    target: str,
    desired_values: List[Any],
    value_patterns: List[str],
    value_converters: List[Callable],
) -> None:
    """
    Base VRROOM command function used by specific setter commands.

    Raises InvalidTargetError if an invalid command target is specified.
    Raises ValueNotChangedError if the returned values are different than the desired values.
    """
    if not Target.is_valid(target):
        raise InvalidTargetError(
            f"Invalid target '{target}' was passed to set command!"
        )

    socket.sendall(Codec.encode_command_set(target, desired_values))
    response = socket.recv(DEFAULT_RECEIVE_BUFFER_SIZE)

    returned_values = Codec.decode_response(
        response, target, value_patterns, value_converters
    )
    for returned, desired in zip(returned_values, desired_values):
        if returned != desired:
            returned_type = type(returned).__name__
            raise ValueNotChangedError(
                f"Returned {returned_type} '{returned}' was different than desired ({desired})!"
            )

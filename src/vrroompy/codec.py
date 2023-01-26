#!/usr/bin/env python3

"""
Contains class to encode/decode VRROOM commands for socket recv/send.
"""

import re
from typing import Any, ByteString, Callable, List

from .exceptions import ResponseParsingError


class Codec:
    """
    Encodes/decodes VRROOM commands for socket recv/send.
    """

    __COMMAND_TERMINATOR = "\n"

    @staticmethod
    def decode_response(
        response: ByteString,
        target: str,
        value_patterns: List[str],
        value_converters: List[Callable],
    ) -> List[Any]:
        """
        Decodes a response from the VRROOM switch.

        Returns None if there are no value patterns and converters passed.
        Returns a list of values equal to the number of patterns and converters otherwise.

        Raises ResponseParsingError if the response is unable to be parsed.
        Raises ValueError if the value pattern and converter lists are not the same length.
        """
        if len(value_patterns) != len(value_converters):
            raise ValueError(
                f"Unequal value pattern and converter arrays were passed to decoding!"
            )
        # Now that we know the value lengths are equal, we only have to check one list
        response_has_values = bool(value_patterns)  # Returns false if null or empty

        response_raw = Codec.decode_response_raw(response)
        response_pattern = f"{target}"
        if response_has_values:
            values_pattern = " ".join(value_patterns)
            response_pattern += f" (?P<values>{values_pattern})"
        response_match = re.match(response_pattern, response_raw)
        if response_match is None:
            raise ResponseParsingError(
                f"Unable to parse response '{response}' from VRROOM command!"
            )

        if response_has_values:
            response_value_strs = response_match.groupdict()["values"].split(" ")
            converter_response_pairs = zip(value_converters, response_value_strs)
            return [converter(value) for converter, value in converter_response_pairs]
        else:
            return []

    @staticmethod
    def decode_response_raw(response: ByteString) -> str:
        """
        Decodes a raw bytestring response from the VRROOM switch.

        Returns a string with the terminators removed.
        """
        # Match responses ending in newline, regardless of carriage return beforehand
        return re.match("([^\r\n]*)\r?\n", response.decode()).group(1)

    @staticmethod
    def encode_command_get(target: str) -> ByteString:
        """
        Encodes a command to get a value for the given target.

        Returns the bytestring for the command.
        """
        raw_command = f"get {target}\n"

        return Codec.encode_command_raw(raw_command)

    @staticmethod
    def encode_command_raw(command: str) -> ByteString:
        """
        Encodes a raw string command for the VRROOM switch.

        Returns a byte string with the correct terminators.
        """
        if command[-1:] != Codec.__COMMAND_TERMINATOR:
            command += Codec.__COMMAND_TERMINATOR
        return command.encode()

    @staticmethod
    def encode_command_set(target: str, values: List[Any]) -> ByteString:
        """
        Encodes a command to set a target to the given value(s).

        Returns the bytestring for the command.
        """
        raw_command = f"set {target}"
        if values:
            values_str = " ".join([str(val) for val in values])
            raw_command += f" {values_str}"

        return Codec.encode_command_raw(raw_command)

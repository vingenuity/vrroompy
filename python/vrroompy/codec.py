#!/usr/bin/env python3

"""
Contains class to encode/decode VRROOM commands for socket recv/send.
"""

import re
from typing import Any, ByteString, Callable, List


class Codec:
    """
    Encodes/decodes VRROOM commands for socket recv/send.
    """
    __COMMAND_FMT_GET = "get {target}"
    __COMMAND_FMT_SET = "set {target} {values}"
    __COMMAND_TERMINATOR = '\n'
    __RESPONSE_PATTERN_FMT = "{target} (?P<values>{values})"

    @staticmethod
    def decode_response(response:ByteString,
                        target: str,
                        value_patterns: List[str],
                        value_converters: List[Callable]) -> List[Any]:
        """
        Decodes a raw bytestring respons from the VRROOM switch.

        Returns a string with the terminators removed.
        """
        response_raw = Codec.decode_response_raw(response)

        response_pattern = Codec.__RESPONSE_PATTERN_FMT.format(
            target=target,
            values=' '.join(value_patterns))
        response_match = re.match(response_pattern, response_raw)
        if response_match is None:
            raise ValueError("Unable to parse response '{}' from VRROOM command!".format(response))

        response_value_strs = response_match.groupdict()["values"].split(' ')
        converter_response_pairs = zip(value_converters, response_value_strs)
        return [converter(value) for converter, value in converter_response_pairs]

    @staticmethod
    def decode_response_raw(response:ByteString) -> str:
        """
        Decodes a raw bytestring response from the VRROOM switch.

        Returns a string with the terminators removed.
        """
        return response.decode()[:-2]

    @staticmethod
    def encode_command_get(target: str) -> ByteString:
        """
        Encodes a command to get a value for the given target.

        Returns the bytestring for the command.
        """
        raw_command = Codec.__COMMAND_FMT_GET.format(target=target)

        return Codec.encode_command_raw(raw_command)

    @staticmethod
    def encode_command_raw( command:str) -> ByteString:
        """
        Encodes a raw string command for the VRROOM switch.

        Returns a byte string with the correct terminators.
        """
        if(command[-1:] != Codec.__COMMAND_TERMINATOR):
            command += Codec.__COMMAND_TERMINATOR
        return command.encode()

    @staticmethod
    def encode_command_set(target: str, values: List[Any]) -> ByteString:
        """
        Encodes a command to set a target to the given value(s).

        Returns the bytestring for the command.
        """
        values_str = ' '.join([str(val) for val in values])
        raw_command = Codec.__COMMAND_FMT_SET.format(target=target, values=values_str)

        return Codec.encode_command_raw(raw_command)

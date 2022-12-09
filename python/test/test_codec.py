#!/usr/bin/env python3
# pylint: disable=missing-function-docstring

"""
Contains unit tests for the module vrroompy.codec.
"""

import unittest
from vrroompy.codec import Codec
from vrroompy.commands.input import Input


class TestCodec(unittest.TestCase):
    """
    Unit tests the class vrroompy.Codec.
    """

    def test_decode_response_output(self):
        # String type, single output
        decoded_response = Codec.decode_response(
            b"opmode 4\r\n", "opmode", ["[0-4]"], [str]
        )
        self.assertEqual(decoded_response, ["4"])

        # Custom type, multiple outputs
        decoded_response = Codec.decode_response(
            b"insel 0 4\r\n",
            "insel",
            [Input.pattern(), Input.pattern()],
            [Input.from_string, Input.from_string],
        )
        self.assertEqual(decoded_response, [Input.RX0, Input.FOLLOW])

    def test_decode_response_raises(self):
        # Asserts when value pattern does not match response
        with self.assertRaises(ValueError):
            Codec.decode_response(b"opmode 5\r\n", "opmode", ["[0-4]"], [str])

    def test_decode_raw(self):
        decoded_response = Codec.decode_response_raw(b"opmode 4\r\n")
        self.assertEqual(decoded_response, "opmode 4")

        decoded_response = Codec.decode_response_raw(b"insel 3 0\r\n")
        self.assertEqual(decoded_response, "insel 3 0")

    def test_encode_get(self):
        encoded_command = Codec.encode_command_get("opmode")
        self.assertEqual(encoded_command, b"get opmode\n")

    def test_encode_raw(self):
        # Caller provides terminator for us
        encoded_command = Codec.encode_command_raw("get opmode\n")
        self.assertEqual(encoded_command, b"get opmode\n")

        # Caller forgets to provide terminator
        encoded_command = Codec.encode_command_raw("set insel 2 4")
        self.assertEqual(encoded_command, b"set insel 2 4\n")

    def test_encode_set(self):
        # Single value, str type
        encoded_command = Codec.encode_command_set("opmode", ["2"])
        self.assertEqual(encoded_command, b"set opmode 2\n")

        # Multiple values, custom type
        encoded_command = Codec.encode_command_set("insel", [Input.RX0, Input.RX1])
        self.assertEqual(encoded_command, b"set insel 0 1\n")

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

    def test_decode_raw(self):
        decoded_response = Codec.decode_response_raw(b'opmode 4\r\n')
        self.assertTrue(decoded_response == "opmode 4")

        decoded_response = Codec.decode_response_raw(b'insel 3 0\r\n')
        self.assertTrue(decoded_response == "insel 3 0")

    def test_encode_raw(self):
        # Caller provides terminator for us
        encoded_command = Codec.encode_command_raw("get opmode\n")
        self.assertTrue(encoded_command == b'get opmode\n')

        # Caller forgets to provide terminator
        encoded_command = Codec.encode_command_raw("set insel 2 4")
        self.assertTrue(encoded_command == b'set insel 2 4\n')

    def test_encode_get(self):
        encoded_command = Codec.encode_command_get("opmode")
        self.assertTrue(encoded_command == b'get opmode\n')

    def test_encode_set(self):
        # Single value, str type
        encoded_command = Codec.encode_command_set("opmode", ["2"])
        self.assertTrue(encoded_command == b'set opmode 2\n')

        # Multiple values, custom type
        encoded_command = Codec.encode_command_set("insel", [Input.RX0, Input.RX1])
        self.assertTrue(encoded_command == b'set insel 0 1\n')

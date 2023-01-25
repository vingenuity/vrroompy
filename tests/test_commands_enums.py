#!/usr/bin/env python3

"""
Contains unit tests for enums within vrroompy.commands.enums.
"""

from re import fullmatch
import unittest
from vrroompy.commands.enums import *


class TestOnOffSwitch(unittest.TestCase):
    """
    Unit tests the OnOffSwitch enumeration.
    """

    def test_str(self):
        self.assertEqual(str(OnOffSwitch.OFF), "off")
        self.assertEqual(str(OnOffSwitch.ON), "on")

    def test_from_bool(self):
        self.assertEqual(OnOffSwitch.from_bool(False), OnOffSwitch.OFF)
        self.assertEqual(OnOffSwitch.from_bool(True), OnOffSwitch.ON)

    def test_from_string(self):
        self.assertEqual(OnOffSwitch.from_string("off"), OnOffSwitch.OFF)
        self.assertEqual(OnOffSwitch.from_string("on"), OnOffSwitch.ON)

    def test_pattern(self):
        self.assertIsNotNone(fullmatch(OnOffSwitch.pattern(), str(OnOffSwitch.OFF)))
        self.assertIsNotNone(fullmatch(OnOffSwitch.pattern(), str(OnOffSwitch.ON)))
        self.assertIsNone(fullmatch(OnOffSwitch.pattern(), "OFF"))
        self.assertIsNone(fullmatch(OnOffSwitch.pattern(), "ON"))

    def test_to_bool(self):
        self.assertEqual(OnOffSwitch.to_bool(OnOffSwitch.OFF), False)
        self.assertEqual(OnOffSwitch.to_bool(OnOffSwitch.ON), True)


class TestTarget(unittest.TestCase):
    """
    Unit tests the Target enumeration.
    """

    def test_str(self):
        self.assertEqual(str(Target.SELECTED_INPUT_TX0), "inseltx0")
        self.assertEqual(str(Target.CEC), "cec")

    def test_from_string(self):
        self.assertEqual(Target.from_string("opmode"), Target.OPERATION_MODE)
        self.assertEqual(Target.from_string("reboot"), Target.ACTION_REBOOT)

    def test_is_valid(self):
        self.assertEqual(Target.is_valid("ipaddr"), True)
        self.assertEqual(Target.is_valid("edidmode"), True)
        self.assertEqual(Target.is_valid("invalid"), False)

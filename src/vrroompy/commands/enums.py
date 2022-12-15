#!/usr/bin/env python3

"""
Contains enumeration classes that are used across multiple commands.
"""

from enum import Enum


class OnOffSwitch(Enum):
    """
    Enumerates the values for a VRROOM on/off switch.
    """

    OFF = "off"
    ON = "on"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    def from_string(string: str) -> "OnOffSwitch":
        """
        Converts a string into a value of this enumeration, if possible.
        """
        return OnOffSwitch(string)

    @staticmethod
    def pattern() -> str:
        """
        Returns a regex pattern that matches values of this enumeration.
        """
        return f"(?:{OnOffSwitch.OFF}|{OnOffSwitch.ON})"

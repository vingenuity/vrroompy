#!/usr/bin/env python3

"""
Contains custom exception classes raised by the VRROOM package.
"""


class VrroomError(Exception):
    """Raised when a non-specific Vrroom exception occurs."""


class InvalidTargetError(VrroomError):
    """Raised when a command is called with an invalid target."""


class ResponseParsingError(VrroomError):
    """Raised when this module is unable to parse a received response."""


class ValueNotChangedError(VrroomError):
    """Raised when a set command fails to set the desired value."""

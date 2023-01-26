#!/usr/bin/env python3

"""
Allows VRROOM actions to be executed from the command line.
"""

import argparse
import logging
import socket
import sys
from typing import List
from vrroompy.commands.actions import factory_reset, hotplug, reboot, ResetDataType
from vrroompy.exceptions import VrroomError


ACTION_MAP = {
    "hotplug": lambda socket: hotplug(socket),
    "reboot": lambda socket: reboot(socket),
    "reset all": lambda socket: factory_reset(socket, ResetDataType.RESET_ALL),
    "reset edid": lambda socket: factory_reset(socket, ResetDataType.RESET_EDID_TABLES),
    "reset settings": lambda socket: factory_reset(
        socket, ResetDataType.RESET_SETTINGS
    ),
}


def main(address: str, port: int) -> int:
    """
    Contains the main functionality of this script.
    """
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger()

    logger.info("Connecting to VRROOM switch at '%s:%d'...", address, port)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as vrroom_socket:
        vrroom_socket.settimeout(5)
        vrroom_socket.connect((address, port))
        logger.info("Successfully connected to VRROOM switch.")

        logger.info("The following actions are supported:")
        for action_name, _ in ACTION_MAP.items():
            logger.info(f"\t{action_name}")

        requested_action = input("Enter action to execute: ")
        if requested_action not in ACTION_MAP.keys():
            raise ValueError(f"Invalid action '{requested_action}' was requested!")

        logger.info(f"Executing action '{requested_action}'...")
        action_func = ACTION_MAP[requested_action]
        try:
            action_func(vrroom_socket)
            logger.info("VRROOM action executed successfully.")
            return 0
        except VrroomError as err:
            logger.error(f"An error has occurred! {err}")
            return 1


def parse_arguments(arguments: List[str]) -> argparse.Namespace:
    """
    Parses command-line arguments into namespace data.
    """
    parser = argparse.ArgumentParser(
        description="Displays and allows changing of VRROOM inputs."
    )
    parser.add_argument(
        "--address",
        "-a",
        dest="address",
        required=True,
        type=str,
        help="IP or web address of the switch to connect.",
    )
    parser.add_argument(
        "--port",
        "-p",
        dest="port",
        required=True,
        type=int,
        help="Port number of the switch to connect.",
    )

    return parser.parse_args(arguments)


if __name__ == "__main__":
    exit(main(**vars(parse_arguments(sys.argv[1:]))))

#!/usr/bin/env python3

"""
Controls an HDFury VRROOM HDMI switch via serial socket.

Only raw string commands are supported.
"""

import argparse
import logging
import socket
import sys
from typing import List
from vrroompy.codec import Codec


QUIT_COMMAND = "quit"


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
        logger.info("Enter the command '%s' to quit.", QUIT_COMMAND)

        command = input("Enter command: ")
        while command != QUIT_COMMAND:
            logger.debug("Sending command '%s'...", command)
            vrroom_socket.sendall(Codec.encode_command_raw(command))
            response = vrroom_socket.recv(256)
            logger.info("Response: '%s'", Codec.decode_response_raw(response))

            command = input("Enter command: ")

    return 0


def parse_arguments(arguments: List[str]) -> argparse.Namespace:
    """
    Parses command-line arguments into namespace data.
    """
    parser = argparse.ArgumentParser(
        description="Controls an HDFury VRROOM HDMI switch via serial socket."
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

#!/usr/bin/env python3

"""
Controls an HDFury VRROOM HDMI switch via serial socket.
"""

import argparse
import logging
import socket
import sys
from typing import List


def main(address: str, port:int) -> int:
    """
    Contains the main functionality of this script.
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()

    test_command = b"get opmode\n"
    logger.info("Sending '%s' to VRROOM switch at '%s:%d'...", test_command, address, port)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as rs232_socket:
        rs232_socket.connect((address, port))
        rs232_socket.send(test_command)
        response = rs232_socket.recv(1024)

    logger.info("Received response '%s'", response)

    return 0


def parse_arguments(arguments: List[str]) -> argparse.Namespace:
    """
    Parses command-line arguments into namespace data.
    """
    parser = argparse.ArgumentParser(
        description="Controls an HDFury VRROOM HDMI switch via serial socket."
    )
    parser.add_argument('--address',
                        '-a',
                        dest='address',
                        required=True,
                        type=str,
                        help='IP or web address of the switch to connect.')
    parser.add_argument('--port',
                        '-p',
                        dest='port',
                        required=True,
                        type=int,
                        help='Port number of the switch to connect.')

    return parser.parse_args(arguments)


if __name__ == "__main__":
    exit(main(**vars(parse_arguments(sys.argv[1:]))))

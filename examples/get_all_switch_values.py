#!/usr/bin/env python3

"""
Displays all current values obtainable from the VRROOM switch.
"""

import argparse
import logging
import socket
import sys
from typing import List
from vrroompy.commands.enums import OnOffSwitch
from vrroompy.commands.input import get_selected_inputs
from vrroompy.commands.network import (
    get_ip_address,
    get_ip_network_mask,
    get_ip_gateway,
    get_dhcp_enabled,
    get_ip_interrupts_enabled,
    get_tcp_port,
)
from vrroompy.commands.modes import get_operation_mode, get_autoswitch_enabled


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

        logger.info("Getting all values from VRROOM switch...")
        logger.info("Operation mode: %s", get_operation_mode(vrroom_socket))

        selected_inputs = get_selected_inputs(vrroom_socket)
        logger.info("Selected inputs:")
        logger.info("\tTX0: %s", selected_inputs[0].name)
        logger.info("\tTX1: %s", selected_inputs[1].name)

        logger.info("IP Address: %s", get_ip_address(vrroom_socket))
        logger.info("Network Mask: %s", get_ip_network_mask(vrroom_socket))
        logger.info("Default Gateway: %s", get_ip_gateway(vrroom_socket))
        logger.info("DHCP: %s", OnOffSwitch.from_bool(get_dhcp_enabled(vrroom_socket)))
        logger.info(
            "IP Interrupts: %s",
            OnOffSwitch.from_bool(get_ip_interrupts_enabled(vrroom_socket)),
        )
        logger.info("TCP Port: %s", get_tcp_port(vrroom_socket))
        logger.info(
            "Autoswitch mode: %s",
            OnOffSwitch.from_bool(get_autoswitch_enabled(vrroom_socket)),
        )

        logger.info("All VRROOM values obtained successfully.")

    return 0


def parse_arguments(arguments: List[str]) -> argparse.Namespace:
    """
    Parses command-line arguments into namespace data.
    """
    parser = argparse.ArgumentParser(
        description="Displays all current values obtainable from the VRROOM switch."
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

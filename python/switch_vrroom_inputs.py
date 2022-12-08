#!/usr/bin/env python3

"""
Displays and allows changing of VRROOM inputs.
"""

import argparse
import logging
import socket
import sys
from typing import List
from vrroompy.commands.input import *



def main(address: str, port:int) -> int:
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

        selected_inputs = get_selected_inputs(vrroom_socket)
        logger.info("Currently selected inputs:")
        logger.info("\tTX0: %s", selected_inputs[0].name)
        logger.info("\tTX1: %s", selected_inputs[1].name)

        target_output = int(input("Select output to change (0-2, 2 means both): "))
        if (target_output < 0) or (target_output > 2):
            raise ValueError("Invalid output '{0}' was requested!".format(target_output))

        target_input_int = int(input("Select input to switch to (0-3): "))
        if (target_input_int < Input.RX0.value) or (target_input_int > Input.RX3.value):
            raise ValueError("Invalid input '{0}' was requested!".format(target_input_int))
        target_input = Input(target_input_int)

        target_func = None
        target_input_values = []
        log_text = ""
        if target_output == 2:
            target_func = set_selected_inputs
            target_input_values = [target_input, Input.FOLLOW]
            log_text = "Setting both outputs to input '{0}'...".format(target_input.name)
        else:
            output_name = ""
            if target_output == 0:
                output_name = "TX0"
                target_func = set_selected_input_tx0
            else:
                output_name = "TX1"
                target_func = set_selected_input_tx1
            target_input_values = [target_input]
            log_text = "Setting output '{0}' to input '{1}'...".format(output_name, target_input.name)

        logger.info(log_text)
        target_func(vrroom_socket, *target_input_values)
        logger.info("VRROOM inputs set successfully.")

    return 0


def parse_arguments(arguments: List[str]) -> argparse.Namespace:
    """
    Parses command-line arguments into namespace data.
    """
    parser = argparse.ArgumentParser(
        description="Displays and allows changing of VRROOM inputs."
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

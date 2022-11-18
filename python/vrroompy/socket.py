#!/usr/bin/env python3

"""
Contains class to manage VRROOM socket connections.
"""

import socket


class Socket:
    COMMAND_TERMINATOR = '\n'
    RECEIVE_BUFFER_SIZE = 256

    def __init__(self, address:str, port:int) -> None:
        self.__address = address
        self.__port = port
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __enter__(self):
        self.connect(self.__address, self.__port)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if not self.closed():
            self.close()
        return False

    def closed(self) -> bool:
        """
        Returns whether the socket is closed.

        Closure is determined by checking for file descriptor validity.
        """
        return (self.__socket.fileno == -1)

    def close(self) -> bool:
        """
        Closes the socket connection with the VRROOM switch.
        """
        self.__socket.close()

    def connect(self, address:str, port:int) -> None:
        """
        Connects to the given VRROOM address and port.
        """
        self.__socket.connect((address, port))

    def send_command(self, command:str) -> str:
        """
        Sends a raw string command to the VRROOM switch.

        Returns the raw string output from the command.
        """
        if(command[-1:] != self.COMMAND_TERMINATOR):
            command += self.COMMAND_TERMINATOR
        self.__socket.send(command.encode())

        response = self.__socket.recv(self.RECEIVE_BUFFER_SIZE)
        return response.decode()[:-2]

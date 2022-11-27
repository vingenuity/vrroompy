#!/usr/bin/env python3

"""
Contains class to manage VRROOM socket connections.
"""

import socket


class Socket:
    """
    Manages VRROOM socket connections.
    """
    __COMMAND_TERMINATOR = '\n'
    __RECEIVE_BUFFER_SIZE = 256

    def __init__(self, address:str, port:int) -> None:
        self.__address = address
        self.__port = port
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __enter__(self) -> "Socket":
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> bool:
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
        if not self.closed():
            self.__socket.close()

    def connect(self) -> None:
        """
        Connects to the VRROOM address and port given during initialization.
        """
        if self.closed():
            self.__socket.connect((self.__address, self.__port))

    def send_raw_command(self, command:str) -> str:
        """
        Sends a raw string command to the VRROOM switch.

        Returns the raw string output from the command.
        """
        if(command[-1:] != self.__COMMAND_TERMINATOR):
            command += self.__COMMAND_TERMINATOR
        self.__socket.send(command.encode())

        response = self.__socket.recv(self.__RECEIVE_BUFFER_SIZE)
        return response.decode()[:-2]

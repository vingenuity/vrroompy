# VRROOMpy

## Overview
VRROOMpy is a pure Python package for controlling HDFury VRROOM HDMI switches.

Only a subset of the full VRROOM API is currently available, but development on the remaining commands is ongoing.

The eventual intent is for this package to be used in a Home Assistant integration, which is hopefully coming soon.


## Usage
VRROOMpy provides two different APIs: "Raw" and "Command".

Regardless of the API, Python's `socket` package and class are used to establish the network connection. The APIs then call upon that socket to control the switch.

### Raw API
Calling the API directly via strings is exposed via the `Codec` class. The command names themselves can be found in the accompanying documentation file from HDFury.

For example, the following code snippet gets the current value, then overwrites the input TX0:
```
import socket
from vrroompy.codec import Codec

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as vrroom_socket:
    vrroom_socket.connect((address, port))

    vrroom_socket.sendall(Codec.encode_command_raw("get inseltx0"))
    print(vrroom_socket.recv(256))  # Prints "inseltx0 1"

    vrroom_socket.sendall(Codec.encode_command_raw("set inseltx0 2"))
    print(vrroom_socket.recv(256))  # Prints "inseltx0 2"
```

### Command API
The command API provides a higher-level, more Pythonic interface to the VRROOM switch. Commands are distributed by function within the `commands` sub-package.

For example, the following code snippet performs the same get/set of the TXO input:
```
import socket
from vrroompy.commands.input import Input, get_selected_input_tx0, set_selected_input_tx0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as vrroom_socket:
    vrroom_socket.connect((address, port))

    print(get_selected_input_tx0(vrroom_socket))  # Prints "1" (Input.RX1)
    set_selected_input_tx0(vrroom_socket, Input.RX2)
    print(get_selected_input_tx0(vrroom_socket))  # Prints "2" (Input.RX2)
```

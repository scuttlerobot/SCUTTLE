# This file receives data from a server program and can be used to receive telemetry. 
# The client runs on a local pc.

import math
import json
import time
import socket

class network:              # Holds IP and port as global variables

    ip = "192.168.50.1"     # SCUTTLE IP
    port = 2442             # SCUTTLE server port

try:

    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # Setup UDP Communication
    socket.settimeout(0.2)                                      # If response from server takes longer than
                                                                # time in seconds, move on.
except socket.error:

    print("Oops, something went wrong connecting the server!")  # If cannot connect, stop program.
    exit()

def get(items):

    try:

        message = json.dumps(items).encode('utf-8')         # Take requested data and convert to bytes
        socket.sendto(message, (network.ip,network.port))   # Send data to server
        data, ip = socket.recvfrom(4000)                    # Wait for response, create 4000 byte buffer to store response.
        data = json.loads(data)                             # Take response and convert from bytes to string
        data = dict(zip(items, data))                       # Combine request list with respose list to create dictionary
        return data                                         # Return data

    except Exception as e:

        print(e)
        return 1

print("SCUTTLE IP:", network.ip)

items = ['a','b','c']   # Construct request of data you want from server

while 1:    # Infinite loop

    data = get(items)   # Call function to request data from server

    if data != 1:       # If data is not equal to 1 (error code from get() function)
        print(data)     # print whole dictionary
    else:
        pass            # Else, ignore unsuccessful request fro data.

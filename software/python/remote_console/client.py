import math
import socket
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class network:

    ip = "192.168.1.1"
    port = 9999

try:

    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket.settimeout(0.001)

except socket.error:

    print("Oops, something went wrong connecting the server!")
    exit()

def get(items)

    try:

        message = items.encode()
        socket.sendto(message, (network.ip, network.port))
        data, ip = socket.recvfrom(4000)
        data = data.split()

    except:

        return 1

        pass

    return data

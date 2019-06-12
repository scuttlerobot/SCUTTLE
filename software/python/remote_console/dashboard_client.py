import math
import socket
import json
import time

class network:

    ip = "192.168.50.1"
    port = 9999

try:

    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket.settimeout(0.1)

except socket.error:

    print("Oops, something went wrong connecting the server!")

    exit()

def get(items):

    try:

        message = json.dumps(items).encode('utf-8')
        socket.sendto(message, (network.ip,
        network.port))
        data, ip = socket.recvfrom(4000)
        data = json.loads(data)

    except:

        return 1

        pass

    return data

items = ["a","b","c"]

while 1:

    data = get(items)

    print(data)

    time.sleep(0.05)

import math
import socket
import json

class network:

    ip = "localhost"
    port = 9999

try:

    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket.settimeout(0.001)

except socket.error:

    print("Oops, something went wrong connecting the server!")
    exit()

def get(items):

    try:

        message = json.dumps(items).encode()
        socket.sendto(message, (network.ip, network.port))
        data, ip = socket.recvfrom(4000)
        data = json.loads(data)

    except:

        return 1

        pass

    return data

items = ["a","b","c"]
items = get(items)
print(items)

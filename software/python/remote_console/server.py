import socket
import time
import json

port = 9999

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# socket.bind(("", port))
socket.bind(("localhost", port))

print("Server running!")

# while 1:

data = {
  "a": 1,
  "b": 2,
  "c": 3
}

try:

    request, ip = socket.recvfrom(1024)
    request = json.loads(request)

    print("got data: ",request)

    packet = []

    for item in request:

        if item in data:

            packet.append(data[item])

        elif item not in data:

            packet.append(None)

    print(packet)

    packet = json.dumps(packet)

    socket.sendto(packet.encode(), ip)

except:

    socket.sendto(packet.encode(), ip)
    pass

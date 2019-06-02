import socket
import time
import json
import kinematics as k

port = 9999

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# socket = sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# socket.bind(("", port))
socket.bind(("localhost", port))

print("Server running!")

while 1:

    theta = k.getMotion()

    data = {"thetaDot": theta[0],
            "xDot": theta[1]
            }

    try:

        request, ip = socket.recvfrom(1024)
        request = json.loads(request)

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

        pass

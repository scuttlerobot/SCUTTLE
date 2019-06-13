import socket
import time
import json
import sys

ip = "0.0.0.0"
port = 2442

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.bind((ip, port))

print("Bound to IP:  ",ip,"\n\t Port:",port)
print("\nServer running!")

i = 0

while 1:

    data = {
      "a": 1,
      "b": 2,
      "c": 3
    }


    try:

        request, ip = socket.recvfrom(1024)
        print(i," - Received Request from", ip[0])
        request = json.loads(request.decode('utf-8'))
        packet = []

        for item in request:

            if item in data:

                packet.append(data[item])

            elif item not in data:

                packet.append(None)

        packet = json.dumps(packet)
        socket.sendto(packet.encode(), ip)

    except Exception as e:

        if e == "KeyboardInterrupt":

            print("Exiting!")
            exit()

        else:

            print(e)

    i+=1

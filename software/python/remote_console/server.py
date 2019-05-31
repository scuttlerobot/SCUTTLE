import socket
import pysicktim as lidar

port = 9999

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.bind(("", port))

while 1:
    try:
        request, ip = socket.recvfrom(1024)

        for item in request:
            print(item)

       socket.sendto(packet.encode(), ip)
    except:
        socket.sendto(packet.encode(), ip)
        pass

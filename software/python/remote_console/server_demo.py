# This file is just a basic example of the server comunication structure to a client program.
# The server is run on the embedded computer and passes data to a client on your local pc
# over a direct wifi connection. This can be used to display telemetry. 

import time
import json
import socket

def current_time(start_time):
    current_time = time.time() - start_time
    day = current_time // (24 * 3600)
    current_time = current_time % (24 * 3600)
    hour = current_time // 3600
    current_time %= 3600
    minutes = current_time // 60
    current_time %= 60
    seconds = round(current_time,3)
    return hour, minutes, seconds

def log(*args):
    t = current_time(start_time)
    print("%02d:%02d:%02.3f -" % (t[0],t[1],t[2]),' '.join(map(str, args)))

ip = "0.0.0.0"      # 0.0.0.0 will make the server accessable on all network interfaces
port = 2442         # Port to run server on

start_time = time.time()    # Record start time for logging

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # Setup UDP Communication
socket.bind((ip, port))

print("Bound to IP:  ",ip,"\n\t Port:",port)
print("\nServer running!")

while 1:

    data = {
      "a": 1,
      "b": 2,
      "c": 3
    }

######################################

    # UPDATE DATA HERE

    # Example:
    # data["batt_v"] = analog_read(battery)

######################################

    try:

        request, ip = socket.recvfrom(1024)                     # Wait until data is received
        request = json.loads(request.decode('utf-8'))           # Converts data back from bytes to string
        log("Received Request from", ip[0], "for:", request)    # Log to console
        packet = []                                             # Create empty list to construct packet

        for item in request:                # Iterate through requested items and
                                            # assemble packet in order requested
            if item in data:                # Check requested item exists in data dictionary

                packet.append(data[item])   # If items exists append to end of packet

            elif item not in data:                              # If item doesnt exist in data dictionary
                log("Item \"",item,"\"", "does not exist!")     # Log to console
                packet.append(None)                             # append 'None' for better error handling

        packet = json.dumps(packet)                     # Convert message to bytes
        socket.sendto(packet.encode('utf-8'), ip)       # Send back to device that requested
        log("Sent response", packet,"to",ip[0])         # Log to console

    except Exception as e:      # If there is an error
        print(e)                # Print error
        exit()                  # Exit code. Replace with "pass" for code to move on after error

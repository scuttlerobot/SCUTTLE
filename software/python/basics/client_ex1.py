# This file is a customized client which operates on the PC and receives wheelspeed
# data from the robot.  A server must be configured and running on the robot to 
# send this data over direct wifi connection.  MatPlot Lib functions are included to
# generate a continuoulsy updating bar chart on the user's PC.

import math
import json 
import time  
import socket
import matplotlib.pyplot as plt # Import matplotlib as plt for shorter name
import matplotlib
import matplotlib.animation as animation

class network:              # Holds IP and port as global variables
    #ip = "localhost"
    #ip = "scuttle.ddns.net"
    ip = "192.168.8.1"     # SCUTTLE IP
    #port = 2442             # SCUTTLE server port
    port = 2222
    #port = 135

try:
    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # Setup UDP Communication
    socket.settimeout(0.2) #previously 0.2                                     # If response from server takes longer than
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

def animate(i):
    try:
        data = get(items)   # Call function to request data from server
        if data != 1:       # If data is not equal to 1 (error code from get() function)
            x = ["Left Wheel","Right Wheel"]
            # y = [6,80]
            phi_dots = [data["phi_dots_L"], data["phi_dots_R"]]
            phi_plot.clear()
            phi_plot.set_ylim(-30, 30)
            # phi_plot.xlabel('Left and Right Wheels')
            # phi_plot.ylabel('Phi Dots')
            # phi_plot.legend()
            # phi_plot.xticks(x, ('Left', 'Right'))
            phi_plot.axhline(0, color='black', lw=1)
            phi_plot.bar(x, phi_dots, label='Phi Dots', color='r')
        else:
            pass
    except:
        pass

items = ["phi_dots_L","phi_dots_R"]
fig = plt.figure()
fig.canvas.set_window_title('Scuttle Wheel Speeds Distribution')
phi_plot = plt.subplot()
ani = animation.FuncAnimation(fig, animate)
plt.show()

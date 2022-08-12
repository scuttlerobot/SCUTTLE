#!/usr/bin/python3

# L3 program for driving the SCUTTLE with a Node-RED flow's joystick inputs
# Requires the Node-RED joystick control flow to be imported
# Communicates with Node-RED using sockets and handles that process using threads,
# which improves the motor control latency

import socket
import json
from time import sleep
from threading import Thread
import numpy as np
import L1_ina as ina
import L2_inverse_kinematics as ik
import L2_speed_control as sc


#UPD communication#
IP = "127.0.0.1"                                                        
listen_port = 3553
publish_port = 3554

dashBoardDatasock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dashBoardDatasock.bind((IP, listen_port))
dashBoardDatasock.settimeout(.25)

#Robot data#
dashBoardData = None
batteryPackVoltage = 0.


## Thread functions ##                    
def _dashBoardDataUpdater():                                            #thread function to listen for latest dashboard inputs
    global dashBoardData 
    while True:
        try:
            dashBoardData,recvAddr = dashBoardDatasock.recvfrom(1024)   #wait and listen for a message from nodered
            dashBoardData = json.loads(dashBoardData)                   #load the json string message to a python dictionary
        except socket.timeout:                                          #timeout occurs if the listener waits too long
            dashBoardData = None

        voltage_message = str(ina.readVolts()).encode('utf-8')            #convert voltage to string and encode for publishing
        dashBoardDatasock.sendto(voltage_message, (IP, publish_port))   #send the voltage message to nodered

def _controlLoopUpdater():                                              #thread function to set motors from the latest joystick data
    while True:
        if dashBoardData != None:                                       #only update if there's some nodered input
            try:
                joystickDict = dashBoardData['one_joystick']            #get data stored under the key 'one_joystick' from dictionary
                joystickTarget = np.array((joystickDict['y'], -joystickDict['x']))  #extract joystick x and y from dictionary to an array

                robotSpeedTarget = ik.map_speeds(joystickTarget)        #calculate robot speed target (xdot, thetadot) from joystick position 
                wheelSpeedTarget = ik.getPdTargets(robotSpeedTarget)    #calculate wheel speed target (pdl, pdr) from (xdot, thetadot)
                
                sc.driveOpenLoop(wheelSpeedTarget)                      #send wheel speeds to speed control for driving
            except Exception as ex:
                print(repr(ex))                                         #if something goes wrong, print the error but keep looping
                sleep(.5)


## Configure threads ##
dashBoardDataUpdateThread = Thread(target=_dashBoardDataUpdater)    #communicates with nodered to get joystick and send battery data
controlThread = Thread(target=_controlLoopUpdater)                  #updates motor speeds from joystick position

dashBoardDataUpdateThread.daemon = True                             #daemon threads will close automatically once the main thread closes
controlThread.daemon = True

## Runs only when L3_noderedControl.py is directly executed ##
if __name__ == "__main__":                                          #must be main thread
    dashBoardDataUpdateThread.start()                               #start threads, from here their target functions will execute asynchronously
    controlThread.start()
    
    try:
        while True:                                                
            sleep(0.2)                      #while the main thread sleeps, the two daemon threads will run asynchronously in parallel
    except:                     
        sc.driveOpenLoop((0,0))             #stop the robot if interrupted


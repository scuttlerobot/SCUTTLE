#This example drives the robot with the DSTR mobile app. (andoid and ios)

# import python libraries

import time

import socket



# import rcpy library

# This automatically initizalizes the robotics cape

import rcpy

import rcpy.motor as motor

#import rcpy.gpio as gpio

#import rcpy.led as led



UDP_IP = "192.168.1.1"

UDP_PORT = 3553 #port that the DSTR app listens to

bufferSize = 512

#  ALWAYS check these they could be flipped 



Motor_X = 1 	#Right Motor

Motor_Y = 2 	#Left Motor



dutyX = 0

dutyY = 0



# set state to rcpy.RUNNING

rcpy.set_state(rcpy.RUNNING)



try:

    # Create a UDP/IP socket

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:

        try:    

            sock.bind((UDP_IP, UDP_PORT))

#            led.red.off()

#            led.green.on()

            break

        except:

            pass

    sock.settimeout(.25)

    # keep running forever

    while True:

        #print ("dutyX", dutyX)

        #print ("dutyY", dutyY)

        # running?

        if rcpy.get_state() == rcpy.RUNNING:

            try:    

                data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes

                #print("data", data[2])

            except socket.timeout:

                dutyX = 0

                dutyY = 0

                data = 0

                motor.set_brake(Motor_X)

                motor.set_brake(Motor_Y)

                continue

            if int(data[0]) == 187:

                #print("data 1", data[3])

                dutyX = 1*(int(data[3])-255)/255

                #print("dutyX", dutyX)

            elif int(data[0]) == 170:

                #print("data 1", data[1])

                dutyX = -1*(int(data[3])-255)/255

                #print("dutyX", dutyX)

            if int(data[2]) == 187:

                #print("data 3", data[1])

                dutyY = -1*(int(data[1])-255)/255

                #print("dutyY", data[1])

            elif int(data[2]) == 170:

                #print("data 3", data[1])

                dutyY = 1*(int(data[1])-255)/255

                #print("dutyY", data[1])

            motor.set(Motor_X, dutyX)

            motor.set(Motor_Y, dutyY)

            pass

    

        # paused?

        elif rcpy.get_state() == rcpy.PAUSED:

            # do nothing

            pass



except KeyboardInterrupt:

    # Catch Ctrl-C

    pass

        

finally:

    # say bye

    print("\nBye Beaglebone!")

            



# This program offers enhanced control of servos, speed and angles

# import external libraries
import time

# import internal programs
import L1_servo as servo

span = 180 # input here the span of the servo in use (degrees)
maxCmd = 1.5

def one(deg):
    cmd = deg * maxCmd /(span / 2 ) # rescale the value for servo commands
    print("moving to", deg)
    servo.move1(cmd)
    

# # UNCOMMENT THE LOOP TO RUN AS A STANDALONE PROGRAM
# while 1:
#     one(-45)
#     time.sleep(2)
#     one(0)
#     time.sleep(2)
#     one(45)
#     time.sleep(2)

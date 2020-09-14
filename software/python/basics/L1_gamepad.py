# an example to grab values from the wireless gamepads (EasySMX brand) and print them.
# gamepad must be plugged in and activated at start of program.
# see the scuttle software documentation for a map of buttons.
# 16 values will be returned, 4 floatig and 12 boolean
# last updated 2019.05.24

import pygame                                       # this library contains functions to communicate with a gamepad
import numpy as np                                  # for working with arrays
import os                                           # for making commands directly to the OS
import time                                         # only required if we run this program  in a loop

os.environ['SDL_VIDEODRIVER'] = 'dummy'
pygame.display.set_mode((1, 1))
pygame.init()


# function for reading the game pad
def getGP():

    for event in pygame.event.get():                # User did something
        pass

    gamepad_count = pygame.joystick.get_count()     # Get count of gamepads connected
    for i in range(gamepad_count):                  # For each gamepad:

        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        # Get Left X and Y Joystick Values
        axis_0 = round(joystick.get_axis(0), 3)    # left thumb, right is positive
        axis_1 = round(joystick.get_axis(1), 3)    # left thumb, down is positive
        axis_2 = round(joystick.get_axis(2), 3)    # right thumb, right is positive
        axis_3 = round(joystick.get_axis(3), 3)    # right thumb, down is positive

        # Get Controller Buttons
        buttons = joystick.get_numbuttons()

        # Get Button States
        B0 = joystick.get_button(0)                 # Y
        B1 = joystick.get_button(1)                 # B
        B2 = joystick.get_button(2)                 # A
        B3 = joystick.get_button(3)                 # X
        B4 = joystick.get_button(4)                 # LB
        B5 = joystick.get_button(5)                 # RB
        B6 = joystick.get_button(6)                 # LT
        B7 = joystick.get_button(7)                 # RT
        B8 = joystick.get_button(8)                 # back
        B9 = joystick.get_button(9)                 # start
        B10 = joystick.get_button(10)               # left thumb press
        B11 = joystick.get_button(11)               # right thumb press

        axes = np.array([axis_0, axis_1, axis_2, axis_3])                       # store all axes in an array
        buttons = np.array([B0, B1, B2, B3, B4, B5, B6, B7, B8, B9, B10, B11])  # store all buttons in array
        gp_data = np.hstack((axes, buttons))                                    # this array will have 16 elements
        return(gp_data)


if __name__ == "__main__":
    while True:
        # collect commands from the gamepad.  Run as many times as there are commands in the queue.
        myGpData = getGP()                          # store data from all axes to the myGpData variable
        print(myGpData)                             # print out the first element of the data to confirm functionality
        time.sleep(0.25)

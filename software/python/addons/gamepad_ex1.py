# an example to grab values from the wireless gamepads (EasySMX brand) and print them.
# gamepad must be plugged in at start of program.
# see the scuttle software documentation for a map of buttons.
# last updated 2019.05.17

import os
import time

# Create Dummy Display
# PyGame relies on having a display connected when the library is initialized
# This section of code uses a pygame function to fake a display outputself.
os.environ['SDL_VIDEODRIVER'] = 'dummy' #create dummy display
import pygame
pygame.init()
pygame.display.set_mode((1,1))
pygame.init()

#Loop until the user clicks the close button.
# Initialize the joysticks
pygame.joystick.init()

os.system("reset")  # Clear the terminal
print("Running!")

while 1:  #loop for 20 seconds
    # collect commands from the gamepad.  Run as many times as there are commands in the queue.
    for event in pygame.event.get():
        pass

    # Get count of gamepads connected
    gamepad_count = pygame.joystick.get_count()

    # For each gamepad:
    for i in range(gamepad_count):

        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        # Get Left X and Y Joystick Values
        axis_0 = round(joystick.get_axis( 0 ),3) #left thumb, right is positive
        axis_1 = round(joystick.get_axis( 1 ),3) # left thumb, down is positive
        axis_2 = round(joystick.get_axis( 2 ),3) # right thumb, right is positive
        axis_3 = round(joystick.get_axis( 3 ),3) # right thumb, down is positive

        # Get Controller Buttons
        buttons = joystick.get_numbuttons()

        # Get Button States
        B0 = joystick.get_button( 0 ) # Y
        B1 = joystick.get_button( 1 ) # B
        B2 = joystick.get_button( 2 ) # A
        B3 = joystick.get_button( 3 ) # X
        B4 = joystick.get_button( 4 ) # LB
        B5 = joystick.get_button( 5 ) # RB
        B6 = joystick.get_button( 6 ) # LT
        B7 = joystick.get_button( 7 ) # RT
        B8 = joystick.get_button( 8 ) # back
        B9 = joystick.get_button( 9 ) # start
        B10 = joystick.get_button( 10 ) # left thumb press
        B11 = joystick.get_button( 11 ) # right thumb press

        print(" X:", B3, " Y:", B0, " A:", B2, " B :", B1, "LB: ", B4, "RB: ", B5, "Axis0", axis_0, "Axis1", axis_1, "Axis 2", axis_2, "Axis3: ", axis_3)
        time.sleep(0.1)


<<<<<<< HEAD
# Gamepad Program for SCUTTLE running rasPi
=======
# Gamepad Program for SCUTTLE running RasPi
>>>>>>> a2c881dbe9f0f83a5d5508e0e3396db5ae1abd66
# This program grabs values from the wireless EasySMX gamepad & stores to arrays.
# Gamepad dongle must be plugged in and gamepad activated at start of program.
# See the scuttle software guide for a map of buttons.
# 16 values will be returned, 4 floats (axes) and 12 booleans (buttons)
# last updated 2020.11

# Import external programs
import pygame # for connecting to bluetooth controller
import numpy as np  # for matrix math
import os   # supports pygame

os.putenv('DISPLAY', ':0.0')    # create dummy display as required for lib initialization
pygame.display.init()           # Initialize the dummy display
pygame.joystick.init()          # Initialize the joysticks

def getGP():  #function for reading the game pad

    for event in pygame.event.get():            # User moved gamepad
        pass

    gamepad_count = pygame.joystick.get_count() # Get count of gamepads connected
    for i in range(gamepad_count):              # For each gamepad:

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
        #B11 = joystick.get_button( 11 ) # right thumb press (button 11 throws an error on raspi)

        # print(" X:", B3, " Y:", B0, " A:", B2, " B :", B1, "LB: ", B4, "RB: ", B5, "Axis0", axis_0, "Axis1", axis_1, "Axis 2", axis_2, "Axis3: ", axis_3)
        axes = np.array([axis_0, axis_1, axis_2, axis_3])                   # store all axes in an array
        buttons = np.array([B0, B1, B2, B3, B4, B5, B6, B7, B8, B9, B10])   # store all buttons in array
        gp_data = np.hstack((axes, buttons))                                # this array will have 16 elements
        return(gp_data)

# THIS LOOP RUNS ONLY IF PROGRAM IS CALLED DIRECTLY
if __name__ == "__main__":
    while 1:
        # collect commands from the gamepad.  Run as many times as there are commands in the queue.
        myGpData = getGP()                    # store data from all axes to the myGpData variable
        print("First axis:", myGpData[0])     # print out the first element
<<<<<<< HEAD
        time.sleep(0.1)                       # wait 0.1 sec
=======
>>>>>>> a2c881dbe9f0f83a5d5508e0e3396db5ae1abd66

# an example to grab values from the joysticks and print them.
# this file started with joystick_drive.py and is to be modified, as of 2019.05.16

import os
import time

# Create Dummy Display
# PyGame relies on having a display connected when the library is initialized
# This section of code uses a pygame function to fake a display outputself.

os.environ['SDL_VIDEODRIVER'] = 'dummy'
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

    for event in pygame.event.get(): # User did something
        pass

    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    # For each joystick:
    for i in range(joystick_count):

        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        # Get Left X and Y Joystick Values
        l_joy_x = joystick.get_axis( 0 )
        l_joy_y = joystick.get_axis( 1 )

        # Get Controller Buttons
        buttons = joystick.get_numbuttons()

        # Get Button States
        x_button = joystick.get_button( 3 )
        l_button = joystick.get_button( 6 )
        r_button = joystick.get_button( 7 )

        print(x_button)
        time.sleep(0.1)

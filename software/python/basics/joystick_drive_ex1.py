# This code allows you to drive SCUTTLE robot using a USB or Bluetooth joystick.

#!/usr/bin/env python
import Adafruit_BBIO.GPIO as GPIO
import os
import signal,sys

print("loading rcpy.")
# import rcpy library
# This automatically initizalizes the robotics cape
import rcpy
import rcpy.motor as motor
print("finished loading libraries.")

import time
import os

# Create Dummy Display
# PyGame relies on having a display connected when the library is initialized
# This section of code uses a pygame function to fake a display outputself.

os.environ['SDL_VIDEODRIVER'] = 'dummy'
import pygame
pygame.init()
pygame.display.set_mode((1,1))

pygame.init()

#Loop until the user clicks the close button.
#done = False    #PROBABLY NOT NEEDED, REMOVE LINE 115 TOO

# Initialize the joysticks
pygame.joystick.init()

duty_l = 0 # initialize motor with zero duty cycle
duty_r = 0 # initialize motor with zero duty cycle

motor_r = 2 	# Right Motor assigned to #2
motor_l = 1 	# Left Motor assigned to #1

print("initializing rcpy...")
rcpy.set_state(rcpy.RUNNING)
print("finished initializing rcpy.")

try:

    os.system("reset")  # Clear the terminal

    print("Running!")

    while rcpy.get_state() != rcpy.EXITING:

        if rcpy.get_state() == rcpy.RUNNING:

            for event in pygame.event.get(): # User did something
                # if event.type == pygame.QUIT: # If user clicked close
                #     done=True # Flag that we are done so we exit this loop  PROBABLY NOT NEEDED
                #               # MIGHT NEED PASS IF done=TRUE REMOVED
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

                # Calculate Left and Right Wheel Duty Cycles

                duty_r = ((-1*(l_joy_x))-l_joy_y)
                duty_l = (    (l_joy_x) -l_joy_y)

                # Set wheel duty cycles between -1 and 1 if calculated is outside range.

                if duty_l > 1:

                    duty_l = 1

                if duty_r > 1:

                    duty_r = 1

                if duty_l < -1:

                    duty_l = -1

                if duty_r < -1:

                    duty_r = -1

                #   Print for debugging

                # print("Duty L: ",round(duty_l,2),"\t\tDuty R: ",round( duty_r,2), "\t\tLB: ", l_button, "\t\tRB: ", r_button)

                # Set motor values

                motor.set(motor_l, round(duty_l,2))
                motor.set(motor_r, round(duty_r,2))

        elif rcpy.get_state() == rcpy.PAUSED:

                pass

except KeyboardInterrupt: # condition added to catch a "Ctrl-C" event and exit cleanly

    print("Exiting")

    rcpy.set_state(rcpy.EXITING)

    pass

finally:

    rcpy.set_state(rcpy.EXITING)

    print("Exiting")

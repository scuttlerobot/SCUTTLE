# THIS CODE NEEDS TO BE REDONE FROM SCRATCH


# This program offers functions for controlling servos on the blue
# servo position is specified by "duty."  If the servo is a continuous
# type, the duty will set the speed instead of the position. 
# Uses rcpy library.  Documentation: guitar.ucsd.edu/rcpy/rcpy.pdf
# PROGRAM REQUIRES SUDO.

import time, math
import getopt, sys
import rcpy  # This automatically initizalizes the robotics cape
import rcpy.servo as servo
import rcpy.clock as clock	# For PWM period for servos

# defaults
duty = 1.5	# Duty cycle (-1.5,1.5)
period = 0.02	# Set servo period to 20ms
ch1 = 1	# Which channel (1-8), 0 outputs to all channels
ch2 = 2
ch3 = 3

rcpy.set_state(rcpy.RUNNING) # set state to rcpy.RUNNING
srvo1 = servo.Servo(ch1)	# Create servo object
srvo2 = servo.Servo(ch2)
srvo3 = servo.Servo(ch3)
clck1 = clock.Clock(srvo1, period)	# Set PWM period for servos
clck2 = clock.Clock(srvo2, period)
clck3 = clock.Clock(srvo3, period)

#try:
servo.enable()		# Enables 6v rail
clck1.start()		# Starts PWM
clck2.start()
clck3.start()

def move1(angle):
	srvo1.set(angle)
	
def move2(angle):
	srvo2.set(angle)
	
def move3(angle):
	srvo3.set(angle)
	
# UNCOMMENT THE SECTION BELOW TO RUN AS STANDALONE PROGRAM
print("beginning servo loop")
while rcpy.get_state() != rcpy.EXITING: 	# keep running
		print("move 1.5")
		move1(1.5)	# Set servo duty
		move2(1.5)
		move3(1.5)
		time.sleep(2)
		print("move -0.5")
		move1(-1.5)
		move2(-1.5)
		move3(-1.5)
		time.sleep(2)

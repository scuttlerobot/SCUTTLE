# This program offers functions for controlling servos on the blue
# servo position is specified by "duty."  If the servo is a continuous
# type, the duty will set the speed instead of the position. 
# Uses rcpy library.  Documentation: guitar.ucsd.edu/rcpy/rcpy.pdf
# PROGRAM REQUIRES SUDO. Last udpated 2020.10.08

# Import external libraries
import time, math
import getopt, sys
import rcpy  # This automatically initizalizes the robotics cape
import rcpy.servo as servo
import rcpy.clock as clock	# For PWM period for servos

# INITIALIZE DEFAULT VARS
duty = 1.5		# Duty cycle (-1.5,1.5 is the typical range)
period = 0.02 	# recommended servo period: 20ms (this is the interval of commands)
ch1 = 1			# select channel (1 thru 8 are available)
ch2 = 2			# selection of 0 performs output on all channels

rcpy.set_state(rcpy.RUNNING) # set state to rcpy.RUNNING
srvo1 = servo.Servo(ch1)	# Create servo object
srvo2 = servo.Servo(ch2)
clck1 = clock.Clock(srvo1, period)	# Set PWM period for servos
clck2 = clock.Clock(srvo2, period)

servo.enable()		# Enables 6v rail on beaglebone blue
clck1.start()		# Starts PWM
clck2.start()

def move1(angle):
	srvo1.set(angle)
	
def move2(angle):
	srvo2.set(angle)

# THE SECTION BELOW WILL ONLY RUN IF L1_SERVO.PY IS CALLED DIRECTLY	 
if __name__ == "__main__":
	while True:
		print("beginning servo loop")
		while rcpy.get_state() != rcpy.EXITING: 	# keep running
				print("move 1.5")
				move1(1.5)	# Set servo duty (1.5 has no units, see library for details)
				time.sleep(2)
				print("move -1.5")
				move1(-1.5)
				time.sleep(2)

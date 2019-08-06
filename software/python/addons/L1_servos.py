# This example moves the servos to the position specified by "duty."   
# If the servo is a continuous type, the duty will set the speed instead of the position. 

# import python libraries
import time, math
import getopt, sys

# import rcpy library
# This automatically initizalizes the robotics cape
import rcpy 
import rcpy.servo as servo
import rcpy.clock as clock	# For PWM period for servos

# defaults
duty = 1.5	# Duty cycle (-1.5,1.5)
period = 0.02	# Set servo period to 20ms
channel = 0	# Which channel (1-8), 0 outputs to all channels

# set state to rcpy.RUNNING
rcpy.set_state(rcpy.RUNNING)

srvo = servo.Servo(channel)	# Create servo object


clck = clock.Clock(srvo, period)	# Set PWM period for servos

try:

	# enable servos
	servo.enable()		# Enables 6v rail

	# start clock
	clck.start()		# Starts PWM

	# keep running
	while rcpy.get_state() != rcpy.EXITING:

		srvo.set(duty)	# Set servo duty

except KeyboardInterrupt:
	
	pass

finally:

	# stop clock
	clck.stop()

	# disable servos
	servo.disable()

	# say bye
	print("\nBye Beaglebone!")


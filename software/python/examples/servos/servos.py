# import python libraries
import time, math
import getopt, sys

# import rcpy library
# This automatically initizalizes the robotics cape
import rcpy 
import rcpy.servo as servo
import rcpy.clock as clock

# defaults
duty = 1.5
period = 0.02
channel = 0

# set state to rcpy.RUNNING
rcpy.set_state(rcpy.RUNNING)

# Create servo
srvo = servo.Servo(channel)

clck = clock.Clock(srvo, period)

try:

	# enable servos
	servo.enable()

	# start clock
	clck.start()

	# keep running
	while rcpy.get_state() != rcpy.EXITING:

		srvo.set(duty)

except KeyboardInterrupt:
	
	pass

finally:

	# stop clock
	clck.stop()

	# disable servos
	servo.disable()

	# say bye
	print("\nBye Beaglebone!")


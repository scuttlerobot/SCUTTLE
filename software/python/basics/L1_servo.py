# This program offers functions for controlling servos on the blue
# servo position is specified by "duty."  If the servo is a continuous
# type, the duty will set the speed instead of the position. 
# PROGRAM REQUIRES SUDO.  IN PROGRESS AS OF 2019.08.09

import time, math
import getopt, sys
import rcpy  # This automatically initizalizes the robotics cape
import rcpy.servo as servo
import rcpy.clock as clock	# For PWM period for servos

# defaults
duty = 1.5	# Duty cycle (-1.5,1.5)
period = 0.02	# Set servo period to 20ms
channel = 1	# Which channel (1-8), 0 outputs to all channels
channel2 = 2

rcpy.set_state(rcpy.RUNNING) # set state to rcpy.RUNNING
srvo = servo.Servo(channel)	# Create servo object
srvo2 = servo.Servo(channel2)
clck = clock.Clock(srvo, period)	# Set PWM period for servos
clck2 = clock.Clock(srvo2, period)


#try:
servo.enable()		# Enables 6v rail
clck.start()		# Starts PWM
clck2.start()


def move(angle):
	srvo.set(angle)
	
def move2(angle):
	srvo2.set(angle)
	
# 	while rcpy.get_state() != rcpy.EXITING: 	# keep running

# 		srvo.set(duty)	# Set servo duty
# 		srvo2.set(duty)
# 		time.sleep(2)
		
# 		srvo.set(-duty)
# 		srvo2.set(-duty)
# 		time.sleep(2)
        
# except KeyboardInterrupt:
# 	pass
# finally:

# 	clck.stop() # stop clock
# 	servo.disable() # disable servos

# This example drives the right and left motors.
# Intended for Beagle hardware

import rcpy
import rcpy.motor as motor
import time # only necessary if running this program as a loop

motor_r = 2 	# Right Motor
motor_l = 1 	# Left Motor
rcpy.set_state(rcpy.RUNNING)

#channel refers to left(0) or right(1)
def MotorL(speed):
    motor.set(motor_l, duty_l)
    
def MotorR(speed):
    motor.set(motor_r, duty_r)

# Uncomment this section to run this program as a standalone loop
while rcpy.get_state() != rcpy.EXITING:

    if rcpy.get_state() == rcpy.RUNNING:

        MotorL(0.3)  # gentle speed for testing program
        MotorR(0.3)
        time.sleep(2) # run fwd for 2 seconds
        MotorL(-0.3)
        MotorR(-0.3) 
        time.sleep(2) # run reverse for 2 seconds

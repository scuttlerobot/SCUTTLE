# This example drives the right and left motors.
# Intended for Beaglebone Blue hardware.
# This example uses rcpy library. Documentation: guitar.ucsd.edu/rcpy/rcpy.pdf

# Import external libraries
import rcpy
import rcpy.motor as motor
import time # only necessary if running this program as a loop
import numpy # for clip function

motor_l = 1 	# Left Motor (ch1)
motor_r = 2 	# Right Motor (ch2)
# NOTE: THERE ARE 4 OUTPUTS.  3 & 4 ACCESSIBLE THROUGH diode & accy functions

rcpy.set_state(rcpy.RUNNING) # initialize the rcpy library

# define functions to command motors, effectively controlling PWM
def MotorL(speed): # takes argument in range [-1,1]
    motor.set(motor_l, speed)

def MotorR(speed): # takes argument in range [-1,1]
    motor.set(motor_r, speed)

def diode(state, channel): # takes argument in range [0,1]
    np.clip(state, 0, 1) # limit the output, disallow negative voltages
    motor.set(channel, state)
    
def accy(state, channel): # takes argument in range [-1,1]
    motor.set(channel, state)

# Uncomment this section to run this program as a standalone loop
# while rcpy.get_state() != rcpy.EXITING: # exit loop if rcpy not ready
#     if rcpy.get_state() == rcpy.RUNNING: # execute loop when rcpy is ready
#         print("L1_motors.py: driving fwd")
#         MotorL(0.4)  # gentle speed for testing program. 0.3 PWM may not spin the wheels.
#         MotorR(0.4)
#         time.sleep(4) # run fwd for 4 seconds
#         print("L1_motors.py: driving reverse")
#         MotorL(-0.6)
#         MotorR(-0.6)
#         time.sleep(2) # run reverse for 2 seconds

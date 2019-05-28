# speed_control.py takes target speeds and generates duty cycles
# to send to motors, and will perform PID control (when finalized)

import motors_ex2 as m
import numpy as np

# generate_duty is a placeholder function for the inverse kinematics program
def generate_duty(x_dot,theta_dot):
    # Calculate Left and Right Wheel Duty Cycles
    duty_r = ((  1 * (theta_dot)) + x_dot )
    duty_l = (( -1 * (theta_dot))  + x_dot )
    duties = np.array([ duty_l, duty_r ])   # put the values into an array
    duties[0] = sorted([-1, duties[0], 1])[1] # place bounds on duty cycle
    duties[1] = sorted([-1, duties[1], 1])[1] # place bounds on duty cycle
    return duties

def drive(x_dot, theta_dot):
    duties = generate_duty(x_dot, theta_dot)
    m.MotorL(duties[0]) # fcn allows -1 to 1
    m.MotorR(duties[1]) # fcn allows -1 to 1

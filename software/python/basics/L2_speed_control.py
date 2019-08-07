# speed_control.py takes target speeds and generates duty cycles
# to send to motors, and will perform PID control (when finalized)

import L1_motors as m
import numpy as np
import time
import log


# THE FOLLOWING FUNCTION PAIR IS FOR BOTH MAPPING AND DRIVING BY THETA & # X
# DO NOT USE THIS SECTION UNLESS INVERSE KINEMATICS IS BROKEN.
#----------------------------------------------------------------------------
# generate_duty is a placeholder function for the inverse kinematics program
u_integral = 0

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

# THE FOLLOWING FUNCTION PAIR IS FOR BOTH MAPPING AND DRIVING BY pdl & pdr targets
#----------------------------------------------------------------------------
# a function for converting target rotational speeds to PWMs without feedback
def openLoop(pdl,pdr):
    DRS = 0.8   # create a variable for direct-re-scaling
    duty_l = pdl * 1/9.75 * DRS  # 1 is max voltage and 9.75 is max rad/s possible
    duty_r = pdr * 1/9.75 * DRS  #
    duties = np.array([ duty_l, duty_r ])     # put the values into an array
    duties[0] = sorted([-1, duties[0], 1])[1] # place bounds on duty cycle
    duties[1] = sorted([-1, duties[1], 1])[1] # place bounds on duty cycle
    return duties

def driveOpenLoop(dutyl,dutyr):
    duties = openLoop(dutyl,dutyr)
    m.MotorL(duties[0])
    m.MotorR(duties[1])


def scalingFunction(x):
    if -0.222 < x and x < 0.222:
        y = (x * 3)
    elif x > 0.222:
        y = ((x * 0.778) + 0.222)
    else:
        y = ((x * 0.778) - 0.222)
    return y
    
def scaleMotorEffort(u):
    u_out = np.zeros(2)
    u_out[0] = scalingFunction(u[0])
    u_out[1] = scalingFunction(u[1])
    return(u_out)

def driveClosedLoop(pdt, pdc, de_dt):
    global u_integral
    e = (pdt - pdc) # compute error
    kp = 0.07  # proportional constant
    ki = 0.011 # integral constant
    kd = 0     # derivative constant
    
    # generate components of the control effort, u
    u_proportional = (e * kp)     # proportional term
    u_integral    += (e * ki)     # integral term 
    u_derivative   = (de_dt * kd) # derivative term
    # condition the signal before sending to motors 
    u = np.round((u_proportional + u_integral),2) # must round to ensure driver handling
    u = scaleMotorEffort(u)
    u[0] = sorted([-1,u[0],1])[1]  # place bounds on the motor commands
    u[1] = sorted([-1,u[1],1])[1]  # within [-1, 1]
    # send the signal to motors
    m.MotorL(round(u[0],2)) # must round to ensure driver handling!
    m.MotorR(round(u[1],2)) # must round to ensure driver handling!

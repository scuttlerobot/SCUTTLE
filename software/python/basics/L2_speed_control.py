#!/usr/bin/python3

# speed_control.py takes target speeds and generates duty cycles
# to send to motors, and has a function to execute PID control.

# Import external libraries
import numpy as np                                  # for handling arrays

# Import local files
import L1_motors as m                               # for controlling motors

# Initialize variables
u_integral = 0
DRS = 0.8
kp = 0.04                                           # proportional term
ki = 0.04                                           # integral term
kd = 0.0                                            # derivative term
pidGains = np.array([kp, ki, kd])                   # form an array to collect pid gains.


# a function for converting target rotational speeds to PWMs without feedback
def openLoop(pdl, pdr):
    DRS = 0.8                                       # create a variable for direct-re-scaling
    duties = np.array([pdl, pdr])                   # put the values into an array
    duties = duties * 1/9.75 * DRS                  # rescaling. 1=max PWM, 9.75 = max rad/s achievable
    duties[0] = sorted([-1, duties[0], 1])[1]       # place bounds on duty cycle
    duties[1] = sorted([-1, duties[1], 1])[1]       # place bounds on duty cycle
    return duties


def driveOpenLoop(pdTargets):                       # Pass Phi dot targets to this function
    duties = openLoop(pdTargets[0], pdTargets[1])   # produce duty cycles from the phi dots
    m.MotorL(duties[0])                             # send command to motors
    m.MotorR(duties[1])                             # send command to motors


def scalingFunction(x):                             # a fcn to compress the PWM region where motors don't turn
    if -0.222 < x and x < 0.222:
        y = (x * 3)
    elif x > 0.222:
        y = ((x * 0.778) + 0.222)
    else:
        y = ((x * 0.778) - 0.222)
    return y


def scaleMotorEffort(u):                            # send the control effort signals to the scaling function
    u_out = np.zeros(2)
    u_out[0] = scalingFunction(u[0])
    u_out[1] = scalingFunction(u[1])
    return(u_out)


def driveClosedLoop(pdt, pdc, de_dt):               # new function requires pidGains argument
    global u_integral
    e = (pdt - pdc)                                 # compute error

    kp = pidGains[0]
    ki = pidGains[1]
    kd = pidGains[2]

    # generate components of the control effort, u
    u_proportional = (e * kp)                                       # proportional term
    # u_integral += (e * ki)
    try:
        u_integral += (e * ki)                                      # integral term
    except:
        u_integral = (e*ki)

    u_derivative = (de_dt * kd)                                     # derivative term

    # condition the signal before sending to motors
    u = np.round((u_proportional + u_integral + u_derivative), 2)   # must round to ensure driver handling
    u = scaleMotorEffort(u)                                         # perform scaling - described above
    u[0] = sorted([-1, u[0], 1])[1]                                 # place bounds on the motor commands
    u[1] = sorted([-1, u[1], 1])[1]                                 # within [-1, 1]

    # send the signal to motors
    m.MotorL(round(u[0], 2))                                        # must round to ensure driver handling!
    m.MotorR(round(u[1], 2))                                        # must round to ensure driver handling!
    return

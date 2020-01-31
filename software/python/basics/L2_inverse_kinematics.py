#!/usr/bin/python3

# inverse_kinematics.py will take in motion requests in theta
# and x form, and output motion requests in phi dot (left & right)

# Import external libraries
import numpy as np                          # to perform matrix operations
import time

# Import internal programs
import L1_gamepad as gp                     # to call getGP from gamepad

# define robot geometry
R = 0.041                                   # wheel radius
L = 0.201                                   # half of the wheelbase
A = np.array([[1/R, -L/R], [1/R, L/R]])     # matrix A * [xd, td] = [pdl, pdr]

# define constraints for theta and x speeds
max_xd = 0.4                                # maximum achievable x_dot (m/s) FW  translation
max_td = (max_xd / L)                       # maximum achievable theta_dot (rad/s)


def map_speeds(B):                          # this function will map the gamepad speeds to max values
    B_mapped = np.zeros(2)
    B_mapped[0] = max_xd*B[0]
    B_mapped[1] = max_td*B[1]
    return(B_mapped)


def populate_gp():
    gpData = gp.getGP()                     # when there is no controller input, update is empty
    global axes                             # create a global variable for other programs to access
    try:                                    # when update has no data, update.size DNE
        if gpData.size == 16:               # if update has data, store it to axes
            axes = gpData                   # now axes is a 16-element array
    except:
        pass

    # assign axes from gamepad to requested velocities
    x_dot = -1*axes[1]                      # assign forward axis, inverted
    theta_dot = -1*axes[0]                  # assign L/R axis, inverted
    B_raw = np.array([x_dot, theta_dot])    # form the B matrix
    B = map_speeds(B_raw)                   # re map the values to within max achievable speeds
    print("td:", B[1])
    return(B)


# Convert will take the "B" matrix containing [x_dot, theta_dot]
# and return the C matrix containing [phi_dot_L, phi_dot_R]
def convert(B):
    C = np.matmul(A, B)                     # matrix multiplication
    C = np.round(C, decimals=3)             # round both elements in the array
    return(C)


def getPdTargets():
    B = populate_gp()                       # retrieves targets in [xdot, thetadot] form
    C = convert(B)                          # convert the targets to [pdl, pdr] form
    C = np.clip(C, -9.7, 9.7)
    return(C)


# create a function that can convert an obstacle into an influence on theta dot
def phi_influence(yValue):
    limit = 0.30                                            # meters to limit influence
    if (yValue < limit and yValue > 0):
        theta_influence = max_td*0.7*(limit - yValue)       # give theta push only if object is near
    elif (yValue > -limit and yValue < 0):
        theta_influence = -1*max_td*0.7*(limit - yValue)    # give theta push only if object is near
    else:
        theta_influence = 0
    B = np.array([0, theta_influence])
    C = np.matmul(A, B)
    return(C)


if __name__ == "__main__":
    while True:
        x_dot = 1                           # meters per second
        theta_dot = 0                       # radians per second
        B = np.array([x_dot, theta_dot])
        phis = convert(B)                   # convert [xd, td] to [pdl, pdr]
        print(phis[0])                      # print pdl
        time.sleep(0.5)

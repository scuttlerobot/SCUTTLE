# inverse_kinematics.py will take in motion requests in theta
# and x form, and output motion requests in phi dot (left & right)

import numpy as np # to perform matrix operations
import time
import gamepad_ex2 as gp # to call getGP from gamepad

# define robot geometry
R = 0.041 # wheel radius
L = 0.201 # half of the wheelbase
A = np.array([[1/R, L/R],[1/R, -L/R]])
# define constraints for theta and x speeds
max_td = 1.99 # maximum achievable theta x_dot
max_xd = 0.4 # maximum achievable x_dot

def map_speeds(B): # this function will map the gamepad speeds to max values
    B_mapped = np.zeros(2)
    B_mapped[0] = max_xd*B[0]
    B_mapped[1] = max_td*B[1]
    return(B_mapped)

def populate_gp():
    gpData = gp.getGP() #when there is no controller input, update is empty
    try:                      # when update has no data, update.size DNE
        if gpData.size == 16:  # if update has data, store it to axes
            axes = gpData # now axes is a 16-element array
            #print("gpData size :", gpData.size)
    except:
        pass

    # assign axes from gamepad to requested velocities
    x_dot = -1*axes[1] # assign forward axis, inverted
    theta_dot = -1*axes[0] # assign L/R axis, inverted
    B_raw = np.array([x_dot, theta_dot]) # form the B matrix
    B = map_speeds(B_raw) # re map the values to within max achievable speeds
    return(B)

# get_inv will take the "B" matrix containing x_dot and theta_dot
# and return the C matrix containing phi_dot (left and right)
def get_phis():
    B = populate_gp()
    C = np.matmul(A, B)
    return(C)

# UNCOMMENT THE CODE BELOW TO RUN AS A STANDALONE PROGRAM
# while(1):
#     x_dot = 1 #meters per second
#     theta_dot = 0 # radians per second
#     B = np.array([x_dot, theta_dot])
#     phis = get_inv(B)
#     print(phis[0])
#     time.sleep(0.5)

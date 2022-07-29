# inverse_kinematics.py calculates wheel speeds from chassis speeds
# Calculations will intake motion requests in [theta, x] (rad, m)
# and output motion requests in [phi dot Left, pi dot right] (rad/s).
# This program runs on SCUTTLE with any CPU. 

# Import external libraries
import numpy as np                          # to perform matrix operations
import time

# define robot geometry
R = 0.041                           # wheel radius
L = 0.201                           # half of the wheelbase
A = np.array([[1/R, -L/R], 
              [1/R, L/R]])          # matrix A * [xd, td] = [pdl, pdr]

# define constraints for x_dot and theta_dot
max_xd = 0.4                        # maximum achievable x_dot (m/s), forward speed
max_td = (max_xd / L)               # maximum achievable theta_dot (rad/s), rotational speed

# Transform joystick position with x and y ranging (-1,1) into robot speed [xdot, thetadot]
def map_speeds(B):                          
    B_mapped = np.zeros(2)
    B_mapped[0] = max_xd*B[0]
    B_mapped[1] = max_td*B[1]
    return(B_mapped)

# Convert desired robot speeds [xdot, thetadot] to wheel speeds [pdl, pdr]
def getPdTargets(B):
    C = np.matmul(A, B)             # matrix multiplication: converts [xdot, thetadot] to [pdl, pdr]
    C = np.round(C, decimals=3)     # round the result
    C = np.clip(C, -9.7, 9.7)       # keep it between -9.7 and +9.7, the max wheel speeds in rad/s
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


# this function takes user input for x_dot and theta_dot
def wait_user():
    x_dot = input("please enter x_dot (m/s): ")                     # takes x_dot as user input
    theta_dot = input("please enter theta_dot (rad/s): ")             # takes theta_dot as user input
    return (float(x_dot) , float(theta_dot))                    # returns x_dot and theta_dot


if __name__ == "__main__":
    while True:
        x_dot , theta_dot = wait_user()                     # user input [x_dot,theta_dot]
        B = np.array([x_dot, theta_dot])                    # make user inputs into an array
        phis = getPdTargets(B)                                   # convert [xd, td] to [pdl, pdr]
        print("pdl",phis[0],"\tpdr",phis[1])                # print pdl & pdr
        time.sleep(1)
# inverse_kinematics.py will take in motion requests in theta
# and x form, and output motion requests in phi dot (left & right)

import numpy as np
import time

R = 0.041 # wheel radius
L = 0.201 # half of the wheelbase
A = np.array([[1/R, L/R],[1/R, -L/R]])

# get_inv will take the "B" matrix containing x_dot and theta_dot
# and return the C matrix containing phi_dot (left and right)
def get_inv( B ):
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

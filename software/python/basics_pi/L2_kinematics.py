# This program takes the encoder values from encoders, computes wheel movement
# and computes the movement of the wheelbase center based on SCUTTLE kinematics.
# This program runs on SCUTTLE with any CPU.

# THIS PROGRAM IS IN PROGRESS AS OF 2020.11 (DPM)

# Import external libraries
import numpy as np                          # library for math operations
import time                                 # library for time access

# Import local files
import L1_encoder as enc                    # local library for encoders

# define kinematics
R = 0.041                                   # wheel radius (meters)
L = 0.201                                   # half of wheelbase (meters)
res = (360/2**14)                           # resolution of the encoders (degrees per LSB)
pulleyRatio = 0.5                           # wheel movement per shaft movement
A = np.array([[R/2, R/2], [-R/(2*L), R/(2*L)]])     # This matrix relates [PDL, PDR] to [XD,TD]
wait = 0.02                                 # wait time between encoder measurements (s)


# Note:  this function takes at least 5.1ms plus "wait" to run.  It also populates a global
# variable so programs can access the previous measurement instantaneously.
def getPdCurrent():
    global pdCurrents                       # make a global var for easy retrieval
    encoders_t1 = enc.readShaftPositions()  # grabs the current encoder readings in degrees
    t1 = time.monotonic()                   # time.monotonic() reports in seconds
    time.sleep(wait)                        # delay for the specified amount
    
    encoders_t2 = enc.readShaftPositions()  # grabs the current encoder readings in degrees
    t2 = time.monotonic()                   # usually takes about .003 seconds gap
    global deltaT
    deltaT = round((t2 - t1), 3)            # compute delta-time (t.ttt scalar)

    # calculate travel of both wheels simultaneously
    travel = encoders_t2 - encoders_t1      # compute change in both shaft encoders (degrees)
    travel = encoders_t2 - encoders_t1      # array, 2x1 to indicate travel
    trav_b = travel + 360                   # array variant b
    trav_c = travel - 360                   # array variant c
    mx = np.stack((travel, trav_b, trav_c)) # combine array variants
    mx_abs = np.absolute(mx)                # convert to absolute val
    mins = np.argmin(mx_abs,0)              # find the indices of minimum values (left and right hand)
    left = mx[mins[0],0]                    # pull corresponding indices from original array
    right = mx[mins[1],1]                   # pull corresponding index for RH
    shaftTravel = np.array([left,right])    # combine left and right sides to describe travel (degrees)
    
    # build an array of wheel speeds in rad/s
    wheelTravel = shaftTravel * pulleyRatio     # compute wheel turns from motor turns
    wheelSpeeds_deg = wheelTravel / deltaT      # compute wheel speeds (degrees/s)
    pdCurrents = wheelSpeeds_deg * np.pi / 180  # compute wheel speeds (rad/s) & store to global variable
    return(pdCurrents)                          # returns [pdl, pdr] in radians/second


def getMotion():                            # this function returns the chassis speeds
    B = getPdCurrent()                      # store phidots to array B (here still in rad/s)
    C = np.matmul(A, B)                     # perform matrix multiplication
    C = np.round(C, decimals=3)             # round the matrix
    return(C)                               # returns a matrix containing [xDot, thetaDot]

def phiTravels(encoders_t1, encoders_t2):   # get travel of wheels [deg, deg] (take no measurements)
    travel = encoders_t2 - encoders_t1      # compute change in both shaft encoders (degrees)
    travel = encoders_t2 - encoders_t1      # array, 2x1 to indicate travel
    trav_b = travel + 360                   # array variant b
    trav_c = travel - 360                   # array variant c
    mx = np.stack((travel, trav_b, trav_c)) # combine array variants
    mx_abs = np.absolute(mx)                # convert to absolute val
    mins = np.argmin(mx_abs,0)              # find the indices of minimum values (left and right hand)
    left = mx[mins[0],0]                    # pull corresponding indices from original array
    right = mx[mins[1],1]                   # pull corresponding index for RH
    shaftTravel = np.array([left,right])    # combine left and right sides to describe travel (degrees)
    wheelTravel = shaftTravel * pulleyRatio # compute wheel turns from motor turns [deg,deg]
    return(wheelTravel)                     # return the movement

# THIS SECTION ONLY RUNS IF THE PROGRAM IS CALLED DIRECTLY
if __name__ == "__main__":
    while True:
        C = getMotion()  # This take approx 25.1 ms if the delay is 20ms
        print("xdot(m/s), thetadot (rad/s):", C, "\t","deltaT: ", deltaT)
        time.sleep(0.2)
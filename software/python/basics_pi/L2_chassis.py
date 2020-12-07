# This program offers a chassis object that collects info from L1_motor and L1_encoder.
# We also import L2_kinematics to perform some chassis calculations.
# chassis parameters can be updated in the chassis object in realtime.
# Storing parameters in the object will give immediate access to other programs.
# Last updated 2020.12 DPM

# Import external libraries
import time
import math
import numpy as np                                         # for handling arrays
from fastlogging import LogInit                            # for logging & debug

# Import local files
#from scuttlepy import PID                                 # for PID controller
import L1_motor as m                                       # for controlling motors
import L1_encoder as enc                                   # for reading encoders
import L2_kinematics as kin                                # for calculating chassis movement

# THIS SECTION WILL BE PREPARED AND TESTED NEXT
import os                                                  # to make command line commands
if os.path.exists("robotTest.log"):                        # clear the previous log
    os.remove("robotTest.log")
logger = LogInit(pathName="./robotTest.log")               # Set up fresh logger
logger.debug("ColumnA ColumnB ColumnC ColumnD")            # make columns

class chassis:
    def __init__(self):
        self.speed = 0                                  # meters/sec
        self.heading = 0                                # degrees from North
        self.angularVelocity = 0                        # rad/s
        self.globalPosition = np.array([0, 0])          # cartesian [x, y] meters
        self.angularDisplacement = 0                    # For tracking displacement between waypoints
        self.forwardDisplacement = 0                    # For tracking displacement between waypoints
        self.pulleyRatio = 2.0                          # output/input ratio

        self.shaft1 = np.array([0,0])                   # left, right (deg)
        self.shaft2 = np.array([0,0])                   # left, right (deg)
        self.phis = np.array([0,0])                     # left, right (deg)

        self.wheelBase = 0.180                          # L - meters    Measured from center of wheel base to inside edge of wheel.
        self.wheelRadius = 0.041                        # R - meters
        self.wheelIncrements = np.array([0, 0])         # Latest increments of wheels
        self.wheelSpeeds = [0, 0]                       # [Left wheel speed, Right wheel speed.]
        self.t1 = time.monotonic()                      # time sample 1
        self.t2 = 0                                     # time sample 2
        self.loopPeriod = 0.060                         # How fast to make the loop (s)
        self.loopStart = time.monotonic()               # Updates when we grab chassis displacements
        self.sleepTime = 0                              # Time to sleep updated per loop

        self.l_motorChannel = 1
        self.r_motorChannel = 2
        self.l_encoderAddress = 0x40                    # Left wheel encoder address
        self.r_encoderAddress = 0x41                    # Right wheel encoder address

    def setGlobal(self, pos):                           # assign calculated value to the global [x,y]
        self.globalPosition = pos

    def setHeading(self, heading):                      # assign calculated value to the global (deg)
        self.heading = heading

    def updateShaftPositions(self):                     # (TAKE READING) take a new reading on wheels
        self.shaft1 = self.shaft2                       # reassign the latest value to previous
        self.shaft2 = enc.readShaftPositions()          # measure shaft positions
        self.t1 = self.t2                               # reassign the time sample
        self.t2 = time.monotonic()                      # grab the latest time
        return self.shaft2                              # return latest shaft positions [deg, deg]

    def getWheelIncrements(self):                       # (NO READING) get wheel increment
        s1 = self.shaft1                                # first you must update shaft2 via updateShaftPositions()
        s2 = self.shaft2
        self.wheelTravel = kin.phiTravels(s1, s2)
        return self.wheelTravel                         # return wheel travels between datapoints

    def updatePhis(self):                               # (NO READING) first must update getWheelIncrement
        self.phis = self.phis + self.wheelTravel        # add the latest value to previous
        self.phis = np.round(self.phis, 4)              # round the values
        logger.debug("Phis(deg) " + str(self.phis[0])   # log phi positions
                            + " " + str(self.phis[1]))
        return self.phis                                # return latest wheel positions [deg, deg]

    def updatePhiDots(self):                            # (NO READING) compute phidots (wheel speeds) (deg/s)
        dt = self.t2 - self.t1                          # compute delta-time from last samples
        # print("t2: ", self.t2)
        # print("dt ", dt)
        self.wheelSpeeds = self.wheelTravel / dt        # compute wheel speeds (deg/s)
        self.wheelSpeeds = np.round(self.wheelSpeeds,3) # round the values
        logger.debug("Phidots(deg/s) "                  # log phi positions
                    + str(self.wheelSpeeds[0]))
        return self.wheelSpeeds                         # return phi dots

    def getChassis(self, displacement):                  # returns [dx, dth] given [delta phi L, delta phi R]
        L = self.wheelBase
        R = self.wheelRadius
        A = np.array([[     R/2,     R/2],
                      [-R/(2*L), R/(2*L)]])              # This matrix relates [PDL, PDR] to [XD,TD]
        B = displacement                                 # this array should store phi displacements (in radians)
        C = np.matmul(A, B)                              # perform matrix multiplication
        C = np.round(C, decimals=3)                      # round the matrix
        return C                                         # returns a matrix containing [dx (m), dTheta (rad)]
    
    def getWheels(self, chassisValues):                  # Inverse Kinematic function. Take x_dot, theta_dot as arguments
        L = self.wheelBase
        R = self.wheelRadius
        A = np.array([[ 1/R, -L/R],                      # This matrix relates chassis to wheels
                      [ 1/R,  L/R]])
        B = np.array([chassisValues[0],                  # Create an array for chassis speed
                      chassisValues[1]])
        C = np.matmul(A, B)                              # Perform matrix multiplication
        return C                                         # Returns Phi_dots, (rad or rad/s)

# THE NEXT SECTION WILL BE MADE TO TRACK AND STORE INFO ABOUT THE CHASSIS POSITION
# INCLUDING: X and Y position of the wheelbase center, latest chassis speed,
# rotational velocity of the chassis, and rotational displacement of chassis.

if __name__ == "__main__":
    chas = chassis()
    while 1:
        
        shaft = chas.updateShaftPositions()
        wheelInc = chas.getWheelIncrements()
        phis = chas.updatePhis()
        phiDots = chas.updatePhiDots()
        print("Wheel increments: ", wheelInc, "\t \t positions: ", phis)
        time.sleep(0.4)
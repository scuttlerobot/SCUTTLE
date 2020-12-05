# This program offers a chassis object that collects info from L1_motor and L1_encoder.
# chassis parameters can be updated in the chassis object in realtime.
# Storing parameters in the object will give immediate access to other programs.
# Last updated 2020.12 DPM

# Import external libraries
import time
import math
import numpy as np                                                          # for handling arrays
from fastlogging import LogInit                                             # for logging & debug

# Import local files
from scuttlepy import PID                                                    # for PID controller
from scuttlepy import L1_motor                                                 # for controlling motors
from scuttlepy import L1_encoder                                               # for reading encoders

import os                                                                   # to make command line commands
if os.path.exists("robotTest.log"):                                         # clear the previous log
    os.remove("robotTest.log")
logger = LogInit(pathName="./robotTest.log")                                # Set up fresh logger
logger.debug("ColumnA ColumnB ColumnC ColumnD")                             # make columns

class chassis:
    def __init__(self, )
self.speed = 0
        self.heading = 0
        self.angularVelocity = 0
        self.globalPosition = np.array([0, 0])
        self.angularDisplacement = 0                                        # For tracking displacement between waypoints
        self.forwardDisplacement = 0                                        # For tracking displacement between waypoints

        self.wheelBase = 0.180                                              # L - meters    Measured from center of wheel base to inside edge of wheel.
        self.wheelRadius = 0.041                                            # R - meters
        self.wheelIncrements = np.array([0, 0])                             # Latest increments of wheels
        self.wheelSpeeds = [0, 0]                                           # [Left wheel speed, Right wheel speed.]
        self.timeInitial = time.monotonic()
        self.timeFinal = 0
        self.loopPeriod = 0.060                                             # How fast to make the loop (s)
        self.loopStart = time.monotonic()                                   # Updates when we grab chassis displacements
        self.sleepTime = 0                                                  # Time to sleep updated per loop

        self.l_motorChannel = 1
        self.r_motorChannel = 2
        self.l_encoderAddress = 0x40 # Left wheel encoder address
        self.r_encoderAddress = 0x41 # Right wheel encoder address

    def setGlobal(self, pos):
        self.globalPosition = pos

    def setHeading(self, heading):
        self.heading = heading

    def getWheelIncrements(self):   # get the wheel increment in radians

        positionInitial = enc.readShaftPositions()
        self.timeInitial = self.timeFinal

        self.timeFinal = time.monotonic()
        wheelIncrements = # must calculate (in radians)
        timeIncrement = self.timeFinal - self.timeInitial

        self.wheelSpeeds = wheelIncrements / timeIncrement                  # speed = distance/time

        logger.debug("Time_Increment(s) " + str(round(timeIncrement, 3)) )
        logger.debug("Wheel_Increments(rad) " + str(round(wheelIncrements[0], 4))
                     + " " + str(round(wheelIncrements[1], 4)))

        return wheelIncrements

    def getChassis(self, displacement):                                     # returns chassis displacement since last reading
        L = self.wheelBase
        R = self.wheelRadius
        A = np.array([[     R/2,     R/2],
                      [-R/(2*L), R/(2*L)]])                                 # This matrix relates [PDL, PDR] to [XD,TD]
        B = displacement                                                    # this array should store phi displacements (in radians)
        C = np.matmul(A, B)                                                 # perform matrix multiplication
        C = np.round(C, decimals=3)                                         # round the matrix
        return C                                                            # returns a matrix containing [dx (m), dTheta (rad)]

    def getChassisVelocity(self):                                           # Function to update and return [x_dot,theta_dot]
        B = np.array([self.l_wheel.speed,                                   # make an array of wheel speeds (rad/s)
                      self.r_wheel.speed])
        C = self.getChassis(B)                                              # Perform matrix multiplication
        self.speed = C[0]                                                   # Update speed of SCUTTLE [m/s]
        self.angularVelocity = C[1]                                         # Update angularVelocity = [rad/s]
        return [self.speed, self.angularVelocity]                           # return [speed, angularVelocity]
    
    def getWheels(self, chassisValues):                                     # Inverse Kinematic function. Take x_dot, theta_dot as arguments
        L = self.wheelBase
        R = self.wheelRadius
        A = np.array([[ 1/R, -L/R],                                         # This matrix relates chassis to wheels
                      [ 1/R,  L/R]])
        B = np.array([chassisValues[0],                                     # Create an array for chassis speed
                      chassisValues[1]])
        C = np.matmul(A, B)                                                 # Perform matrix multiplication
        return C                                                            # Returns Phi_dots, (rad or rad/s)

    def displacement(self, chassisIncrement):
        # chassisIncrement = self.getChassis(self.getWheelIncrements())       # get latest chassis travel (m, rad)
        self.forwardDisplacement = chassisIncrement[0]                      # add the latest advancement(m) to the total
        self.angularDisplacement = chassisIncrement[1]                      # add the latest advancement(rad) to the total
        logger.debug("Chassis_Increment(m,rad) " +
            str(round(chassisIncrement[0], 4)) + " " +
            str(round(chassisIncrement[1], 4)) + " " +
            str(time.monotonic()))
        self.loopStart = time.monotonic()                                   # use for measuring loop time
        logger.debug("TimeStamp(s) " + str(self.loopStart))
        logger.debug("Gyro_raw(deg/s) " +
            str(round(self.imu.getHeading(), 3)) + " " +
            str(time.monotonic()))

    def stackDisplacement(self):                                            # add the latest displacement to the global position
        theta = self.heading + ( self.angularDisplacement / 2 )             # use the "halfway" vector as the stackup heading
        c, s = np.cos(theta), np.sin(theta)
        R = np.array(((c, -s), (s, c)))                                     # create the rotation matrix
        localVector = np.array([self.forwardDisplacement, 0])               # x value is increment and y value is always 0
        globalVector = np.matmul(R, localVector)
        self.globalPosition = self.globalPosition + globalVector            # add the increment to the global position
        logger.debug("global_x(m) " +
            str(round(self.globalPosition[0], 3)) + " global_y(m) " +
            str(round(self.globalPosition[1], 3) ) )
        return self.globalPosition

    
    def stackHeading(self):                                                 # increment heading & ensure heading doesn't exceed 180
        self.heading = self.heading + self.angularDisplacement              # update heading by the turn amount executed
        if self.heading > math.pi:
            self.heading += (2 * math.pi)
        if self.heading < -math.pi:
            self.heading += (2 * math.pi)
        logger.debug("heading(deg) " + str(round(math.degrees(self.heading), 3)))
        return self.heading

    def checkLoop(self):
        self.loopFinish = time.monotonic()
        self.sleepTime = self.loopPeriod - (self.loopFinish - self.loopStart)
        logger.debug("sleepTime(s) " + str(round(self.sleepTime, 3)) )
        return(self.sleepTime)

    def setup(self):                                                        # call this before moving to points
        self.getWheelIncrements()                                           # get the very first nonzero readings fron enconders
        self.setMotion([0,0])                                               # set speed zero
        self.displacement(self.getChassis(self.getWheelIncrements()))       # increment the displacements (update robot attributes)
        self.stackDisplacement()                                            # add the new displacement to global position
        self.stackHeading()                                                 # add up the new heading

if __name__ == "__main__":

    r_wheel = Wheel(2, 0x40) 	                                            # Right Motor (ch2)
    l_wheel = Wheel(1, 0x43, invert_encoder=True)                           # Left Motor  (ch1)

    r_wheel.setAngularVelocity(math.pi)
    l_wheel.setAngularVelocity(math.pi)

    while 1:

        r_wheel.getAngularVelocity()
        l_wheel.getAngularVelocity()


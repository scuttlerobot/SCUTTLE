# This program takes the encoder values from encoders, computes wheel movement
# and computes the movement of the wheelbase center based on SCUTTLE kinematics.

# //usr/bin/python3
import Adafruit_GPIO.I2C as Adafruit_I2C #i2c communication
import numpy as np			  #scientific computing
import time					 #time access and conversions

# --- david M speed calc-----
degL0 = 0
degL1 = 0
travL = 0
distL = 0
whlSpdL = 0
wsl0 = 0
degR0 = 0
degR1 = 0
travR = 0
distR = 0
whlSpdR = 0
wsr0 = 0
xLoc = 0
yLoc = 0
cgSpeedPrev = 0
cgSpeed = 0
theta = 0

# --- encoders
enc0 = Adafruit_I2C.Device(0x40,1)
enc1 = Adafruit_I2C.Device(0x41,1)
PreviousEncoderL=0
PreviousEncoder1 = 0
t0 = time.time()
t2 = 0;
timeA = 0

def read_encoders_angle(enc0,enc1):  # this function designed by Ahmad B
    try:
        x = enc0.readU16(0xFE)
        x = ((x << 8) | (x >> 8)) & 0xFFFF
        meas = ((x & 0xFF00) >> 2) | ( x & 0x3F)
        angle0 = meas*0.0219  # convert to degrees
    except:
        print('Warning (I2C): Could not read encoder0')
        angle0 = 0
    try:
        x = enc1.readU16(0xFE)
        x = ((x << 8) | (x >> 8)) & 0xFFFF
        meas = ((x & 0xFF00) >> 2) | ( x & 0x3F)
        angle1 = meas*0.0219 # convert to degrees
    except:
        print('Warning (I2C): Could not read encoder1')
        angle1 = 0
    return [angle0, angle1]

while 1:
    time.sleep(0.10) #delay 100ms
    ## --- grab encoders values
    encoderL, encoderR = read_encoders_angle(enc0,enc1)
    deltaT = time.time() - timeA
    timeA = time.time()

    #---- movement calculations
    # calculate the delta on Left wheel
    case_number = 0
    degL1 = round(encoderL,2)  # reading in degrees. Convert to meters by 0.0007306
    if(abs(abs(degL1) - abs(degL0)) < 1 ):
    	travL = 0 #ignore tiny movements
    	case_number=1
    elif(abs(abs(degL1) - abs(degL0)) < 100 ): # if movement is small (no rollover)
    	case_number=2
    	if(degL1 > degL0 + 2): travL = (degL1 - degL0) * 0.0007306 # if movement is positive
    	elif(degL0 > degL1 + 2): travL = (degL1 - degL0) * 0.0007306 # if movement is negative
    elif(degL0 - degL1 > 100):
    	travL = ((degL1 + 360.0) - degL0)*0.0007306 # if movement is large (rollover)
    	case_number=3
    elif(degL1 - degL0 > 100):
    	travL = (degL1 - (degL0 + 360.0))*0.0007306 # reverse and large (rollover)
    	case_number=4
    travL = -travL # right encoder is mounted reverse from the left
    degL0 = degL1 # setup for next loop
    distL = distL + travL  #distance in total since boot
    wsl0 = whlSpdL #store the previous value for averaging
    whlSpdL = travL/deltaT  #current speed
    wsla = (wsl0 + whlSpdL)/2 #wheel-speed-left-averaged

    # calculate the delta on Right wheel
    degR1 = round(encoderR,2)  # reading in degrees

    if(abs(abs(degR1) - abs(degR0)) < 1 ):
    	travR = 0 #ignore tiny movements
    	case_number=1
    elif(abs(abs(degR1) - abs(degR0)) < 100 ): # if movement is small (no rollover)
    	case_number=2
    	if(degR1 > degR0 + 2): travR = (degR1 - degR0) * 0.0007306 # if movement is positive
    	elif(degR0 > degR1 + 2): travR = (degR1 - degR0) * 0.0007306 # if movement is negative
    elif(degR0 - degR1 > 100):
    	travR = ((degR1 + 360.0) - degR0)*0.0007306 # if movement is large (rollover)
    	case_number=3
    elif(degR1 - degR0 > 100):
    	travR = (degR1 - (degR0 + 360.0))*0.0007306 # reverse and large (rollover)
    	case_number=4
    degR0 = degR1 # setup for next loop
    distR = distR + travR  #distance in total since boot
    wsr0 = whlSpdR #store the previous value for averaging
    whlSpdR = travR/deltaT  #current speed
    wsra = (wsr0 + whlSpdR)/2 #wheel-speed-right-averaged

    print(wsra)

    # calculate speed of wheelbase center
    travs = ([travL, travR])
    cgTrav = np.average(travs)
    speeds = ([ whlSpdL , whlSpdR ])
    cgSpeedPrev = cgSpeed
    cgSpeed = np.average(speeds)
    cgSpeedReport = (cgSpeed + cgSpeedPrev)/2

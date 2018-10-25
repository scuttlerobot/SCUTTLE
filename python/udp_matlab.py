# udp_matlab.py
# This program passes sensor data to matlab over UDP and
# receive commands from the keyboard for driving control.

# //usr/bin/python3
import Adafruit_GPIO.I2C as Adafruit_I2C
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import numpy as np
import socket
import struct
import subprocess
import time
import rcpy.mpu9250 as mpu9250
import scuttle as sc
#import compass
import math
from rcpy._adc import *

DATA_UPDATE_FREQ = 20.0 # Hertz

# --- initiliaze compass
I2Ccompass = Adafruit_I2C.Device(0x1e,1)
I2Ccompass.write8(0x00,0x70)
I2Ccompass.write8(0x02,0x01)
# ---
# --- encoders
enc0 = Adafruit_I2C.Device(0x40,1)
enc1 = Adafruit_I2C.Device(0x41,1)
PreviousEncoderL=0
#enc1.write8(0x02,0x3D)
# --- ultrasonic sensor pins
echo_pin = 'P9_23' # GPIO1_17 actual name on BB Black
trig_pin = 'GPIO3_20' # name on board diagram
GPIO.setup(echo_pin, GPIO.IN) 
GPIO.setup(trig_pin, GPIO.OUT)
# --- Initialize UDP
IPADDR = '192.168.8.1' #BBB ip address
PORTNUM = 3553 # port number, has to match the one in MATLAB
# initialize a socket, think of it as a cable
# SOCK_DGRAM specifies that this is UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
s.settimeout(0.0001) # 1ms
# connect the socket, think of it as connecting the cable to the address location
s.bind((IPADDR, PORTNUM))
# ---
# --- initialize on board imu
imu = mpu9250.IMU(enable_dmp = True, dmp_sample_rate = 20, enable_magentometer = False)
# ---
# --- initialize motor ports on BBB
Motor_X = 1
Motor_Y = 2
# ---

# --- david M speed calc-----
degL0 = 0
degL1 = 0
travL = 0
distL = 0
whlSpdL = 0
degR0 = 0
degR1 = 0
travR = 0
distR = 0
whlSpdR = 0

address = []
data = []
data_snt = 13*[0]
speedL, speedR = 127, 127
i = 0 #counter for encoder readings
avgEncoderWinSize = 5
array = avgEncoderWinSize*[0]   #dpm working vars
t0 = time.time()

t2 = 0;
PreviousEncoder1 = 0
timeA = 0

while 1:
    t1 = time.time()
    # --- any speed commands from matlab?
    try:
        data, address = s.recvfrom(65536)
    except:
        pass
    while data:
        speedL = data[0]
        speedR = data[1]
        if speedL == 127: 
            if speedR == 254:   # these 6 lines convert turning style to CG-centered
                speedL = 25                     # 80 percent reverse
                speedR = 229                    # 80 percent fwd
        if speedL == 254: 
            if speedR == 127:
                speedL = 229
                speedR = 25
        
        try:
            data, address = s.recvfrom(65536)
        except:
            break
    # --- 
    # --- did we reach 10ms? yes, send data to MATLAB
    if ((t1-t0) >= (1.0/DATA_UPDATE_FREQ)): # send data every 50 millisecond
        t0 = t1
        if address: # at least one package has to be received before we know where to send!
            PACKETDATA = struct.pack('%sf' %len(data_snt),*data_snt)
            s.sendto(PACKETDATA, address)
            data = []
    # --- 
## --- write speed to H-bridge
    sc.set_speed(speedL, speedR)
    voltage = round(get_dc_jack_voltage(),2)
    #[vDC0, vDC1] = motor.read_voltage()
    #[temp0, temp1] = motor.read_temperature()
    #print("voltage: ",voltage)
    

## --- reading the compass angle
    heading = sc.get_angle(I2Ccompass)
    x_compass = sc.read_xyz(I2Ccompass) #grabs 3 axes
    #print("compass: ",round(x_compass[1],0))  # values: x=[0], y=[1], z=[2]

## --- read pitch and roll
    data_imu = imu.read()#read_accel_data()#

## --- ultrasonic distance measurement using HC-SR04
    distance = sc.distanceMeasurement(trig_pin, echo_pin, GPIO)
    #distance = sc.ultrasonic("cm") # get distance in cm
    distance = round(distance,0)
    #print("ultrasonic: ",distance)

## --- encoders

    encoderL, encoderR = sc.read_encoders_angle(enc0,enc1)
    
    #Left side - this code block is used to create an averaging array
    # array[i%avgEncoderWinSize] = encoderL #assign latest reading to the proper array element
    # CurrentEncoderL = sum(array)/avgEncoderWinSize #take the average of the array
    deltaT = time.time() - timeA 
    timeA = time.time()
    
    # if not(i%avgEncoderWinSize):
    #     angle = 180 - abs(abs(CurrentEncoderL - PreviousEncoderL) - 180)
    #     deltaRadians = .01745*angle
    #     #speedL = deltaRadians/deltaT*0.5*.083 #should return meters/second
    #     PreviousEncoderL = CurrentEncoderL
    # i = i + 1

    # if i == 500: #reset i to prevent conversion to a different var type
    #     i = 1       

#---- movement calculations
# calculate the delta on Left wheel
    degL1 = encoderL  # reading in degrees
    if(degL1 > degL0 + 0.1): travL = (degL1 - degL0)*.0007306 #meters per degree
    elif(degL0 - degL1 > 350): travL = ((degL1 + 360) - degL0) # in case of rollover
    else : travL = 0;
    degL0 = degL1 # setup for next loop
    distL = distL + travL  #distance in total since boot
    whlSpdL = travL/deltaT  #current speed

# calculate the delta on Right wheel
    degR1 = encoderR  # reading in degrees
    if(degR1 > degR0 + 0.1): travR = (degR1 - degR0)*.0007306 #meters per degree
    elif(degR0 - degR1 > 350): travR = ((degR1 + 360) - degR0) # in case of rollover
    else : travR = 0;
    degR0 = degR1 # setup for next loop
    distR = distR + travR  #distance in total since boot
    whlSpdR = travR/deltaT  #current speed


            
## --- put data in array to send over udp
    data_snt[0] = heading
    data_snt[1] = voltage #vDC0
    #data_snt[2] = vDC1
    #data_snt[3] = temp0
    #data_snt[4] = temp1
    data_snt[6] = distL    # sends to encoder L
    data_snt[7] = distR    # sends to encoder R
    data_snt[8] = whlSpdL  # sends to speed L
    data_snt[9] = whlSpdR  # sends to speed R
    data_snt[10] = distance
    data_snt[11] = data_imu['tb'][0] # pitch
    data_snt[12] = data_imu['tb'][1] # roll
    #print(round(data_snt[11],4))
## ---
# close the socket (UDP connection)
s.close()
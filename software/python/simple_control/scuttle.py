# scuttle.py - core functions for scuttle robot (last update 2019.02.20)
# contains basic functions to gather data, perform minor interpretation, and command actuators

# Written By: Daniyal Ansari, David Malawey
# contains functions to run the SCUTTLE platform


import time, getopt, sys, math, serial, types, socket, signal, inspect, numpy as np, argparse, os
import rcpy
import rcpy.motor as motor
import rcpy.mpu9250 as mpu9250  # IMU Library
import numpy as np

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_GPIO.I2C as Adafruit_I2C

    #####################################
    #                                   #
    #       Configuration Values        #
    #                                   #
    #####################################

'''
    This configuration section allows you to change properties of the SCUTTLE library code.
'''
    #   Debugging Options

verbose = False  
log_output_location = "./scuttle_debugging.log"

    #   ADC Settings

valid_adc_pins = ("AIN0","AIN1","AIN2","AIN3")

    #   Compass Settings

comapss_i2c = Adafruit_I2C.Device(0x1e,1)   # I2C Bus Device Location

compass_write_registers =      (0x00, 0x02)     # Registers to Write Data to
compass_write_registers_data = (0x70, 0x01)     # Data to Write to Registers

    #   Rotary Encoder Settings

right_encoder = Adafruit_I2C.Device(0x40,1) # Power the Rotary Encoder Address Select Pin to change the address of the left encoder
left_encoder  = Adafruit_I2C.Device(0x41,1) # Power pin A0 to set address to 0x41 (default) or power pin A1 to set address to 0x42

    #   Motor Controller Settings

Motor_L = 1  # left motor connects to output 1
Motor_R = 2  # right motor connects to output 2

    #   UDP Control Settings

ip = "192.168.8.1"      # Set to the interface IP over which you will send UDP Data
port = 1337             # Set to the port to which you will send UDP Data

bufferSize = 1024   # Definitely too much space.

forward_key = 0     # The value the UDP server expects to recieve to perform an action
back_key    = 1
right_key   = 2
left_key    = 3
stop_key    = 4
quit_key    = 5

    #   Ultrasonic Sensor Settings

echo_pin = "P9_23"      # Ultrasonic Echo Pin
trig_pin = "GPIO3_20"   # Ultrasonic Trigger Pin

trigger_pulse_duration = 0.0001     # How long to hold TRIG On dictating pulse length

    # PMOD compass
   
def RotationMatrix(degrees):   #build a 2d rotation matrix
    theta = np.radians(degrees)
    c, s = round(np.cos(theta),4), round(np.sin(theta),4)
    R = np.array(((c,-s), (s, c)))
    return R

def read_xyz(i2c):  #get the values from the compass
    try:
        i2c.write8(0x02,0x01) # request values from compass
        a = i2c.readList(0x03,6)  # store values
        # for x and y, use offset and scaling to center on zero and give range of [-1,1]
        x_init = (np.int16((a[0] << 8) | a[1])/274) - 0.113
        y_init = (np.int16((a[4] << 8) | a[5])/330) + 0.185
        x_init = round(x_init,3)
        y_init = round(y_init,3)
        q = np.matrix([[x_init],[y_init]]) #create an x,y column matrix
        R = RotationMatrix(90) # the SCUTTLE compass is offset by +90.  This vector for rotation
        vectorA = np.dot(R,q) # take vector product, store the product in vectorA
        #print(vectorA)
        x = round(-y_init,3) #flip axis for cartesian style heading
        y = round(x_init,3) #flip axis for cartesian style heading
        z = 0 # this vector is not used
    except:
        print('Warning (I2C): Could not read compass')
        x,y,z = 0,0,0
    return [x,y,z]
   
def get_heading(i2c):  # designed to return value w.r.t. North
    x, y, z = read_xyz(i2c) #retrieve the scaled x, y, z values
    if x == 0: x = 0.01  # avoid dividing by zero
    heading = np.arctan(y/x)*180/np.pi
    heading = round(heading,1)
    if x < 0: heading = heading + 180
    elif y < 0: heading = heading + 360
    #print("X: ", x ," Y: ", y ," heading: ",heading)
    return heading

#   Rotary Encoder

def rotaryEncoder(motor=None,unit=None): # this function designed by Daniyal A

    if motor == "right":

        right_encoder.write8(0x02,0x3D)
        right_encoder_data = right_encoder.readList(0xfd,3)
        return(right_encoder_data[0],right_encoder_data[1],right_encoder_data[2])

    elif motor == "left":

        left_encoder.write8(0x02,0x3D)
        left_encoder_data = left_encoder.readList(0xfd,3)
        return(left_encoder_data[0],left_encoder_data[1],left_encoder_data[2])

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
#    else:
#        continue

#   Motor Controller

def set_speed(speedL, speedR): #in one function, cmd both motor driver channels

    motor.set(Motor_L, ((speedL-127)/127))  #h bridge commands
    motor.set(Motor_R, ((speedR-127)/127)) 
    
#   UDP Control

def udp_control(ip=None,port=None):

    exit = False

    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    sock.bind((ip, port))   # Start UDP Server

    data_l = [146, 32]  # Brake
    data_r = [146, 32]

    while exit == False:    # Start Infinite Loop and Exit Condition

        data, addr = sock.recvfrom(bufferSize) # buffer size is 1024 bytes

        if data == b"0":
            data_l = [255, 0, 254]  # Go Forward
            data_r = [255, 1, 254]  # Set Left and Right Motor Speeds to Full Forward

        elif data == b"1":
            data_l = [255, 0, 0]    # Go Backwards
            data_r = [255, 1, 0]    # Set Left and Right Motor Speeds to Full Backward

        elif data == b"2":
        	data_l = [255, 0, 254]  # Rotate Right
        	data_r = [255, 1,   0]  # Set Right Motor to Full Backward and Left Motor Speeds to Full Forward

        elif data == b"3":
            data_l = [255, 1, 254]  # Rotate Left
            data_r = [255, 0,   0]  # Set Left Motor to Full Backward and Right Motor Speeds to Full Forward

        elif data == b"4":
        	data_l = [146, 32]      # Brake
        	data_r = [146, 32]      # Set Left and Right Motor Speeds to Brake

        elif data == b"5":
            exit = True             # Quit udp_control()

        else:                       # Throw out any values not expected
            print("Unrecongnized Value!")
            continue

        ser_motor.write(data_l)     # Send Left Motor Data
        ser_motor.write(data_r)     # Send Right Motor Data

#   Ultrasonic Sensor

def sonar(TRIG,ECHO, GPIO):  # measure the distance in cm
    timeout = 0.01 # 10 milliseconds (max dist would be 1.71m)
    pulseEnd = time.time()
    pulseStart = time.time()
    GPIO.output(TRIG, True)
    time.sleep(0.0001)   # sleep for 0.1 milliseconds
    GPIO.output(TRIG, False)

    while (GPIO.input(ECHO) == 0):
        pulseStart = time.time()              #continuosly set start timing until ECHO rises
        if (pulseStart - pulseEnd) > timeout:
            break
    while (GPIO.input(ECHO) == 1):            #continuously set end timing until ECHO falls
        pulseEnd = time.time()
 
    pulseDuration = pulseEnd - pulseStart     #measure amount of time ECHO pin was high
    distance = pulseDuration * 17150          # convert value to cm
    distance = round(distance, 2)
    return distance

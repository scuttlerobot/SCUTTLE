# This code contains a function to turn your robot a specified angle.

import Adafruit_GPIO.I2C as Adafruit_I2C
import time
import math
import rcpy
import rcpy.motor as motor # moves
import rcpy.mpu9250 as mpu9250

# defaults
enable_magnetometer = False
sample_rate = 100
enable_fusion = False

show_tb = True

Motor_L = 1  # left motor connects to output 1
Motor_R = 2  # right motor connects to output 2

mpu9250.initialize(enable_dmp=True,
                   dmp_sample_rate=sample_rate,
                   enable_fusion=enable_fusion,
                   enable_magnetometer=enable_magnetometer)

def read_angle():

    data = mpu9250.read()
    data = data['tb']        # Get imu Value and Convert to Degrees (0 to 180 , -180 to 0)
    data = (math.degrees(round(data[2],2))) % 360     # Convert IMU reading to degrees
    return(data)

def read_accel():

    data = mpu9250.read()
    data = data['accel']
    x = data[0]
    y = data[1]
    return(x,y)

def turn(angle, speed=0.7):

    if rcpy.get_state() == rcpy.RUNNING:    # Only run if  RCPY is running

        turn = True # Sets infinite loop to True until turn is complete

        angle = angle % 360         # Get angle

        duty_l = 0
        duty_r = 0

        while turn:

            imu_deg = read_angle()

            if angle == 0:

                duty_l = 0
                duty_r = 0

            # Check Angle is from 0 to 180 or 180 to 360, to determine which direction to turn

            elif 0 < angle and 180 >= angle:   # If converted angle is between 0 and 180, point turn counter-clockwise

                duty_l = -1*speed  #   Rotate Left
                duty_r = speed

            elif 180 < angle and 360 > angle:   # If converted angle is between 180 and 360, point turn clockwise

                duty_l = speed  #   Rotate Right
                duty_r = -1*speed

            if (imu_deg-2) <= angle and angle <= (imu_deg+2):   # Once Angle is within Range Stop Motors

                duty_l = 0
                duty_r = 0
                turn = False

            motor.set(Motor_L, duty_l) #sets motor to duty cycle above
            motor.set(Motor_R, duty_r) #sets motor to duty cycle above

    final_imu_deg = read_accel()

    return(final_imu_deg)

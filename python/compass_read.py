# compass_read.py

# a simple tool to read and print the compass x and y values
# NOTE: This program does not calibrate your compass.
# This program does not check if your compass is oriented properly.
# The x-axis should point forward on the robot

import Adafruit_GPIO.I2C as Adafruit_I2C #i2c communication
import time                     #time access and conversions
import scuttle as sc            #custom scuttle program

# --- initiliaze compass
I2Ccompass = Adafruit_I2C.Device(0x1e,1)
I2Ccompass.write8(0x00,0x70)
I2Ccompass.write8(0x02,0x01)

while 1:

## --- reading the compass angle
    #heading = sc.get_heading(I2Ccompass)  #get the compass heading
    compass = sc.read_xyz(I2Ccompass) #grabs 3 axes, x points forward
    print("compass[0]: ", compass[0], ", compass[1]: ", compass[1]) # x axis
    time.sleep(0.5) #pause for 500ms

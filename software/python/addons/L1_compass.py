# This program is for communicating with an external i2C Compass, PMOD CMPS or CMPS2
# NOTE: This program does not calibrate your compass.
# This program does not check if your compass is mounted/oriented properly.
# The x-axis should point forward on the robot

import Adafruit_GPIO.I2C as Adafruit_I2C #i2c communication
import time                     #time access and conversions

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

# --- initiliaze compass
I2Ccompass = Adafruit_I2C.Device(0x30,1)    #   For Pmod CMPS2: 3-Axis Compass Address: 0x30
#I2Ccompass = Adafruit_I2C.Device(0x1e,1)    #   For Pmod CMPS: 3-axis Digital Compass: 0x1e

I2Ccompass.write8(0x00,0x70)
I2Ccompass.write8(0x02,0x01)

while 1:

## --- reading the compass angle
    #heading = sc.get_heading(I2Ccompass)  #get the compass heading
    compass = read_xyz(I2Ccompass) #grabs 3 axes, x points forward
    print("compass[0]: ", compass[0], ", compass[1]: ", compass[1]) # x axis
    time.sleep(0.5) #pause for 500ms

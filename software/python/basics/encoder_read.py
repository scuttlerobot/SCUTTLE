import Adafruit_GPIO.I2C as Adafruit_I2C
import time

right_encoder = Adafruit_I2C.Device(0x40,1)
left_encoder  = Adafruit_I2C.Device(0x41,1)

def read_encoders_angle(enc0,enc1):
    try:
        x = enc0.readU16(0xFE)
        x = ((x << 8) | (x >> 8)) & 0xFFFF
        meas = ((x & 0xFF00) >> 2) | ( x & 0x3F)
        angle0 = meas*0.0219
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


while True:
    x = read_encoders_angle(right_encoder,left_encoder)
    print("Left: ",round(x[0],0),"\t","Right: ",round(x[1],0))
    time.sleep(0.1)

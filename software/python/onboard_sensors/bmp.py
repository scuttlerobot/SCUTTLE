# Install required libaries using:
# sudo pip3 install bmp280

#!/usr/bin/env python

import time
from smbus import SMBus #library for accessing i2c devices
from bmp280 import BMP280 #library dedicated to BMP280 sensor

# Initialise the BMP280
bus = SMBus(2) # the sensor is located on the i2c bus no.2
bmp280 = BMP280(i2c_dev=bus)

while True:
    
    temperature = round(bmp280.get_temperature(),2)
    pressure = round(bmp280.get_pressure()*0.1,1)
    altitude = round(bmp280.get_altitude(),1)

    print("Temperature:", temperature, "C\tPressure:", pressure,"kPa\tAltitude:", altitude, "m")
    time.sleep(0.1)

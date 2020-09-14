# This program reads information from the onboard Temperature & Pressure
# sensors on the beaglebone blue. Before running the code, you need to
# install required library using the command:
# sudo pip3 install bmp280

import time
from smbus import SMBus         # library for accessing i2c devices through python
from bmp280 import BMP280       # library dedicated to BMP280 sensor

# Initialize the BMP280
bus = SMBus(2)                  # the sensor is located on the i2c bus no.2
bmp280 = BMP280(i2c_dev=bus)


# get the sensor temp (C)
def temp():
    temperature = round(bmp280.get_temperature(), 2)
    return(temperature)


# get the ambient pressure (kPa)
def pressure():
    pressure = round(bmp280.get_pressure()*0.1, 1)
    return(pressure)


# get the estimated altitude (m) (not calibrated)
# altitude is not reliable unless you know how to calibrate it
def altitude():
    altitude = round(bmp280.get_altitude(), 1)
    return(altitude)


if __name__ == "__main__":
    while True:
        t = temp()
        p = pressure()
        a = altitude()
        print("Temperature: (C)", t, "\t Pressure (kPa):", p)
        time.sleep(0.5)

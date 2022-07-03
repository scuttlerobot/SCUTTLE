# This code is adapted from: github.com/chrisb2/pi_ina219 examples
# This basic code samples voltage and uses auto-ranging.
# WARNING: configure ina sensor for address 0x44. Encoder occupies 0x40.

import time                 # for keeping time
import ina219               # for reading voltage/current sensor
from ina219 import INA219   # sensor library

# Declare relevant variables
SHUNT_OHMS = 10.8 # Measure your shunt with a multimeter & update.

# Set up the INA219 sensor
ina = INA219(SHUNT_OHMS, address = 0x40)
ina.configure()

def read():
    print("Bus Voltage: %.3f V" % ina.voltage())
    try:
        print("Bus Current: %.3f mA" % ina.current())
        print("Power: %.3f mW" % ina.power())
        print("Shunt voltage: %.3f mV" % ina.shunt_voltage())
    except DeviceRangeError as e:
        # Current out of device range with specified shunt resistor
        print(e)

def readVolts():
    volts = round(ina.voltage(),2)
    return volts


if __name__ == "__main__":
    read()
    while True:
        myBatt = round(readVolts(),2)       # collect a reading
        print("Battery Voltage: ",myBatt)   # print the reading
        time.sleep(1)                       # pause

# This basic code samples voltage and uses auto-ranging.
# WARNING: configure ina sensor for address 0x44. Encoder occupies 0x40.

import time                 # for keeping time
from adafruit_ina219 import INA219
import board

# Set up the INA219 sensor
i2c = board.I2C()
ina = INA219(i2c, 0x44)

def read():
    print("Bus Voltage: %.3f V" % ina.bus_voltage)
    try:
        print("Bus Current: %.3f mA" % ina.current)
        print("Power: %.3f mW" % ina.power)
        print("Shunt voltage: %.3f mV" % ina.shunt_voltage)
    except DeviceRangeError as e:
        # Current out of device range with specified shunt resistor
        print(e)

def readVolts():
    volts = round(ina.bus_voltage,2)
    return volts


if __name__ == "__main__":
    read()
    while True:
        myBatt = round(readVolts(),2)       # collect a reading
        print("Battery Voltage: ",myBatt)   # print the reading
        time.sleep(1)                       # pause

# This program runs the INA219 sensor
# and reports on voltage and current 
# and communicates on the i2c bus

# Import external programs
import time
from ina219 import INA219
from ina219 import DeviceRangeError

# Define important parameters
SHUNT_OHMS = 0.1    # only relevant if a shunt resistor is in the circuit
MAX_EXPECTED_AMPS = 0.2


def read():
    ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS)
    ina.configure(ina.RANGE_16V, ina.GAIN_1_40MV)

    print("Bus Voltage: %.3f V" % ina.voltage())
    try:
        print("Bus Current: %.3f mA" % ina.current())
        print("Power: %.3f mW" % ina.power())
        print("Shunt voltage: %.3f mV" % ina.shunt_voltage())
    except DeviceRangeError as e:
        print("Current overflow")

# THIS PORTION ONLY RUNS IF THE PROGRAM IS CALLED DIRECTLY
if __name__ == "__main__":
    read()
    time.sleep(1)

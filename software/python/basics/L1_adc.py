# This code retrieves information from the onboard analog-to-digital converter
# on the beaglebone blue.
# Uses rcpy library.  Documentation at guitar.ucsd.edu/rcpy/rcpy.pdf

# Import External Libraries
import time                 # for handing timing
import numpy as np          # for handling arrays
import rcpy                 # for driving peripherals on beaglebone blue
from rcpy._adc import *     # import functions in rcpy adc


# Define Relevant Functions
# get readings from all channels of onboard ADC.
def getAdc(channel=None):
    if channel is None:
        A0 = round(get_voltage(0), 3)                       # ADC channel 0
        A1 = round(get_voltage(1), 3)                       # ADC channel 1
        A2 = round(get_voltage(2), 3)                       # ADC channel 2
        A3 = round(get_voltage(3), 3)                       # ADC channel 3
        A4 = round(get_voltage(4), 3)                       # ADC channel 4
        A5 = round(get_voltage(5), 3)                       # DC Input (unscaled)
        A6 = round(get_voltage(6), 3)                       # Lipo battery input (unscaled)
        adcData = np.array([A0, A1, A2, A3, A4, A5, A6])
    elif channel >= 0 and channel <= 6:
        adcData = round(get_voltage(channel), 3)            # ADC channel specified by user
    elif channel < 0 and channel > 6:
        print("ERROR: Invalid ADC Channel!")
        adcData = None
    return(adcData)


# return the voltage measured at the barrel plug
def getDcJack():
    voltage = round(get_dc_jack_voltage(), 2)
    return (voltage)


if __name__ == "__main__":
    while True:
        adcData = getAdc()
        dcJack = getDcJack()
        print("adc (v):", adcData, "\t battery (v):", dcJack)
        time.sleep(0.5)

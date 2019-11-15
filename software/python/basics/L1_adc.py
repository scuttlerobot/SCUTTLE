# This code retrieves information from the onboard analog-to-digital converter
# on the beaglebone blue.
# Uses rcpy library.  Documentation at guitar.ucsd.edu/rcpy/rcpy.pdf

# Import External Libraries
import time # for handing timing
import numpy as np # for handling arrays
import rcpy # library for driving several peripherals on beaglebone blue
from rcpy._adc import *  # this allows functions from rcpy adc to be called directly

# Define Relevant Functions
def getAdc():  # get readings from all channels of onboard ADC.
    A0 = round(get_voltage(0),3)    # ADC channel 0 
    A1 = round(get_voltage(1),3)    # ADC channel 1 
    A2 = round(get_voltage(2),3)    # ADC channel 2 
    A3 = round(get_voltage(3),3)    # ADC channel 3 
    A4 = round(get_voltage(4),3)    # ADC channel 4 
    A5 = round(get_voltage(5),3)    # DC Input (unscaled)
    A6 = round(get_voltage(6),3)    # Lipo battery input (unscaled)
    adcData = np.array([A0, A1, A2, A3, A4, A5, A6])
    # nicely formatted print statement below
    #print("\nA0:",A0, "\nA1:",A1, "\nA2:", A2, "\nA3:", A3, "\nA4:", A4, "\nA5:", A5, "\nA6:", A6)
    return(adcData)

def getDcJack(): # return the voltage measured at the barrel plug
    voltage = round(get_dc_jack_voltage(), 2)
    return (voltage)

# # UNCOMMENT THE SECTION BELOW TO RUN AS STANDALONE CODE    
# while 1:
#     adcData = getAdc()
#     dcJack = getDcJack()
#     print("adc (v):", adcData, "\t battery (v):", dcJack)
#     time.sleep(0.5)

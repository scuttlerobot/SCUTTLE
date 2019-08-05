# This code retrieves information from the onboard analog-to-digital converter
# on the beaglebone blue

import time
import numpy as np
import rcpy
from rcpy._adc import *


def getAdc():
    A0 = round(get_voltage(0),3)    # ADC channel 0 
    A1 = round(get_voltage(1),3)    # ADC channel 1 
    A2 = round(get_voltage(2),3)    # ADC channel 2 
    A3 = round(get_voltage(3),3)    # ADC channel 3 
    A4 = round(get_voltage(4),3)    # ADC channel 4 
    A5 = round(get_voltage(5),3)    # DC Input
    A6 = round(get_voltage(6),3)    # Lipo battery input
    adcData = np.array([A0, A1, A2, A3, A4, A5, A6])
    print("\nA0:",A0, "\nA1:",A1, "\nA2:", A2, "\nA3:", A3, "\nA4:", A4, "\nA5:", A5, "\nA6:", A6)
    return(adcData)
    
while 1:
    myAdcData = getAdc()
    print (myAdcData)
    time.sleep(0.1)

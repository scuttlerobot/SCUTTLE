#This example takes a data point from the ultrasonic sensor (HC-SR04)
# and prints the data point, then repeats.

import Adafruit_BBIO.GPIO as GPIO
import time
import signal

echo_pin = 'P9_23'
trig_pin = 'GP0_3'
GPIO.setup(echo_pin, GPIO.IN)
GPIO.setup(trig_pin, GPIO.OUT)

def distanceMeasurement(TRIG,ECHO):
    pulseEnd = 0
    pulseStart = time.time()
    GPIO.output(TRIG, True)
    time.sleep(0.0001)
    GPIO.output(TRIG, False)

    while (GPIO.input(ECHO) == 0):# and (time.time()-pulseStart < 1):
        pulseStart = time.time()
    while GPIO.input(ECHO) == 1:
        pulseEnd = time.time()

    pulseDuration = pulseEnd - pulseStart
    #print pulseEnd- pulseStart
    distance = pulseDuration * 17150
    distance = round(distance, 2)
    return distance

while True:
    recoveredDistance = distanceMeasurement(trig_pin, echo_pin)
    print ("Distance: ", recoveredDistance, "cm")
    time.sleep(0.1)

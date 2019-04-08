import Adafruit_BBIO.GPIO as GPIO
import time
import signal

echo_pin = 'P9_28' # GPIO1_17 actual name on BB Black
trig_pin = 'GPIO1_25' # name on board diagram
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



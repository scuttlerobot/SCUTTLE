import time
import RPi.GPIO as GPIO

r_wheel_pin = 32      # Right wheel
l_wheel_pin = 33      # Left wheel

r_dir_pin = 18
l_dir_pin = 16

r_wheel_dir = 0
l_wheel_dir = 0

GPIO.setmode(GPIO.BOARD)

GPIO.setup(r_wheel_pin, GPIO.OUT)
GPIO.setup(l_wheel_pin, GPIO.OUT)
GPIO.setup(r_dir_pin, GPIO.OUT)
GPIO.setup(l_dir_pin, GPIO.OUT)

r_wheel = GPIO.PWM(r_wheel_pin, 500)  # channel=pin frequency=50Hz
l_wheel = GPIO.PWM(l_wheel_pin, 500)  # channel=pin frequency=50Hz

r_wheel.start(0)
l_wheel.start(0)

try:

    while 1:

        GPIO.output(r_dir_pin, r_wheel_dir)
        GPIO.output(l_dir_pin, l_wheel_dir)

        r_wheel.ChangeDutyCycle(100)
        l_wheel.ChangeDutyCycle(100)

        time.sleep(0.1)

except KeyboardInterrupt:
    pass

r_wheel.stop()
l_wheel.stop()

GPIO.cleanup()

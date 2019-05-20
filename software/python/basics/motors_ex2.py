import time
import RPi.GPIO as GPIO

r_wheel_pin = 32      # Right wheel pwm pin
l_wheel_pin = 33      # Left wheel pwm pin

r_dir_pin = 18        # Right Wheel direction pin
l_dir_pin = 16        # Left Wheel direction pin

r_wheel_dir = 0     # 0 = LOW, 1 = HIGH
l_wheel_dir = 0

GPIO.setmode(GPIO.BOARD)    #Tells RPi how to interperet pin names

GPIO.setup(r_wheel_pin, GPIO.OUT)   # Set outputs
GPIO.setup(l_wheel_pin, GPIO.OUT)
GPIO.setup(r_dir_pin, GPIO.OUT)
GPIO.setup(l_dir_pin, GPIO.OUT)

r_wheel = GPIO.PWM(r_wheel_pin, 500)  # channel=pin frequency=50Hz
l_wheel = GPIO.PWM(l_wheel_pin, 500)  # channel=pin frequency=50Hz

r_wheel.start(0)    # Start PWM at 0%
l_wheel.start(0)

try:

    while 1:

        GPIO.output(r_dir_pin, r_wheel_dir)     # Set digital pin
        GPIO.output(l_dir_pin, l_wheel_dir)

        r_wheel.ChangeDutyCycle(100)     #Set PWM
        l_wheel.ChangeDutyCycle(100)

        time.sleep(0.1)

except KeyboardInterrupt:
    pass

r_wheel.stop()  # Stop PWM
l_wheel.stop()

GPIO.cleanup()

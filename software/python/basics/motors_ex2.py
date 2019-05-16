# # A barebones example code to operate motors on the SCUTTLE robot.
# # Uses Pi hardware.
#
# import RPi.GPIO as io
# import time
# io.setmode(io.BOARD)
#
# #        GPIO Define PWM, Direction
#
# dir_l = 11	# Left Motors Direction
# dir_r = 13	# Right Motors Direction
#
# pwm_l_pin = 12	# Left Motors PWM - drives mot.driver pin
# pwm_r_pin = 21	# Right Motors PWM
#
# #        Digital pwms Setup
#
# io.setup(dir_l,io.OUT)
# io.setup(dir_r,io.OUT)
#
# #        Analog pwms Setup
#
# io.setup(pwm_l_pin, io.OUT)
# io.setup(pwm_r_pin, io.OUT)
#
# pwm_l = io.PWM(pwm_l_pin, 1000)     # set Frequece to 1KHz
# pwm_r = io.PWM(pwm_r_pin, 1000)     # set Frequece to 1KHz
#
#
# while 1:
#
#     io.output(dir_r,0)
#     io.output(dir_l,0)
#
#     pwm_l.ChangeDutyCycle(10)     # Change duty cycle percentage
#     pwm_r.ChangeDutyCycle(0)     # Change duty cycle percentage

#temporarily use an example "fade" program

import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

p = GPIO.PWM(12, 500)  # channel=12 frequency=50Hz
p.start(0)
try:
    while 1:
        for dc in range(0, 101, 5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
        for dc in range(100, -1, -5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
except KeyboardInterrupt:
    pass
p.stop()
GPIO.cleanup()

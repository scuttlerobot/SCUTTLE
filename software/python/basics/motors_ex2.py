# A barebones example code to operate motors on the SCUTTLE robot.
# Uses Pi hardware.

import RPi.GPIO as io
import time
io.setmode(io.BOARD)

#        GPIO Define PWM, Direction

dir_l = 11	# Left Motors Direction
dir_r = 13	# Right Motors Direction

pwm_l_pin = 19	# Left Motors PWM - drives mot.driver pin 
pwm_r_pin = 21	# Right Motors PWM

#        Digital pwms Setup

io.setup(dir_l,io.OUT)
io.setup(dir_r,io.OUT)

#        Analog pwms Setup

io.setup(pwm_l_pin, io.OUT)
io.setup(pwm_r_pin, io.OUT)

pwm_l = io.PWM(pwm_l_pin, 1000)     # set Frequece to 1KHz
pwm_r = io.PWM(pwm_r_pin, 1000)     # set Frequece to 1KHz


while 1:

    io.output(dir_r,1)
    io.output(dir_l,1)

    pwm_l.ChangeDutyCycle(0)     # Change duty cycle
    pwm_r.ChangeDutyCycle(0)     # Change duty cycle

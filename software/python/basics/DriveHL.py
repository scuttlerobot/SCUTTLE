# this program demonstrates importing of other python files and
# calling functions from child files.

import motors_ex2 as m #module calculates PWM commands
import encoder_ex2 as enc
import time

try:
    while 1:
        # verify encoders are working
        encoderValues = enc.read()
        print("left encoder reads", encoderValues[0])
        print("right encoder reads", encoderValues[1])
        # verify motors are working
        m.MotorL(0.3)
        m.MotorR(0.3)
        time.sleep(2)
        m.MotorL(-0.3)
        m.MotorR(-0.3)
        time.sleep(2)
        # verify gamepad is working

except KeyboardInterrupt:
    pass

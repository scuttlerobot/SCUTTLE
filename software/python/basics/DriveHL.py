# this program demonstrates importing of other python files and
# calling functions from child files.
# last updated 2019.05.23

import motors_ex2 as m #module calculates PWM commands
import encoder_ex2 as enc # for encoders
import gamepad_ex1 as gp #for gamepad
import time
import numpy as np # for handling matrices

m.MotorL(0)
m.MotorR(0)
axes = np.zeros(4)
try:
    while 1:
        # verify encoders are working
        encoderValues = enc.read()
        #print("left encoder reads", encoderValues[0])
        #print("right encoder reads", encoderValues[1])
        # verify motors are working
        update = gp.getGP() #when there is no controller input, update is empty
        try:                      # when update has no data, update.size DNE
            if update.size == 4:  # if update has data, store it to axes
                axes = update
        except:
            pass
        #right = axes[0][0]
        mySpeed = -1*axes[1];

        print("speed axis reads ", mySpeed)
        m.MotorL(mySpeed)
        m.MotorR(mySpeed)
        # time.sleep(2)
        # m.MotorL(-0.3)
        # m.MotorR(-0.3)
        time.sleep(0.1)
        # verify gamepad is working

except KeyboardInterrupt:
    pass

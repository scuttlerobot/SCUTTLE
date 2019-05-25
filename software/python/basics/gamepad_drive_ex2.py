import time
import numpy as np
import motors_ex2 as m #module calculates PWM commands
import gamepad_ex2 as gp #for gamepad

def set_motors(L,R):
    m.MotorL(L)
    m.MotorR(R)

set_motors(0,0)
axes = np.zeros(4)

try:
    while 1:
        update = gp.getGP() #when there is no controller input, update is empty
        # print(update)
        # if update.size == 4:  # if update has data, store it to axes
        axes = update
        # mySpeed = -1*axes[1]

        set_motors(-1*axes[1],-1*axes[3])


        time.sleep(0.1)
        # verify gamepad is working

except KeyboardInterrupt:
    pass

import time
import numpy as np
import motors_ex2 as m #module calculates PWM commands
import gamepad_ex2 as gp #for gamepad

m.MotorL(0)
m.MotorR(0)
axes = np.zeros(4)

def set_motors(L,R):
    m.MotorL(L)
    m.MotorR(R)

try:
    while 1:
        update = gp.getGP() #when there is no controller input, update is empty
        try:                      # when update has no data, update.size DNE
            if update.size == 4:  # if update has data, store it to axes
                axes = update
        except:
            pass

        print(axes)

        time.sleep(0.1)
        # verify gamepad is working

except KeyboardInterrupt:
    pass

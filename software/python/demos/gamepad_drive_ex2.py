import time
import numpy as np
import motors_ex2 as m #module calculates PWM commands
import gamepad_ex2 as gp #for gamepad

def set_motors(L,R):
    m.MotorL(L)
    m.MotorR(R)

set_motors(0,0)
axes = np.zeros(4)

duty_l = 0 # initialize motor with zero duty cycle
duty_r = 0 # initialize motor with zero duty cycle

try:
    while 1:
        update = gp.getGP() #when there is no controller input, update is empty

        l_joy_x = update[0]
        l_joy_y = update[1]

        # Calculate Left and Right Wheel Duty Cycles

        duty_r = ((-1*(l_joy_x))-l_joy_y)
        duty_l = (    (l_joy_x) -l_joy_y)

        # Set wheel duty cycles between -1 and 1 if calculated is outside range.

        if duty_l > 1:

            duty_l = 1

        if duty_r > 1:

            duty_r = 1

        if duty_l < -1:

            duty_l = -1

        if duty_r < -1:

            duty_r = -1

        set_motors(duty_l,duty_r)

        time.sleep(0.1)

except KeyboardInterrupt:
    pass

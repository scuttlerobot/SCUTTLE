# this program demonstrates importing of other python files and
# calling functions from child files.
# last updated 2019.05.23

import motors_ex2 as m #module calculates PWM commands
import encoder_ex2 as enc # for encoders
import gamepad_ex2 as gp #for gamepad
import time
import numpy as np # for handling matrices

m.MotorL(0)
m.MotorR(0)
axes = np.zeros(4)

# generate_duty is a placeholder function for the inverse kinematics program
def generate_duty(x_dot,theta_dot):
        # Calculate Left and Right Wheel Duty Cycles
    duty_r = ((  1 * (theta_dot)) + x_dot )
    duty_l = (( -1 * (theta_dot))  + x_dot )
    duties = np.array([ duty_l, duty_r ])
    return duties

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

        # assign axes grom gamepad to requested velocities
        x_dot = -1*axes[1] # times -1 so forward gives positive
        theta_dot = -1*axes[0]
        #generate duty cycles
        duties = generate_duty(x_dot, theta_dot)
        duties[0] = sorted([-1, duties[0], 1])[1] # place bounds on duty cycle
        duties[1] = sorted([-1, duties[1], 1])[1] # place bounds on duty cycle
        print("x dot: ", x_dot)
        m.MotorL(duties[0]) # fcn allows -1 to 1
        m.MotorR(duties[1]) # fcn allows -1 to 1
        # time.sleep(2)
        # m.MotorL(-0.3)
        # m.MotorR(-0.3)
        time.sleep(0.1)
        # verify gamepad is working

except KeyboardInterrupt:
    pass

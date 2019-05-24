# this program demonstrates importing of other python files and
# calling functions from child files.
# last updated 2019.05.23

import motors_ex2 as m #module calculates PWM commands
import encoder_ex2 as enc # for encoders
import gamepad_ex2 as gp #for gamepad
import time
import numpy as np # for handling matrices
import text2speech_ex2 as t2s #for speaking by aux port
import threading # only used for threading functions

m.MotorL(0)
m.MotorR(0)
axes = np.zeros(16) #number of elements returned by gamepad

# generate_duty is a placeholder function for the inverse kinematics program
def generate_duty(x_dot,theta_dot):
    # Calculate Left and Right Wheel Duty Cycles
    duty_r = ((  1 * (theta_dot)) + x_dot )
    duty_l = (( -1 * (theta_dot))  + x_dot )
    duties = np.array([ duty_l, duty_r ])
    return duties

def loop_speak( ID ):
    while(1):
        myStringA = "hello everybody I'm a multi-threading scuttle"
        myStringX = "you pressed X!"
        myStringB = "firing the missiles"
        signals = gp.getGP()
        if signals[6]==1: # A button is pressed
            t2s.say(myStringA)
        if signals[7]==1: # x button is pressed
            t2s.say(myStringX)
        if signals[5]==1: # x button is pressed
            t2s.say(myStringB)
        time.sleep(0.1)

def loop_drive( ID ):
    while(1):
            # verify motors are working
            update = gp.getGP() #when there is no controller input, update is empty
            try:                      # when update has no data, update.size DNE
                if update.size == 16:  # if update has data, store it to axes
                    axes = update
                    print("update size :", update.size)
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

            time.sleep(0.1)


def main():
        print("starting the main fcn")
        threads = []

        t = threading.Thread( target=loop_speak, args=(1,) )
        threads.append(t)
        t.start()
        print("started thread1")
        t2 = threading.Thread( target=loop_drive, args=(2,) )
        threads.append(t2)
        t2.start()
        print("started thread2")
        t.join()
        t2.join()

main()
        # verify encoders are working
        #encoderValues = enc.read()  # creates an array of 2 values

        # TEMPORARILY MOVED TO LOOP-DRIVE TO TRY THREADING
        # # verify motors are working
        # update = gp.getGP() #when there is no controller input, update is empty
        # try:                      # when update has no data, update.size DNE
        #     if update.size == 16:  # if update has data, store it to axes
        #         axes = update
        #         print("update size :", update.size)
        # except:
        #     pass
        #
        # # assign axes grom gamepad to requested velocities
        # x_dot = -1*axes[1] # times -1 so forward gives positive
        # theta_dot = -1*axes[0]
        # #generate duty cycles
        # duties = generate_duty(x_dot, theta_dot)
        # duties[0] = sorted([-1, duties[0], 1])[1] # place bounds on duty cycle
        # duties[1] = sorted([-1, duties[1], 1])[1] # place bounds on duty cycle
        # print("x dot: ", x_dot)
        # m.MotorL(duties[0]) # fcn allows -1 to 1
        # m.MotorR(duties[1]) # fcn allows -1 to 1

        # TEMPORARILY MOVED TO LOOP-SPEAK TO TRY THREADING.
        # myString = "I am SCUTTLE robot."
        # if axes[6]==1:
        #     t2s.say(myString)

        #time.sleep(0.1)

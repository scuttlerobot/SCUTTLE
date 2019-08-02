# speed_control.py takes target speeds and generates duty cycles
# to send to motors, and will perform PID control (when finalized)

import motors_ex1 as m
import numpy as np
import time
import log


# THE FOLLOWING FUNCTION PAIR IS FOR BOTH MAPPING AND DRIVING BY THETA & # X
# DO NOT USE THIS SECTION UNLESS INVERSE KINEMATICS IS BROKEN.
#----------------------------------------------------------------------------
# generate_duty is a placeholder function for the inverse kinematics program
u_integral = 0
def generate_duty(x_dot,theta_dot):
    # Calculate Left and Right Wheel Duty Cycles
    duty_r = ((  1 * (theta_dot)) + x_dot )
    duty_l = (( -1 * (theta_dot))  + x_dot )
    duties = np.array([ duty_l, duty_r ])   # put the values into an array
    duties[0] = sorted([-1, duties[0], 1])[1] # place bounds on duty cycle
    duties[1] = sorted([-1, duties[1], 1])[1] # place bounds on duty cycle
    return duties

def drive(x_dot, theta_dot):
    duties = generate_duty(x_dot, theta_dot)
    m.MotorL(duties[0]) # fcn allows -1 to 1
    m.MotorR(duties[1]) # fcn allows -1 to 1

# THE FOLLOWING FUNCTION PAIR IS FOR BOTH MAPPING AND DRIVING BY pdl & pdr targets
#----------------------------------------------------------------------------
# a function for converting target rotational speeds to PWMs without feedback
def openLoop(pdl,pdr):
    DRS = 0.8   # create a variable for direct-re-scaling
    duty_l = pdl * 1/9.75 * DRS  # 1 is max voltage and 9.75 is max rad/s possible
    duty_r = pdr * 1/9.75 * DRS  #
    duties = np.array([ duty_l, duty_r ])   # put the values into an array
    duties[0] = sorted([-1, duties[0], 1])[1] # place bounds on duty cycle
    duties[1] = sorted([-1, duties[1], 1])[1] # place bounds on duty cycle
    return duties

def driveOpenLoop(dutyl,dutyr,pdc):
    duties = openLoop(dutyl,dutyr)
    log.duty_speed(duties[0], pdc[0])
    print("Left:", duties[0],"\t Right:", duties[1])
    m.MotorL(duties[0])
    m.MotorR(duties[1])

def Deadzone(dd):
    dd = (dd * 3)
    return dd

def Nonedeadzone(dn):
    dn = ((dn * 0.7778) + 0.2222)
    return dn


def driveClosedLoop(pdt, pdc):
    #print(pdt[0],'  ',pdc[0])
    #calculate the error
    global u_integral

    e = (pdt - pdc)

    #print("EL value",eL,'  ',"Target Speed L:",pdt[0],'  ',"Current Speed L:",pdc[0],'--------'"ER value",eR,'  ',"Target Speed L:",pdt[1],'  ',"Current Speed L:",pdc[1])

    # e_max = 9.7 #r/s        #define e_max
    # u_max = 1.0 #duty       #define u_max
    # kp = np.round(u_max/e_max, decimals=3) #calculate the kp value  #This gives you a Kp of 2.5
    #kp = 1.0/9.7
    kp = 0.07 #variable Kp
    #original was kp = 0.06 and ki = 0.0012
    ki = 0.011
    #kd = 0.08
    #multiply the k by the error to get U_poroportional
    u_proportional = (e * kp)    #will re-define later, u is just the control signal
    u_integral    += (e * ki)
    #u_derivative += (e / dt)

    #u = u_proportional
    u = np.round((u_proportional + u_integral),3) # round to ensure driver handling

    # u = u_proportional + (kd * u_derivative)
    # u = u_proportional + (ki * u_integral) + (kd * u_derivative)

    dutyL = u[0]  #sort u_proportional equal to duty
    dutyR = u[1]
    dutyL = sorted([-1,dutyL,1])[1]
    dutyR = sorted([-1,dutyR,1])[1]

    m.MotorL(round(dutyL,2))
    m.MotorR(round(dutyR,2))
    #print("left:", dutyL, "\t right:", dutyR)
    # if (dutyL < 0.2):
    #     pwmL = Deadzone(dutyL)
    #     m.MotorL(pwmL)
    #     print(pwmL)
    #     #print(pwmL)
    # if (dutyR < 0.2):
    #     pwmR = Deadzone(dutyR)
    #     m.MotorR(pwmR)
    #     #print(pwmR)
    # if (dutyL > 0.2):
    #     pwmL = Nonedeadzone(dutyL)
    #     m.MotorL(pwmL)
    #     print(pwmL)
    # if (dutyR > 0.2):
    #     pwmR = Nonedeadzone(dutyR)
    #     m.MotorR(pwmR)
    #     #print(pwmR)
    log.controlsignal(u_proportional, u_integral)
    #log.error(pdt,pdc)


    

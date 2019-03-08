import rcpy
import rcpy.motor as motor

#   Motor Controller Settings

Motor_L = 1  # left motor connects to output 1
Motor_R = 2  # right motor connects to output 2

#   Motor Controller

def set_speed(speedL, speedR): #in one function, cmd both motor driver channels

    motor.set(Motor_L, ((speedL-127)/127))  #h bridge commands
    motor.set(Motor_R, ((speedR-127)/127))

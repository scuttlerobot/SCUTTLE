import rcpy
import rcpy.motor as motor

motor_r = 2 	# Right Motor
motor_l = 1 	# Left Motor

rcpy.set_state(rcpy.RUNNING)

while rcpy.get_state() != rcpy.EXITING:

    if rcpy.get_state() == rcpy.RUNNING:

        duty_l = 1
        duty_r = -1

        motor.set(motor_l, duty_l)
        motor.set(motor_r, duty_r)

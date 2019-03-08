import rcpy
import rcpy.motor as motor

#   Motor Controller Settings

Motor_L = 1  # left motor connects to output 1
Motor_R = 2  # right motor connects to output 2



#   Motor Controller

def set_speed(speedL, speedR): #in one function, cmd both motor driver channels

    motor.set(Motor_L, ((speedL-127)/127))  #h bridge commands
    motor.set(Motor_R, ((speedR-127)/127))

#       Turning Function

def turn(angle=None,mode=None,speed=30,direction=None):

    turn = True

    rcpy.set_state(rcpy.RUNNING)

    mpu9250.initialize(enable_dmp = True)

    while turn:

        if rcpy.state() == rcpy.RUNNING:

            imu_data = mpu9250.read()   # Read Data from Sensors
            imu = imu_data['tb']        # Get imu Value and Convert to Degrees (0 to 180 , -180 to 0)
            imu_deg = (math.degrees(round(imu[2],2))) % 360

            angle = angle % 360

            if mode == "point" or mode == None:

                if angle == 0:

                    data_l = [146, 32]  # Brake
                    data_r = [146, 32]

                # Check Angle is from 0 to 180 or 180 to 360, to determine which direction to turn

                elif 0 < angle and 180 > angle:   # If converted angle is between 0 and 180, point turn counter-clockwise

                    data_l = [255, 0, 128 - speed]  #   Rotate Left
                    data_r = [255, 1, 128 + speed]

                elif 180 < angle and 360 > angle:   # If converted angle is between 180 and 360, point turn clockwise

                    data_l = [255, 0, 128 + speed]  #   Rotate Right
                    data_r = [255, 1, 128 - speed]

            if (imu_deg-2) <= angle and angle <= (imu_deg+2):   # Once Angle is within Range Stop Motors

                data_l = [146, 32]      # Brake
                data_r = [146, 32]

            elif mode == "swing":

                if direction == "forward":

                    if angle == 0:

                        data_l = [146, 32]  # Brake
                        data_r = [146, 32]

                    # Check Angle is from 0 to 180 or 180 to 360, to determine which direction to turn

                    elif 0 < angle and 180 > angle:   # If converted angle is between 0 and 180, point turn counter-clockwise

                        data_l = [255, 0, 128]  #   Rotate Left
                        data_r = [255, 1, 128 + speed]

                    elif 180 < angle and 360 > angle:   # If converted angle is between 180 and 360, point turn clockwise

                        data_l = [255, 0, 128 + speed]  #   Rotate Right
                        data_r = [255, 1, 128]

                if (imu_deg-2) <= angle and angle <= (imu_deg+2):   # Once Angle is within Range Stop Motors

                    data_l = [146, 32]      # Brake
                    data_r = [146, 32]

                elif direction == "backward":

                    if angle == 0:

                        data_l = [146, 32]  # Brake
                        data_r = [146, 32]

                    # Check Angle is from 0 to 180 or 180 to 360, to determine which direction to turn

                    elif 0 < angle and 180 > angle:   # If converted angle is between 0 and 180, point turn counter-clockwise

                        data_l = [255, 0, 128 - speed]  #   Rotate Left
                        data_r = [255, 1, 128]

                    elif 180 < angle and 360 > angle:   # If converted angle is between 180 and 360, point turn clockwise

                        data_l = [255, 0, 128]  #   Rotate Right
                        data_r = [255, 1, 128 - speed]

                if (imu_deg-2) <= angle and angle <= (imu_deg+2):   # Once Angle is within Range Stop Motors

                    data_l = [146, 32]      # Brake
                    data_r = [146, 32]

                else:

                    continue

                ser_motor.write(data_l)     # Send Data to Motor Controllers
                ser_motor.write(data_r)

        data_l = [146, 32]  # Brake
        data_r = [146, 32]

        ser_motor.write(data_l)     # Send Data to Motor Controllers
        ser_motor.write(data_r)

        turn = False

        print("Done!")

        pass

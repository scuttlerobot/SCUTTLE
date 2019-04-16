#!/usr/bin/env python3
# import python libraries
import time
import getopt, sys

# import rcpy library
# This automatically initizalizes the robotics cape
import rcpy
import rcpy.mpu9250 as mpu9250

def main():

    # defaults
    enable_magnetometer = False
    show_compass = False
    show_gyro = False
    show_accel = False
    show_quat = False
    show_tb = False
    sample_rate = 100
    enable_fusion = False
    show_period = False
    newline = '\r'

    show_tb = True

    # set state to rcpy.RUNNING
    rcpy.set_state(rcpy.RUNNING)

    # magnetometer ?
    mpu9250.initialize(enable_dmp=True,
                       dmp_sample_rate=sample_rate,
                       enable_fusion=enable_fusion,
                       enable_magnetometer=enable_magnetometer)

    try:

        # keep running
        while True:

            # running
            if rcpy.get_state() == rcpy.RUNNING:

                t0 = time.perf_counter()
                data = mpu9250.read()
                t1 = time.perf_counter()
                dt = t1 - t0
                t0 = t1

                print(data)
#                print('{0[0]:6.2f} {0[1]:6.2f} {0[2]:6.2f} |'
#                          .format(data['tb']), end='')

                # no need to sleep

    except KeyboardInterrupt:
        # Catch Ctrl-C
        pass

    finally:

        # say bye
        print("\nBye Beaglebone!")

# exiting program will automatically clean up cape

if __name__ == "__main__":
    main()

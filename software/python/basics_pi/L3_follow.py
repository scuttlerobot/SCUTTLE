# This is a demo for following a colored object

# Import internal programs
import L2_track_target as track
import L2_speed_control as sc
import L2_inverse_kinematics as inv

# Import external programs
import time         # keeping time
import numpy as np  # for handling matrices

# THIS SECTION ONLY RUNS IF THE PROGRAM IS CALLED DIRECTLY
if __name__ == "__main__":
    while True:
        target = track.colorTarget(track.color_range) # generate a target
        if target[0] is None:
            print("no target located.")
        else:
            x_range = track.getAngle(target[0])   # find out the angle of the target
            print("Target x location: ", x_range)
            chassisTargets = inv.map_speeds(np.array([0, x_range])) # generate xd, td
            pdTargets = inv.convert(chassisTargets) # pd means phi dot (rad/s)
            sc.driveOpenLoop(pdTargets)     
        time.sleep(0.1) # short delay
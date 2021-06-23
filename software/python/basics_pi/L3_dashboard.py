<<<<<<< HEAD
# L3_dashboard.py
# This program grabs data from the onboard sensors and logs data in files
# for NodeRed access and integrate into a custom flow titled "dashboard".
# Access nodered at your.ip.address:1880

# v2021.05.14 DPM

# Import External programs
import numpy as np
import time

# Import Internal Programs
import L1_gamepad as gp
import L1_log as log
import L2_inverse_kinematics as inv
import L2_kinematics as kin
import L2_speed_control as sc

# Run the main loop
while True:
        
    # # DISPLAY BATTERY LEVEL
    # vb = adc.getDcJack()
    # log.tmpFile(vb,"vb.txt")
    
    # COLLECT GAMEPAD COMMANDS
    gp_data = gp.getGP()
    axis0 = gp_data[0] * -1
    axis1 = gp_data[1] * -1
    rthumb = gp_data[3] # up/down axis of right thumb
    horn = gp_data[4]   # "y" button
    stride = gp_data[5] # "B" button
    
    
    # HORN FUNCTION
    # the horn is connected by relay to port 1 pin 0 (relay 1 of 2)
    # print("horn button:", horn)
    # if horn:
    #     gpio.write(1, 0, 1) # write HIGH
    #     time.sleep(0.30) # actuate for just 0.2 seconds
    #     gpio.write(1, 0, 0) # write LOW
    # #print("rthumb axis:", rthumb)

    # STRIDE FUNCTION (in progress 05.29)
    # press the "B" button to closed-loop drive fwd 50cm
    # if stride:
    #     print("executing stride")
    #     timerStart = time.monotonic()
    #     while timer < 2:                     # stride for 2 seconds
    #         pdc = kin.getPdCurrent()        # get Phi Dots
    #         sc.driveClosedLoop(0.3, pdc, 0) # pdt, pdc, de_dt
    #         time.sleep(0.050)               # actuate for just 50 miliseconds
    #         timer = time.monotonic() - timerStart 
    #     print("finished stride")

    
    # USE KINEMATICS TO MEASURE WHEEL SPEEDS
    phiDots = kin.getPdCurrent()
    myString = str(round(phiDots[0],1)) + "," + str(round(phiDots[1],1))
    log.stringTmpFile(myString,"phidots.txt")

    # GET THE GAMEPAD SIGNALS
    myString = str(round(axis0*100,1)) + "," + str(round(axis1*100,1))
    log.stringTmpFile(myString,"uFile.txt")
    print("Gamepad, xd: " ,axis1, " td: ", axis0) # print gamepad percents
    
    # DRIVE IN OPEN LOOP
    chassisTargets = inv.map_speeds(np.array([axis1, axis0])) # generate xd, td
    pdTargets = inv.convert(chassisTargets) # pd means phi dot (rad/s)
    # phiString = str(pdTargets[0]) + "," + str(pdTargets[1])
    # print("pdTargets (rad/s): \t" + phiString)
    # log.stringTmpFile(phiString,"pdTargets.txt")
    
    #DRIVING
    sc.driveOpenLoop(pdTargets) #call driving function 
    #servo.move1(rthumb) # control the servo for laser
    time.sleep(0.05)
=======
# L3_dashboard.py
# This program grabs data from the onboard sensors and logs data in files
# for NodeRed access and integrate into a custom flow titled "dashboard".
# Access nodered at your.ip.address:1880

# v2021.05.14 DPM

# Import External programs
import numpy as np
import time

# Import Internal Programs
import L1_gamepad as gp
import L1_log as log
import L2_inverse_kinematics as inv
import L2_kinematics as kin
import L2_speed_control as sc

# Run the main loop
while True:
        
    # # DISPLAY BATTERY LEVEL
    # vb = adc.getDcJack()
    # log.tmpFile(vb,"vb.txt")
    
    # COLLECT GAMEPAD COMMANDS
    gp_data = gp.getGP()
    axis0 = gp_data[0] * -1
    axis1 = gp_data[1] * -1
    rthumb = gp_data[3] # up/down axis of right thumb
    horn = gp_data[4]   # "y" button
    stride = gp_data[5] # "B" button
    
    
    # HORN FUNCTION
    # the horn is connected by relay to port 1 pin 0 (relay 1 of 2)
    # print("horn button:", horn)
    # if horn:
    #     gpio.write(1, 0, 1) # write HIGH
    #     time.sleep(0.30) # actuate for just 0.2 seconds
    #     gpio.write(1, 0, 0) # write LOW
    # #print("rthumb axis:", rthumb)

    # STRIDE FUNCTION (in progress 05.29)
    # press the "B" button to closed-loop drive fwd 50cm
    # if stride:
    #     print("executing stride")
    #     timerStart = time.monotonic()
    #     while timer < 2:                     # stride for 2 seconds
    #         pdc = kin.getPdCurrent()        # get Phi Dots
    #         sc.driveClosedLoop(0.3, pdc, 0) # pdt, pdc, de_dt
    #         time.sleep(0.050)               # actuate for just 50 miliseconds
    #         timer = time.monotonic() - timerStart 
    #     print("finished stride")

    
    # USE KINEMATICS TO MEASURE WHEEL SPEEDS
    phiDots = kin.getPdCurrent()
    myString = str(round(phiDots[0],1)) + "," + str(round(phiDots[1],1))
    log.stringTmpFile(myString,"phidots.txt")

    # GET THE GAMEPAD SIGNALS
    myString = str(round(axis0*100,1)) + "," + str(round(axis1*100,1))
    log.stringTmpFile(myString,"uFile.txt")
    print("Gamepad, xd: " ,axis1, " td: ", axis0) # print gamepad percents
    
    # DRIVE IN OPEN LOOP
    chassisTargets = inv.map_speeds(np.array([axis1, axis0])) # generate xd, td
    pdTargets = inv.convert(chassisTargets) # pd means phi dot (rad/s)
    # phiString = str(pdTargets[0]) + "," + str(pdTargets[1])
    # print("pdTargets (rad/s): \t" + phiString)
    # log.stringTmpFile(phiString,"pdTargets.txt")
    
    #DRIVING
    sc.driveOpenLoop(pdTargets) #call driving function 
    #servo.move1(rthumb) # control the servo for laser
    time.sleep(0.05)
>>>>>>> 19b28fe1f166134d486ef440a8f7e9f5030f72d6

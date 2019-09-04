# Level 3 program for driving SCUTTLE and handling other tasks in parallel

# IMPORT EXTERNAL ITEMS
import time
import numpy as np # for handling matrices
import threading # only used for threading functions
import math

# IMPORT INTERNAL ITEMS
import L2_speed_control as sc # closed loop control. Import speed_control for open-loop
import L2_inverse_kinematics as inv #calculates wheel parameters from chassis
import L2_kinematics as kin    # calculates chassis parameters from wheels
import L2_log as log # log live data to local files
# import L2_obstacle as obs  # for detecting obstacles
# import L2_color_target as ct # for driving with computer vision tracking
import L1_text2speech as t2s # for speaking over aux port
import L1_gamepad as gp # for accessing gamepad directly
import L1_encoder as enc # for accessing encoders directly
import L1_bmp as bmp # for accessing bmp sensor onboard
import L1_adc as adc # for accessing adc sensor onboard
import L1_rssi as rssi # for accessing rssi value


# CREATE A THREAD FOR SPEAKING
def loop_speak( ID ):
    myStringA = "I am scuttle robot"
    myStringX = "the future of meka tronics"
    myStringY = "gig em aggies"
    while(1):
        signals = gp.getGP()
        if signals[6]==1: # A button is pressed
            t2s.say(myStringA)
        elif signals[7]==1: # X button is pressed
            t2s.say(myStringX)
        elif signals[5]==1: # B button is pressed
            temp = round(bmp.getTemp(),1)
            myStringB = "My brain temperature is" +str(temp)+ " degrees celsius."
            t2s.say(myStringB)
        elif signals[4]==1: # Y button is pressed
            t2s.say(myStringY)
        elif signals[11]==1: # rt button is pressed (button 7)
            adcData = adc.getADC()
            voltage = round(adcData[5],1)
            myString = "My battery strength is" +str(voltage)+ " volts."
            t2s.say(myString)
        elif signals[10]==1: 
            #myRSSI = rssi.get_rssi('wlan0')
            myRSSI = -71.4
            myString = "wifi rssi is" +str(myRSSI)+ " decibels."
            t2s.say(myString)
        time.sleep(0.020)
        
# CREATE A THREAD FOR DRIVING
def loop_drive( ID ):
    
    # initialize variables for control system
    t0 = 0
    t1 = 1
    e00 = 0
    e0 = 0
    e1 = 0
    dt = 0
    de_dt = np.zeros(2) # initialize the de_dt
    count = 0
    # initialize variables for color tracking
    color_range = np.array([[0, 180, 130], [10, 255, 255]])
    thetaOffset = 0
    # initialize driving mode
    mode = 0
    
    while(1):
        count += 1
        # THIS BLOCK IS FOR DRIVING BY COLOR TRACKING
        # colorTarget = ct.colorTarget(color_range) # use color tracking to generate targets
        # x = colorTarget[0]
        # if x != None:
        #     thetaOffset = ct.horizLoc(x) #grabs the angle of the target in degrees
        # myThetaDot = thetaOffset * 3.14/180 *2 # achieve centering in 0.5 seconds
        # print(myThetaDot)
        # myXDot = 0 # enable this line to freeze driving, and turn only.
        # myXDot = 
        # A = np.array([ myXDot, myThetaDot ])
        # pdTargets = inv.convert(A) # convert [xd, td] to [pdl, pdr]
        # print(pdTargets)
        
        # THIS BLOCK IS FOR CONSTANT SPEED DRIVING (NO CONTROL INPUT)
        # constantThetaDot = 1.5 # target, rad/s
        # constantXDot = 0.2 # target, m/sc
        # A = np.array([constantXDot, constantThetaDot])
        # myPhiDots = inv.convert(A)
       
        # THIS CODE IS FOR OPEN AND CLOSED LOOP control
        #pdTargets = np.array([9.7, 9.7]) #Fixed requested PhiDots; SPECIFICALLY FOR PID LAB
        pdTargets = inv.getPdTargets() # populates target phi dots from GamePad
        kin.getPdCurrent() # capture latest phi dots & update global var
        pdCurrents = kin.pdCurrents # assign the global variable value to a local var
       
        # THIS BLOCK UPDATES VARS FOR CONTROL SYSTEM
        t0 = t1  # assign t0
        t1 = time.time() # generate current time
        dt = t1 - t0 # calculate dt
        e00 = e0 # assign previous previous error
        e0 = e1  # assign previous error
        e1 = pdCurrents - pdTargets # calculate the latest error
        de_dt = (e1 - e0) / dt # calculate derivative of error
        
        # CALLS THE CONTROL SYSTEM TO ACTION
        signals = gp.getGP() # grab gamepad input
        if signals[14]: # check if mode button was pressed (Left stick)
            mode = not mode 
            time.sleep(1)
            #t2s.say("changing modes.")
        if mode == 0:
            sc.driveOpenLoop(pdTargets)
        else:
            sc.driveClosedLoop(pdTargets, pdCurrents, de_dt)  # call the control system
        time.sleep(0.05)
        
        
        u = sc.u 
        u_proportional = sc.u_proportional
        u_integral = sc.u_integral
        u_derivative = sc.u_derivative
        
        # THIS BLOCK OUTPUTS DATA TO A CSV FILE
        if count == 1:
            log.clear_file()
            log.csv_write([count,pdCurrents[0], pdTargets[0],u[0],u_integral[0],u_derivative[0]])
            #log.csv_write([count,pdCurrents[0], pdTargets[0], u[0]] )
        elif count > 1 and count <= 400:
            #log.csv_write([count,pdCurrents[0], pdTargets[0], u[0]])
            log.csv_write([count,pdCurrents[0],pdTargets[0],u[0],u_integral[0],u_derivative[0]])
            #print(count,pdCurrents[0], pdTargets[0])
        else:
            break

# CREATE A THREAD FOR SCANNING FOR OBSTACLES
def loop_scan( ID ):
    while(1):
        #d = obs.nearest_point() #returns the distance and the y-value of nearest obstacle
        #print("nearest point:", d)
        # if d[0] < 0.15: #if the nearest obstacle less than 10cm
        #         t2s.say("NO")
        time.sleep(0.1)

# ALL THREADS ARE CALLED TO RUN IN THE MAIN FUNCTION
def main():

        print("starting the main fcn")
        threads = []  # create an object for threads

        t = threading.Thread( target=loop_speak, args=(1,) ) # make 1st thread object
        threads.append(t)
        t.start()
        print("started thread1")

        t2 = threading.Thread( target=loop_drive, args=(2,) ) # make 2nd thread object
        threads.append(t2)
        t2.start()
        print("started thread2")

        t3 = threading.Thread( target=loop_scan, args=(3,) ) # make 2nd thread object
        threads.append(t3)
        t3.start()
        print("started thread3")

        # the join commands manipulate the way the program concludes multithreading.
        t.join()
        t2.join()
        t3.join()

main()

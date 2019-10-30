#DRIVING BY COLOR TRACKING WITH CLOSED-LOOP CONTROL

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
color_range = np.array([[45, 123, 83], [255, 135, 170]])  
thetaOffset = 0

while(1):
    ts0 = time.time()
    colorTarget = ct.colorTarget(color_range) # use color tracking to generate targets
    #print(colorTarget)
    ts1 = time.time() - ts0
    x = colorTarget[0]  # assign the x pixel location of the target
    if x != None:
        thetaOffset = ct.horizLoc(x) # grabs the angle of the target in degrees
    myThetaDot = thetaOffset * 3.14/180 *2 # attempt centering in 0.5 seconds
    print("processing (s):", round(ts1,4), "myTD (rad/s):", round(myThetaDot,3))
    myXDot = 0 # freeze the forward driving
    
    # Build speed targets array & send
    A = np.array([ myXDot, myThetaDot ])
    pdTargets = inv.convert(A) # convert from [xd, td] to [pdl, pdr]
    kin.getPdCurrent() # capture latest phi dots & update global var
    pdCurrents = kin.pdCurrents # assign the global variable value to a local var
   
    # UPDATES VARS FOR CONTROL SYSTEM
    t0 = t1  # assign t0
    t1 = time.time() # generate current time
    dt = t1 - t0 # calculate dt
    e00 = e0 # assign previous previous error
    e0 = e1  # assign previous error
    e1 = pdCurrents - pdTargets # calculate the latest error
    de_dt = (e1 - e0) / dt # calculate derivative of error
    
    # CALLS THE CONTROL SYSTEM TO ACTION
    sc.driveClosedLoop(pdTargets, pdCurrents, de_dt)  # call the control system
    time.sleep(0.005) # very small delay.

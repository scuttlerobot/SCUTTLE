# This code demonstrates a PI controller for the left wheel speed. 
# In addition to PI, there are two factors impacting 

#########################################################################################

# First we needed to import the rcpy library and initialize the cape
print("loading rcpy.")
# import rcpy library
# This automatically initizalizes the robotics cape
import rcpy
import rcpy.motor as motor # moves motors
print("finished loading libraries.")
import Adafruit_GPIO.I2C as Adafruit_I2C
import time
import math

#########################################################################################

# Setup Variables 
Motor_L = 1 # left motor is connected to output 1
iteration = 0 # iteration of loop
period = 0.03 # seconds between sampling
vr = 0.25 # requested velocity
dt_rev = 0.5*math.pi*0.082 # distance traveled per revolution of encoder, in meters (gear ratio * pi * diameter) 
encL = Adafruit_I2C.Device(0x40,1) # assign left encoder address
# Measurement Variables
enc0 = 0 # encoder, previous (deg)
enc1 = 0 # encoder, current (deg)
x0 = 0 # distance, previous (m)
x1 = 0 # distance, current (m)
dx1 = 0  # change in distance (m)
t0 = 0 # previos time (s)
t1 = 0 # current time (s)
dt0 = 0 # delta-time, previous (s)
dt1 = 0 # delta-time, current (s)
v0 = 0 # velocity, previous (m/s)
v1 = 0 # velocity, current (m/s)
dx1 = 0 # delta-distance, (m)
e0 = 0 #
e1 = 0

de_dt = 0
einteg = 0
Kp = 3.5
Ki = 0.25
Kd = 0  # Kd is not yet tested
u0 = 0 # control signal, previous
u1 = 0 # control signal, current

#########################################################################################

# Encoder Reading

# This is a mod that was given to us in speed_control
def read_encoder_angle(enc): #left encoder inputs
    try:
        x = enc.readU16(0xFE) # this grabs the encoder reading
        x = ((x << 8) | (x >> 8)) & 0xFFFF
        meas = ((x & 0xFF00) >> 2) | ( x & 0x3F)
        angle0 = meas*0.0219 # converts the readings into degrees
    except:
        print('Warning (I2C): Could not read encoder0')
        angle0 = 0
    
    return (angle0) # returns the current angle for the left and right encoder


#########################################################################################



print("initializing rcpy...")
rcpy.set_state(rcpy.RUNNING)
print("finished initializing rcpy.")


try:	

    while rcpy.get_state() != rcpy.EXITING: # Checks if you're in the correct state
        
        if rcpy.get_state() == rcpy.RUNNING: # check rcpy is running, then continue program
        
            x0 = x1 # store previous x reading
            enc1 = read_encoder_angle(encL) # grab a new encoder reading
            x1 = enc1/360*dt_rev # left-hand wheel distance = degrees * distance traveled per rev
            dx1 = -1*(x1-x0) # calculate change in distance (reversed magnitude for left hand)
            if dx1 < -0.001: # if the change is negative (over 1mm,) the encoder has rolled over
                dx1 = dx1 + dt_rev  #add 1 revolution if the encoder rolls over
            
            t0 = t1 # store t1 to t0
            t1 = time.time() # capture time
            dt0 = dt1 # store previous delta in time
            dt1 = t1-t0  # delta in time
            v0 = v1 # store previous velocity
            v1 = round(dx1/dt1,2) # velocity = dx/dt

            e0 = e1 # store previous error
            e1 = round(vr - v1,3) # error = requested minus current

            de_dt = (e1 - e0)/dt1 # derivative is change in error divided by time
            einteg = round((einteg + e1),4) #integral adds up errors forever
            
            KpTerm = Kp * e1        # generate Kp signal
            KiTerm = Ki * einteg    # generate Ki signal
            KdTerm = Kd * de_dt     # generate Kd signal
            
            u1 = round((KpTerm + KdTerm + KiTerm),3 ) # control signal is combo of 3 terms * error
            
            #Limit the change in u each loop
            dev = 0.025 # permitted control deviation from one loop to next
            if u1 > (u0+dev):
                u1 = (u0+dev)
            elif u1 < (u0 - dev):
                u1 = (u0 - dev)
            
            # Place Min/Max bounds on U
            u = sorted([0, u1, 1])[1] #the  function constrains a variable between 1st and 3rd args
            u0 = u # store previous u
            motor.set(Motor_L, u1)
            
            iteration += 1
            if iteration%10 == 1: #print info every 10 samples
                print("x1: ", round(x1,4), "x0: ", round(x0,4), "dt: ", round(dt1,4), "v1: ",v1, "e1: ", e1,"einteg: ", einteg," u: ", round(u,4))
            if iteration%300 == 0:
                motor.set(Motor_L,0) #stop the motor
                rcpy.set_state(rcpy.EXITING) #exit the main loop
            time.sleep(period) #delay by one period 
            
        elif rcpy.get_state() == rcpy.PAUSED:
                pass
    
except KeyboardInterrupt: # condition added to catch a "Ctrl-C" event and exit cleanly
    
    rcpy.set_state(rcpy.EXITING)
    pass

finally:
    
    rcpy.set_state(rcpy.EXITING)

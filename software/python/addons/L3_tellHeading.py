# L2_tellHeading.py
# This program checks the heading of the compass and vocalizes it through tts

# Import external libraries
import time
import numpy as np

# Import internal programs:
import L1_text2speech as tts # for talking
import L2_heading as head # for checking heading

def estimate(): # estimate the heading
    axes = head.getXY()
    scaled = head.scale(axes)
    h = head.getHeading(scaled) # gets heading in degrees
    deg = round(h*180/3.14,2)
    print("heading:",deg)
    print("abs-heading:", abs(deg))
    
    if -45 <= deg <= 45:
        case = 0 # North
    elif 45 <= deg <= 135:
        case = 1 # East
    elif -135 <= deg <= -45:
        case = 2 # West
    else:
        case = 3 # South
    return case
    
switcher={
  0:'Heading North',
  1:'Heading West',
  2:'Heading East',
  3:'Heading South'
  }

def tell():
    myHeading = estimate() # get the heading estimat
    str1 = switcher.get(myHeading) # get the string for the proper case
    print (str1)
    tts.say(str1) # speak

# THIS FUNCTION IS ADDED TO WRAP THE WHILE LOOP INTO ONE FUNCTION
def go():
    while 1:
        tell()
        time.sleep(3)   

# UNCOMMENT THIS CODE TO RUN AS A STANDALONE PROGRAM
# while 1:
#     tell()
#     time.sleep(3)

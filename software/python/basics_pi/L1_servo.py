# This program sets up a servo object and controls the servo
# L1_servo is compatible with raspberry Pi.
# Facing the servo horn, a positive command generates a clockwise turn.
# Servo Basics: lastminuteengineers.com/servo-motor-arduino-tutorial

# Import external programs
from gpiozero import Servo
from time import sleep

# Initialize relevant variables
servo = Servo(12) #initialize the servo on bcm pin 12

# THIS LOOP ONLY RUNS IF THE PROGRAM IS CALLED DIRECTLY
if __name__ == "__main__":
    print("starting L1_servo.py")
    while(1):
      servo.min()
      sleep(1)
      servo.mid()
      sleep(1)
      servo.max()
      sleep(1)

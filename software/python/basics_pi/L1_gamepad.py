# Gamepad Program for SCUTTLE running RasPi
# This program grabs values from the wireless EasySMX gamepad & stores to arrays.
# Gamepad dongle must be plugged in and gamepad activated at start of program.
# See the scuttle software guide for a map of buttons.
# 16 values will be returned, 4 floats (axes) and 12 booleans (buttons)
# last updated 2021.06

# Import external programs
import time                     # for keeping time
import threading                # for asynchronous buttons reporting
import numpy as np              # for handling arrays
from inputs import get_gamepad  # python module for user inputs

class Gamepad:
    def __init__(self):
        self.axesMap = {
            'ABS_X':'LEFT_X',
            'ABS_Y':'LEFT_Y',
            'ABS_Z':'RIGHT_X',
            'ABS_RZ':'RIGHT_Y',
        }

        self.buttonMap = {
            'BTN_SOUTH':'Y',
            'BTN_EAST':'B',
            'BTN_C':'A',
            'BTN_NORTH':'X',
            'BTN_WEST':'LB',
            'BTN_Z':'RB',
            'BTN_TL':'LT',
            'BTN_TR':'RT',
            'BTN_TL2':'BACK',
            'BTN_TR2':'START',
            'BTN_SELECT':'L_JOY',
            'BTN_START':'R_JOY',
        }

        self.buttons = {}
        self.axes = {}
        self.hat = [0,0]
        self.states = { 'axes': self.axes,
                        'buttons': self.buttons,
                        'hat': self.hat
                    }

        for button in self.buttonMap.keys():
            self.buttons[self.buttonMap[button]] = 0

        for axis in self.axesMap.keys():
            self.axes[self.axesMap[axis]] = 128

        # self.stateUpdater()
        self.stateUpdaterThread = threading.Thread(target=self.stateUpdater)
        self.stateUpdaterThread.start()

    def _getStates(self):
        events = get_gamepad()
        for event in events:
            # print(event.ev_type, event.code, event.state)
            if event.ev_type == "Absolute":
                if 'ABS_HAT' in event.code:
                    if 'ABS_HAT0X' == event.code:
                        self.hat[0] = event.state
                    elif 'ABS_HAT0Y' == event.code:
                        self.hat[1] = event.state
                else:
                    self.axes[self.axesMap[event.code]] = event.state
            elif event.ev_type == "Key":
                self.buttons[self.buttonMap[event.code]] = event.state
            else:
                pass

        self.states = { 'axes': self.axes,
                        'buttons': self.buttons,
                        'hat': self.hat
                    }

        return self.states

    def stateUpdater(self):
        while True:
            self._getStates()

    def getStates(self):
        return self.states

gamepad = Gamepad()
def getGP():
    axes = np.array([((2/255)*gamepad.axes['LEFT_X'])-1,
                        ((2/255)*gamepad.axes['LEFT_Y'])-1,
                        ((2/255)*gamepad.axes['RIGHT_X'])-1,
                        ((2/255)*gamepad.axes['RIGHT_Y'])-1]
                        )                                  # store all axes in an array

    buttons = np.array([gamepad.buttons['Y'],              # B0
                        gamepad.buttons['B'],              # B1
                        gamepad.buttons['A'],              # B2
                        gamepad.buttons['X'],              # B3
                        gamepad.buttons['LB'],             # B4
                        gamepad.buttons['RB'],             # B5
                        gamepad.buttons['LT'],             # B6
                        gamepad.buttons['RT'],             # B7
                        gamepad.buttons['BACK'],           # B8
                        gamepad.buttons['START'],          # B9
                        gamepad.buttons['L_JOY'],          # B10
                        gamepad.buttons['R_JOY']]          # B11
                        )                               # store all buttons in array

    gp_data = np.hstack((axes, buttons))                # this array will have 16 elements

    return(gp_data)

if __name__ == "__main__":      # This loop will only run if the program is called directly
    while True:                 # collect commands from the gamepad.  Runs once for each command in the queue.
        myGpData = getGP()      # store data from all axes to the myGpData variable
        print(myGpData)         # print out the first element of the data to confirm functionality
        time.sleep(0.25)

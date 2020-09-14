# This code writes and reads from the GPIO pins available on the BeagleBone Blue.
# See the scuttle wiring graphics pdf at github.com/MXET/SCUTTLE/tree/master/hardware
# Default outputs: Port 0: pins 0, 2.  Port 1: pins 0,1,2,3
# Default inputs: Port 0: pins 1,3
# Thanks to D. Ansari & Nextec capstone team for contributing this.

# Import external libraries
from Adafruit_BBIO.GPIO import *
import time

# DEFINE PIN DICTIONARY
# This dictionary stores our pins in a way that makes them easy to address
# without mapping certain inputs to certain outputs. Makes code shorter.
gpio = [
        [
            {'key': 'GP0_3',   'modes': [   OUT]},
            {'key': 'P9_23',   'modes': [IN,OUT]},
            {'key': 'GP0_5',   'modes': [   OUT]},
            {'key': 'P9_28',   'modes': [IN,OUT]}
        ],
        [
            {'key': 'GP1_3',       'modes': [OUT]},
            {'key': 'GP1_4',       'modes': [OUT]},
            {'key': 'RED_LED',     'modes': [OUT]},
            {'key': 'GREEN_LED',   'modes': [OUT]}
        ]
    ]


# DEFINE RELEVANT FUNCTIONS
def pin_setup(port=None, pin=None, state=None):                 # A function for setting up pins.
    for port in gpio:                                           # Setup all GPIO pins to default I/O state. (The first mode in the 'modes' dictionary)
        for pin in port:
            setup(pin['key'], pin['modes'][0])


def index_exists(index, i):                                     # Check that an idex exists. Used to check if a pin exists.
    try:
        a = gpio[i]
        return True
    except IndexError:
        return False


def check_args(port=None, pin=None, state=None):                # Check that the values passed to our functions are valid
    port_valid = isinstance(port, int) and port in [0, 1]       # Check that the port is in the list of valid port numbers
    pin_valid = isinstance(pin, int) and pin in [0, 1, 2, 3]    # Check that the pin is in the list of valid pin numbers
    if not port_valid:
        print("ERROR: {} is Not a Valid Port Number!".format(port))
    elif not pin_valid:
        print("ERROR: {} is Not a Valid Pin Number!".format(pin))
    return pin_valid and port_valid


def read(port, pin):                                            # Use this function to read an input.
    if check_args(port, pin):
        if gpio[port][pin]['modes'][0] == IN:
            state = input(gpio[port][pin]['key'])
            return state
        else:
            print("ERROR: Pin {} on port {} is not setup as an input!".format(pin, port))
    else:
        exit(1)


def write(port, pin, state):                                    # Use this function to control an output.
    if check_args(port, pin, state):
        if gpio[port][pin]['modes'][0] == OUT:
            output(gpio[port][pin]['key'], state)
        else:
            print("ERROR: Pin {} on port {} is not setup as an output!".format(pin, port))
    else:
        exit(1)

# SET UP ALL OF THE PINS TO DEFAULT


pin_setup()                                                     # set up all pins with the default modes.


# # UNCOMMENT THE SECTION BELOW TO RUN AS A STANDALONE PROGRAM
# # READ EXAMPLE
# if __name__ == "__main__":
#     while True:
#         pin = read(0, 1)                        # read port 0, pin 1
#         print("Port 0 Pin 1 Condition:", pin)   # print the state that was read.
#         time.sleep(1)                           # delay 1 second

# # WRITE EXAMPLE
# if __name__ == "__main__":
#     while True:                                 # a loop to blink the red LED.
#         time.sleep(1)
#         write(0, 0, 1)
#         time.sleep(1)
#         write(0, 0, 0)

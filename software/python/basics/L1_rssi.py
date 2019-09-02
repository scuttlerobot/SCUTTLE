# This program accesses info from the onboard WiFi module of the blue.
# it returns the RECEIVED wifi signal strength of the AP to which the blue is connected.
# Typical values fall near -70dB.  Values near -90dB or lower may lose connection.

#!/usr/bin/env python

import sys
import subprocess
import time

def get_rssi(interface): # ie, 'wlan0'
    proc = subprocess.Popen(["iwlist", interface, "scan"],stdout=subprocess.PIPE, universal_newlines=True)
    out, err = proc.communicate()
    out = out.split("\n")
    for i, val in enumerate(out):
        if 'Signal' in val:
            signal_line = val.split()
            if 'Signal' in signal_line:
                rssi = int(signal_line[signal_line.index('Signal')+1].split('=')[1])
    return rssi

# # UNCOMMENT THE SECTION BELOW TO RUN AS A STANDALONE PROGRAM
# while 1:
#     rssi = get_rssi('wlan0')
#     print(rssi)
#     time.sleep(0.2)

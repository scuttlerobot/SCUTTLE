# This program takes a message and sends it as a voice to the audio output.
# Please run "sudo apt-get install flite" before running this program.
# Next, you can adust volume with a GUI by the command "alsamixer"
# Make sure that the usb is connected on boot to ensure the usb device is recognized

import os # enables usage of shell commands

def say(message):
    s = str(message)  # Make sure input is a string by casting all inputs to a string.
    s2 = "\"" + s + "\"" # frame the text with quotations for passing to flite
    os.system("flite -t " + s2) # sends a system command from within the Python program.
    # male voice:  -voice rms
    # female voice: -voice slt
    
# # UNCOMMENT THIS SECTION TO RUN AS A STANDALONE PROGRAM
# while 1:
#     text = input("Enter text:")
#     say(text)

#!/usr/bin/python3

# L1_oled program for Raspberry Pi, used in lab 2 exercises. Does not display SSID, for simplicity
# Runs the SSD1306 with I2C and displays a title and IP address that is updated every second
# Before running, make sure to stop the default OLED service with the terminal command: 
#            sudo systemctl stop oled.service

import board
import digitalio
import netifaces as ni
from time import sleep
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

## Prepare settings and devices ##

# Display Parameters
address = 0x3d                              #I2C address for the display
screenwidth = 128                           #Display screen width in pixels
screenheight = 64                           #Display screen height in pixels
border = 2                                  #Display border in pixels

# Create a display object from the SSD1306_I2C class and call it oled
i2c = board.I2C()
oled_reset = digitalio.DigitalInOut(board.D4)
oled = adafruit_ssd1306.SSD1306_I2C(screenwidth, screenheight, i2c, addr=address, reset=oled_reset)
####


## Functions to get readings for IP and voltage ##

# Get a voltage reading from the INA219
def getVoltage():
    ##########################################
    # Task: Write your own code here to read and return a voltage from L1_ina
    #       Remember to import the necessary script
    ##########################################
    return

# This function will try to find an IPv4 address from eth0 (ethernet) or wlan0 (wireless), in that order
def getIp():
    for interface in ni.interfaces()[1:]:   #For interfaces eth0 and wlan0
    
        try:
            ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
            return ip
            
        except KeyError:                    #We get a KeyError if the interface does not have the info
            continue                        #Try the next interface since this one has no IPv4
        
    return 'No network found'                        #No interfaces had IPv4, so there's no network available

####


## OLED control functions ##

# Clear the screen by filling it with blank pixels
def clearScreen():
    oled.fill(0)
    oled.show()

# Display some text to the OLED
def displayText():
    ip = getIp()

    image = Image.new("1", (oled.width, oled.height))                       #create a new image to be displayed
    draw = ImageDraw.Draw(image)                                            #create a draw object so text and shapes can be drawn
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)      #draw a blank, filled rectangle the size of the screen to clear it

    font = ImageFont.load_default()                                         #load the default font for text

    #Draw text on the image starting at pixel coordinates (0,20) with a default font and no background fill
    draw.text((0, 20), "IP: " + ip, font=font, fill=255)

    #################################################
    # Task: Write your code here to call getVoltage() and add the value to the display 
    #################################################

    oled.image(image)                           #set the image to be displayed on the OLED                                        
    oled.show()                                 #show the new image

####


## Only runs if __name__ is __main__, indicating the script was executed directly ##
if __name__ == "__main__":
    clearScreen()                               #clear the screen on startup
    try:
        while True:
            sleep(1)                
            displayText()
            
    finally:
        clearScreen()                           #clear the screen when stopped

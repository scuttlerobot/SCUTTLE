#!/usr/bin/python3

# L1_oled program for Raspberry Pi, used in lab 2 exercises.
# Runs the SSD1306 with I2C and displays some text in free sans font
# Before running, make sure to stop the default OLED service with the terminal command: 
#            sudo systemctl stop oled.service


import board
import digitalio
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


## OLED control functions ##

# Clear the screen by filling it with blank pixels
def clearScreen():
    oled.fill(0)
    oled.show()

# Display some text to the OLED
def displayText():
    image = Image.new("1", (oled.width, oled.height))                       #create a new image to be displayed
    draw = ImageDraw.Draw(image)                                            #create a draw object so text and shapes can be drawn
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)      #draw a blank, filled rectangle the size of the screen to clear it
    
    # Load some fonts: the first is default and the rest are loaded from .ttf files
    # The value is the font size. Default font size cannot be changed.
    default = ImageFont.load_default()
    normal = ImageFont.truetype('/home/pi/MXET300-SCUTTLE/software/fonts/FreeSans.ttf',11)
    title = ImageFont.truetype('/home/pi/MXET300-SCUTTLE/software/fonts/FreeSans.ttf',14)
    bold = ImageFont.truetype('/home/pi/MXET300-SCUTTLE/software/fonts/FreeSansBold.ttf',11)

    draw.text((15, 0), "My SCUTTLE", font=title, fill=255)
    draw.text((10, 20), "This is FreeSansBold!", font=bold, fill=255)
    draw.text((10, 30), "This is FreeSans", font=normal, fill=255)
    draw.text((10, 40), "This is the default", font=default, fill=255)

    oled.image(image)
    oled.show()
####


## Only runs if our __name__ is __main__, indicating the script was executed directly ##
# By default, the program displays the text and exits, which leaves the text on display until
# another program overwrites the display buffer
if __name__ == "__main__":
    clearScreen()
    displayText()
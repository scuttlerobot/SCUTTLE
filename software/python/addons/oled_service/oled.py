#!/usr/bin/python3
# Default OLED script that displays a title, IP, and battery voltage; executed by a service

# Copy of the script used by oled.service, the original is /usr/share/pyshared/oled.py
# This prevents breaking the service if the workspace is deleted for some reason and prevents getting
# mixed up with the L1_oled script, which is for a lab exercise.

# ina219.py should be in the local directory, for the same reason above, to run the current sensor

import board
import digitalio
import netifaces as ni
from time import sleep
from threading import Thread
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
from adafruit_ina219 import INA219
import subprocess

class OledDisplay:

    def __init__(self,address=0x3d,bus=1):

        self.voltage = 0.0
        self.ip = 'No IP found'
        self.ssid = 'Not available'
        self.interface = 'lo'
        self.oled_reset = digitalio.DigitalInOut(board.D4)

        # Display Parameters
        self.address = address
        self.screenwidth = 128
        self.screenheight = 64
        self.border = 2

        self.i2c = board.I2C()
        self.oled = adafruit_ssd1306.SSD1306_I2C(self.screenwidth, self.screenheight, self.i2c, addr=self.address , reset=self.oled_reset)
        
        # Set up the INA219 sensor
        try:
            self.ina = INA219(self.i2c, 0x44)
        except Exception as ex:
            print("Failed to start current sensor")

        self.ipUpdateThread = Thread(target=self.ipUpdater)
        self.ipUpdateThread.daemon = True

    def clearScreen(self):
        self.oled.fill(0)
        self.oled.show()

    def updateVoltage(self):
        self.voltage = round(self.ina.bus_voltage, 2)

    def startIpUpdater(self):
        self.ipUpdateThread.start()

    def ipUpdater(self):
        while True:
            self.ip = self.getIp()

            # Ensures the interface the IP was grabbed from matches the SSID
            if self.interface == 'eth0': self.ssid = 'Wired Connection'
            else: self.ssid = self.getSSID()

            sleep(5)

    def getIp(self):
        for interface in ni.interfaces()[1:]:                               
            try:
                addr = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
            except KeyError:
                continue

            self.interface = interface 
            return addr

        return 'No IP found'

    # SSID only available for wireless networks, otherwise it is "Not available"
    def getSSID(self):
        try:
            return subprocess.check_output(['sudo','iwgetid']).decode().split('"')[1]
        except:
            return 'Not available'


    def displayText(self):
        image = Image.new("1", (self.oled.width, self.oled.height))
        
        font = ImageFont.load_default()

        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)


        # Task: Change the string in the line below to your SCUTTLE's name
        draw.text((40, 0), "SCUTTLE", font=font, fill=255)

        draw.text((0, 20), "IP: " + self.ip, font=font, fill=255)

        draw.text((0, 30), "SSID: " + self.ssid, font=font, fill=255)

        
        if self.ina is not None: 
            self.updateVoltage()
            draw.text((0, 40), "Robot Voltage: " +  str(self.voltage) + "V" , font=font, fill=255)

        self.oled.image(image)
        self.oled.show()


oled = OledDisplay()
oled.clearScreen()
oled.startIpUpdater()

try:
    while True:
        sleep(1)
        oled.displayText()
finally:
    oled.clearScreen()

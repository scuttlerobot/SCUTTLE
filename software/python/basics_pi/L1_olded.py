#!/usr/bin/python3

import board
import digitalio
import netifaces as ni
from time import sleep
from threading import Thread
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import L1_ina as ina

import subprocess

class OledDisplay:

    def __init__(self,address=0x3d,bus=1):

        self.voltage = 0.0
        self.ip = '0.0.0.0'
        self.oled_reset = digitalio.DigitalInOut(board.D4)

        # Display Parameters
        self.address = address
        self.screenwidth = 128
        self.screenheight = 64
        self.border = 2

        self.i2c = board.I2C()
        self.oled = adafruit_ssd1306.SSD1306_I2C(self.screenwidth, self.screenheight, self.i2c, addr=self.address , reset=self.oled_reset)

        self.ipUpdateThread = Thread(target=self.ipUpdater)
        self.ipUpdateThread.daemon = True

    def clearScreen(self):
        self.oled.fill(0)
        self.oled.show()

    def updateVoltage(self):
        self.voltage = ina.readVolts()

    def startIpUpdater(self):
        self.ipUpdateThread.start()

    def ipUpdater(self):
        while True:
            self.ip = self.getIp()
            sleep(5)

    def getIp(self):
        for interface in ni.interfaces()[1:]:
            try:
                return ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
            except KeyError:
                continue
        return '0.0.0.0'

    def displayText(self):
        image = Image.new("1", (self.oled.width, self.oled.height))
        
        font = ImageFont.load_default()

        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)

        self.updateVoltage()

        draw.text((15, 0), "CARSON'S SCUTTLE", font=font, fill=255)

        draw.text((0, 20), "IP " + self.ip, font=font, fill=255)

        draw.text((0, 36), "Robot Voltage " +  str(self.voltage) + " v" , font=font, fill=255)

        self.oled.image(image)
        self.oled.show()


oled = OledDisplay()
oled.clearScreen()
oled.startIpUpdater()

while True:
    sleep(1)
    oled.displayText()
        
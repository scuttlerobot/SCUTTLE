# This program sends data from beaglebone sensors to the mydevices.com IOT broker, Cayenne.
# The values are accelerometer (3 axes), gyroscope (3 axes), magnetometer (3 axes),
# voltage at the barrell plug DC jack, voltage at the JST LiPo Battery connector, and
# temperature of the imu chip.
#
# To run the program, you need to create a Cayenne account and enter your credentials
# for username, password, and client ID.

#!/usr/bin/env python

import rcpy
import time
import logging
import cayenne.client
import rcpy.adc as adc
import rcpy.mpu9250 as mpu9250
import rcpy.mpu9250 as mpu9250

sample_rate = 100

# set state to rcpy.RUNNING
rcpy.set_state(rcpy.RUNNING)

mpu9250.initialize(enable_dmp = True,
                       dmp_sample_rate = sample_rate,
                       enable_fusion = True,
                       enable_magnetometer = True)

# Cayenne authentication info. This should be obtained from the Cayenne Dashboard.
MQTT_USERNAME  = "PUT_YOUR_USERNAME_HERE"
MQTT_PASSWORD  = "PUT_YOUR_PASSWORD_HERE"
MQTT_CLIENT_ID = "PUT_YOUR_CLIENT_ID_HERE"


client = cayenne.client.CayenneMQTTClient()
#client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID)
# For a secure connection use port 8883 when calling client.begin:
client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID, port=8883, loglevel=logging.INFO)

i=0
timestamp = 0

while True:
    client.loop()
    # checking if rcpy is running
    if rcpy.get_state() == rcpy.RUNNING:

   	 if (time.time() > timestamp + 10):

                 data = mpu9250.read()
                 temp = mpu9250.read_imu_temp()

                 accel_data = data['accel']

                 client.virtualWrite(1, accel_data[0], "accel", "m/s^2")
                 client.virtualWrite(2, accel_data[1], "accel", "m/s^2")
                 client.virtualWrite(3, accel_data[2], "accel", "m/s^2")

                 gyro_data = data['gyro']

                 client.virtualWrite(4, gyro_data[0],"g","deg/s")
                 client.virtualWrite(5, gyro_data[1],"g","deg/s")
                 client.virtualWrite(6, gyro_data[2],"g","deg/s")

                 mag_data = data['mag']

                 client.virtualWrite(7, mag_data[0])
                 client.virtualWrite(8, mag_data[1])
                 client.virtualWrite(9, mag_data[2])

                 client.virtualWrite(10, adc.get_dc_jack_voltage())
                 client.virtualWrite(11, adc.get_battery_voltage())
                 client.virtualWrite(12, temp)

                 timestamp = time.time()
                 i = i+1

# This programs allows you to publish and subscribe to MQTT topics on the beagleboneblue.

#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import time
from multiprocessing import Process

broker = "broker.hivemq.com"
port = 1883

# This is the Publisher
client = mqtt.Client()
client.connect(broker,port,60)

def publish(topic, data):
    client.publish(topic, data);

# while 1:
#     publish("topic/test/scuttlel1", "on"+str(x))
#     time.sleep(1)






# from multiprocessing import Process
#
# # This is the Subscriber
# def sub():
#     def on_message(client, user, message):
#         data = message.payload.decode()
#         print(data)
#     client.subscribe("topic/test/scuttlel1")
#     client.on_message=on_message
#     client.loop_forever()
#
# if __name__ == '__main__':
#   p1 = Process(target=sub)
#   p1.start()
#   # p1.join()
#
# while 1:
#     print("in while:",data)
#     time.sleep(0.1)

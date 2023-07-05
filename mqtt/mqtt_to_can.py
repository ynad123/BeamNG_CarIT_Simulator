# Bridge from MQTT to CAN-Bus using in RaspPi

#import can
import os
import time

import sys
import struct
import socket
import os

import paho.mqtt.client as mqtt
from time import sleep
import threading
import time
import json

velocity = 0
rpm = 0
temp = 0

topic_str = "ima_beamng1"


#os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
time.sleep(0.1)



######## MQTT callback-methods ##################################
def process_connect2ServerHIVE():
    ##connect to MQTTServer:  
    print("start connect2")
    mqttClient2.connect("broker.hivemq.com", 1883, 60)
    mqttClient2.loop_start()
    
#after connection was established 2
def on_connectHIVE(mqttClient2, userdata, flags, rc):
    print("connected to HIVE")
    mqttClient2.subscribe(topic_str, 0)
    print("subscribed for topic on HIVE: ", topic_str)
    
    
#Reseive message and send with latence a response
def on_messageHIVE(mosq, obj, msg):
    try:
        if msg.topic.startswith(topic_str):
            m_decode = str(msg.payload.decode("utf-8","ignore"))
            m_decode = m_decode.replace('\'', '"')
            m_decode = m_decode.replace('False', 'false')
            m_decode = m_decode.replace('True', 'true')
    
            #print(m_decode)
            m_in = json.loads(m_decode)
            speed = m_in["wheelspeed"]*3.6
            rpm = m_in["rpm"]
            temp = m_in["oil_temperature"]
            print(speed)
            print(rpm)
            print(temp)            
            print("-----")
    except:
        print("Fehler")


########### Can-Message received ########################################################
def on_message_received(msg):
    print("msg erhalten: \n", str(msg))
    
    if (msg.arbitration_id == 0x7df):
        pid = msg.data[2]
        
        if (pid == 5):
            print("OBD Anfrage erhalten Temp",temp)
            transferValue = int(temp)+40
            A = transferValue
            data2 = [4, 0x41, pid, A, 0, 0, 0, 0]
            msg_back = can.Message(arbitration_id=0x7e8, data=data2, extended_id=False)
            bus.send(msg_back)

        if (pid == 12):
            print("OBD Anfrage erhalten RPM",rpm)
            transferValue = int(rpm * 4)
            A = int(transferValue/256)
            B = transferValue%256
            data2 = [4, 0x41, pid, A, B, 0, 0, 0]
            msg_back = can.Message(arbitration_id=0x7e8, data=data2, extended_id=False)
            bus.send(msg_back)

        if (pid == 13):
            print("OBD Anfrage erhalten V",velocity)
            A = int(velocity)
            data2 = [4, 0x41, pid, A, 0, 0, 0, 0]
            msg_back = can.Message(arbitration_id=0x7e8, data=data2, extended_id=False)
            bus.send(msg_back)

#bus = can.ThreadSafeBus(channel='can0', bustype='socketcan_native')
#msg = can.Message(arbitration_id=0x050, data=[1], extended_id=False)
#bus.send(msg)

#listener = can.Listener()
#listener.on_message_received = on_message_received
#notifier = can.Notifier(bus, [listener])


print("START")
mqttClient2 = mqtt.Client()
mqttClient2.on_connect = on_connectHIVE
mqttClient2.on_message = on_messageHIVE


process_connect2ServerHIVE()

while True:
    time.sleep(2)









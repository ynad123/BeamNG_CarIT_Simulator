#MQTT TestmqttClient GUI
import paho.mqtt.client as mqtt
from time import sleep
import threading
import time
import json

topic_str = "ima_beamng1"


#Connect to Server

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
            
            print("")
            print("-----")
            print("")
    except:
        print("Fehler")



#Main-Program


print("START")
mqttClient2 = mqtt.Client()
mqttClient2.on_connect = on_connectHIVE
mqttClient2.on_message = on_messageHIVE


process_connect2ServerHIVE()

while True:
    time.sleep(2)



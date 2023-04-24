import can
import paho.mqtt.client as mqtt
import os
import time

os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
time.sleep(0.1)

def process_connect2Server():
    #Creating Connection
    print("Connecting to Server...")
    client.connect("broker.hivemq.com", 1883, 60)
    
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("Connection: OK")
    else:
        print("Connection: FAILED")
#    client.subscribe("ima_koppmann/classification", 0)
#    print("Subscribed to 'ima_koppmann/classification'")

def on_message_received(msg):
    client.publish("ima/can_sniff", str(msg))
    print("msg published: \n", str(msg))

bus = can.ThreadSafeBus(channel='can0', bustype='socketcan_native')
msg = can.Message(arbitration_id=0x050, data=[1], extended_id=False)
bus.send(msg)

listener = can.Listener()
listener.on_message_received = on_message_received
notifier = can.Notifier(bus, [listener])

client = mqtt.Client()
process_connect2Server()
client.loop_forever()






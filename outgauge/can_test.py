import can
import paho.mqtt.client as mqtt
import os
import time

os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
time.sleep(0.1)

#Can-Message angekommen
def on_message_received(msg):
    print("msg erhalten: \n", str(msg))

bus = can.ThreadSafeBus(channel='can0', bustype='socketcan_native')
msg = can.Message(arbitration_id=0x050, data=[1], extended_id=False)
bus.send(msg)

listener = can.Listener()
listener.on_message_received = on_message_received
notifier = can.Notifier(bus, [listener])







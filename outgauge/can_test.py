import can
import os
import time

import sys
import struct
import socket
import os

velocity = 0
rpm = 0

os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
time.sleep(0.1)

#Can-Message angekommen
def on_message_received(msg):
    print("msg erhalten: \n", str(msg))
    
    if (msg.arbitration_id == 0x7df):
        pid = msg.data[2]
        
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

bus = can.ThreadSafeBus(channel='can0', bustype='socketcan_native')
msg = can.Message(arbitration_id=0x050, data=[1], extended_id=False)
bus.send(msg)

listener = can.Listener()
listener.on_message_received = on_message_received
notifier = can.Notifier(bus, [listener])

# Create UDP socket.
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to BeamNG OutGauge.
sock.bind(('192.168.2.103', 4444))

while True:
    # Receive data.
    data = sock.recv(96)    
    if not data:
        break # Lost connection 
    # Unpack the data.
    outsim_pack = struct.unpack('I4sH2c7f2I3f16s16si', data)

    velocity = outsim_pack[5] * 3.6
    rpm = outsim_pack[6]
    
    sys.stdout.write("%d km/h   ".center(15) % (velocity))
    sys.stdout.write("%d rpm \r" % (rpm))
    sys.stdout.flush()

# Release the socket.
sock.close()









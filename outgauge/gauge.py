#https://www.beamng.com/threads/outgauge-support-specifications.82507/

import sys
import struct
import socket
import os

velocity = 0

print("TEST ")
# Create UDP socket.
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to BeamNG OutGauge.
sock.bind(('192.168.2.108', 4444))

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
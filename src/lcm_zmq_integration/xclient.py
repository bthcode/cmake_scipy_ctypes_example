#!/usr/bin/env python
"""
Example Script to show LCM serialized data transported
 on by very simple ZeroMQ pub/sub message server/client
"""

from example_lcm import image_t
import sys
import zmq


# Set up a simple ZMQ subscriber
#  - socket type is zmq.SUB, meaning just listen
#  - socket connection is connect (with ip), i.e. as a client
context = zmq.Context()
socket = context.socket(zmq.SUB)

print("Collecting updates from message server...")
socket.connect("tcp://localhost:5556")

# Only listen for one type of key
MSG_KEY="KEY"
KEYLEN = len( MSG_KEY )
message_filter = MSG_KEY

# Python 2 - ascii bytes to unicode str
if isinstance(message_filter, bytes):
    message_filter = message_filter.decode('ascii')
socket.setsockopt_string(zmq.SUBSCRIBE, message_filter)

# Listening loope
while True:
    msg_string = socket.recv()
    image = image_t.decode( msg_string[KEYLEN:] )
    
    print image.data
# end while True

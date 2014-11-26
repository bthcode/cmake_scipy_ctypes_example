#!/usr/bin/env python

"""
Example Script to show LCM serialized data transported
 on by very simple ZeroMQ pub/sub message server/client
"""

import zmq
from example_lcm import image_t
import time

#
# Set up a simple ZMQ publisher
#   - socket type is zmq.PUB, meaning fire and forget publisher
#   - socket connection is bind ( meaning server ) 
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5556")

counter = 0
while True:
    
    # populate a sample LCM data structure
    I = image_t()
    I.data = [ counter,1,1,2,2,2,3,3,3,4,4,4]
    I.height = 4
    I.width  = 3
    I.size   = len(I.data )

    # give the message a type
    if counter % 2 == 0:
        buf = 'KEY' + I.encode()
    else:
        buf = 'XXX' + I.encode()

    counter += 1

    # send
    socket.send(buf)
    time.sleep(0.5) 
# end while True

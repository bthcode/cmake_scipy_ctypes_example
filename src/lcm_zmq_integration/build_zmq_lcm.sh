#!/bin/bash

./create-lcm.sh
g++ zmq_lcm_pub.cpp -lzmq -llcm -o zmq_lcm_pub -I.
g++ zmq_lcm_sub.cpp -lzmq -llcm -o zmq_lcm_sub -I.

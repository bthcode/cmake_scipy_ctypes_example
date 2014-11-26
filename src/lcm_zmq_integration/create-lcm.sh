#!/bin/sh

lcm-gen \
    --python --ppath python \
    --cpp    --cpp-hpath . \
    lcmtypes/*.lcm

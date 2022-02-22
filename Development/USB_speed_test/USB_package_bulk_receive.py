#!/usr/bin/env python3

#
# Copyright (c) 2020 Raspberry Pi (Trading) Ltd.
#
# SPDX-License-Identifier: BSD-3-Clause
#

# sudo pip3 install pyusb

import usb.core
import usb.util
import numpy as np
import time



dev = usb.core.find(idVendor=0x0000, idProduct=0x0001)

# find our device
#dev = usb.core.find(idVendor=0x0000, idProduct=0x0001)
# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()
# was it found?
if dev is None:
    raise ValueError('Device not found')
print(dev)
# get an endpoint instance
cfg = dev.get_active_configuration()
intf = cfg[(0, 0)]

outep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match= \
        lambda e: \
            usb.util.endpoint_direction(e.bEndpointAddress) == \
            usb.util.ENDPOINT_OUT)

inep = usb.util.find_descriptor(
    intf,
    # match the first IN endpoint
    custom_match= \
        lambda e: \
            usb.util.endpoint_direction(e.bEndpointAddress) == \
            usb.util.ENDPOINT_IN)

assert inep is not None
assert outep is not None
print(type(inep))
num_packages = 2048



for i in range(5):
    outep.write(num_packages.to_bytes(2, 'little'))

    time_1 = time.perf_counter()
    from_device = np.array(inep.read(64*num_packages), dtype = int)
    time_2 = time.perf_counter()
    time_elapsed = time_2 - time_1

    #print("Time Elapsed: ",time_elapsed)
    #print("Trasferred Bytes: ",np.size(from_device))
    #print("Speed: "+str(np.size(from_device)/time_elapsed)+" byte/s")
    print("Speed: "+str(8*np.size(from_device)/time_elapsed/10**6)+" Mbit/s")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
#
# Grove Base Hat for the Raspberry Pi, used to connect grove sensors.
# Copyright (C) 2019  Seeed Technology Co.,Ltd.
#
# Author: Jon Trulson <jtrulson@ics.com>
# Copyright (c) 2016-2017 Intel Corporation.
'''
This code is for
    - `Grove - 3-Axis Digital Compass V2 <https://www.seeedstudio.com/s/Grove-3-Axis-Digital-Compass-V2-p-3034.html>`_

'''

from __future__ import print_function
import time, sys, signal, atexit, math
from upm import pyupm_bmm150 as sensorObj


def main():
    # Instantiate a BMP250E instance using default i2c bus and address
    sensor = sensorObj.BMM150(0, 0x13)

    # For SPI, bus 0, you would pass -1 as the address, and a valid pin for CS:
    # BMM150(0, -1, 10);

    ## Exit handlers ##
    # This function stops python from printing a stacktrace when you hit control-C
    def SIGINTHandler(signum, frame):
        raise SystemExit

    # This function lets you run code on exit
    def exitHandler():
        print("Exiting")
        sys.exit(0)

    # Register exit handlers
    atexit.register(exitHandler)
    signal.signal(signal.SIGINT, SIGINTHandler)

    # now output data every 250 milliseconds
    while (1):
        sensor.update()

        data = sensor.getMagnetometer()
        print("Magnetometer x: {0:.2f}".format(data[0]), end=' ')
        print(" y: {0:.2f}".format(data[1]), end=' ')
        print(" z: {0:.2f}".format(data[2]), end=' ')
        print(" uT")

        xyHeading = math.atan2(data[0], data[1])
        zxHeading = math.atan2(data[2], data[0])
        heading = xyHeading

        if heading < 0:
            heading += 2*math.pi
        if heading > 2*math.pi:
            heading -= 2*math.pi
        
        headingDegrees = heading * 180/(math.pi); 
        xyHeadingDegrees = xyHeading * 180 / (math.pi)
        zxHeadingDegrees = zxHeading * 180 / (math.pi)

        print('heading(axis_Y point to): {0:.2f} degree'.format(headingDegrees))
        time.sleep(.250)

if __name__ == '__main__':
    main()

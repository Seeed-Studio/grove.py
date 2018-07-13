#!/usr/bin/env python
# Author: Jon Trulson <jtrulson@ics.com>
# Copyright (c) 2016-2017 Intel Corporation.
#
# The MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# 
# Change log:
# 
# 2018-07-13 
#   Modified by Lambor
#   To adapt Grove - 3-Axis Digital Compass V2(https://www.seeedstudio.com/s/Grove-3-Axis-Digital-Compass-V2-p-3034.html)
#   This library is used for Grove Base Hat which used to connect grove sensors for raspberry pi.
#
#   Requirement: install python-mraa and python-upm, see the instruction here https://github.com/Seeed-Studio/pi_repo#mraa--upm-package-repository-for-raspberry-pi 
#

from __future__ import print_function
import time, sys, signal, atexit, math
try:
    from upm import pyupm_bmm150 as sensorObj
except ImportError:
    print('Error: Please install python-mraa python-upm module.\r\n' 
          'See instruction here https://github.com/Seeed-Studio/pi_repo#mraa--upm-package-repository-for-raspberry-pi ')


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

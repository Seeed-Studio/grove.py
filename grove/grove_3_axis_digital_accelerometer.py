#!/usr/bin/env python
#
# This code is for Grove - 3-Axis Digital Accelerometer(+/-400g)
# (https://www.seeedstudio.com/Grove-3-Axis-Digital-Accelerometer-400-p-1897.html)
#
# which is a low power high performance 3-axis linear accelerometer belonging
# to the "nano" family, with digital I2C serial interface standard output.
#
# This is the library for Grove Base Hat which used to connect grove sensors for raspberry pi.
#

'''
## License

The MIT License (MIT)

Grove Base Hat for the Raspberry Pi, used to connect grove sensors.
Copyright (C) 2018  Seeed Technology Co.,Ltd. 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

from __future__ import print_function
from upm import pyupm_h3lis331dl as usnr

class Grove3AxisDigAccelerometer(object):
    def __init__(self):
        # Instantiate an H3LIS331DL on I2C bus 0
        self._snr = usnr.H3LIS331DL(
            usnr.H3LIS331DL_I2C_BUS,
            usnr.H3LIS331DL_DEFAULT_I2C_ADDR);
        
        # Initialize the device with default values
        self._snr.init()

        self._x = usnr.new_intp()
        self._y = usnr.new_intp()
        self._z = usnr.new_intp()
        self._adjx, self._adjy, self._adjz = 0, 0, 0

    def __del__(self):
        usnr.delete_intp(self._x)
        usnr.delete_intp(self._y)
        usnr.delete_intp(self._z)

    def read_raw(self):
        self._snr.update()
        self._snr.getRawXYZ(self._x, self._y, self._z)
        x = usnr.intp_value(self._x)
        y = usnr.intp_value(self._y)
        z = usnr.intp_value(self._z)
        return x, y, z

    def set_adjust(self, adjx, adjy, adjz):
        self._adjx, self._adjy, self._adjz = adjx, adjy, adjz

    def read_adjust(self):
        x, y, z = self.read_raw()
        x -= self._adjx
        y -= self._adjy
        z -= self._adjz
        return x, y, z

    def read(self):
        scale_fs_100 = 0.049
        x, y, z = self.read_adjust()
        x *= scale_fs_100
        y *= scale_fs_100
        z *= scale_fs_100
        return x, y, z

Grove = Grove3AxisDigAccelerometer

def main():
    import time, sys, signal, atexit

    ## Exit handlers ##
    # This function stops python from printing a stacktrace when you hit control-C
    def SIGINTHandler(signum, frame):
        raise SystemExit

    # This function lets you run code on exit, including functions from sensor
    def exitHandler():
        print("Exiting")
        sys.exit(0)

    # Register exit handlers
    atexit.register(exitHandler)
    signal.signal(signal.SIGINT, SIGINTHandler)

    print(
""" Make sure Grove-3-Axis-Digital-Acceleratometer(+/-400g)
   inserted in one I2C slot of Grove-Base-Hat
""")

    snr = Grove3AxisDigAccelerometer()

    print("""
STEPS to get more accurate accelerometer data
1. run this code with static(non-moving) sensor to get Raw data
2. uncomment the call to set_adjust() in the source code
   and fill parameters with Raw data got in step 1
3. the next run will get more accurate Accel data
""" )
    snr.set_adjust(0, 0, 0)
    # uncomment below line to set static(non-moving) Raw data
    # snr.set_adjust(160, -48, 496)
    while True:
        x, y, z = snr.read_raw()
        print("Raw:    X = {0:6}   Y = {1:6}   Z = {2:6}"
          .format(x, y, z))
        x, y, z = snr.read()
        print("Accel: AX = {0:6.3}g AY = {1:6.3}g AZ = {2:6.3}g"
          .format(x, y, z))
        time.sleep(.5)

if __name__ == '__main__':
    main()

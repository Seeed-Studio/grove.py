#!/usr/bin/env python
#
# This library is for Grove - Thumb Joystick(https://www.seeedstudio.com/Grove-Thumb-Joystick-p-935.html)
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
import math
import sys
import time
from grove.adc import ADC


class GroveThumbJoystick:

    def __init__(self, channelX, channelY):
        self.channelX = channelX
        self.channelY = channelY
        self.adc = ADC()

    @property
    def value(self):
        return self.adc.read(self.channelX), self.adc.read(self.channelY)

Grove = GroveThumbJoystick


def main():
    if len(sys.argv) < 3:
        print('Usage: {} X_channel Y_channel'.format(sys.argv[0]))
        sys.exit(1)

    sensor = GroveThumbJoystick(int(sys.argv[1]), int(sys.argv[2]))

    while True:
        x, y = sensor.value
        if x > 900:
            print('Joystick Pressed')
        print("X, Y = {0} {1}".format(x, y))
        time.sleep(.2)

if __name__ == '__main__':
    main()

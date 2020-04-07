#!/usr/bin/env python
#
# This is the library for Grove Base Hat which used to connect grove sensors for raspberry pi.
# We use python module serial to enable uart.
#
'''
## License

The MIT License (MIT)

Grove Base Hat for the Raspberry Pi, used to connect grove sensors.
Copyright (C) 2020  Seeed Technology Co.,Ltd. 

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
import serial
import os
from grove.gpio import GPIO
rev_to_tty = {
    1 : "/dev/ttyAMA0",
    2 : "/dev/ttyAMA0",
    3 : "/dev/ttyAMA0",
    4 : "/dev/ttyAMA0",
    'NPi_i_MX6ULL' : "/dev/ttymxc2"
}
rev_to_dtoverlay = {
    "NPi_i_MX6ULL" : "dtoverlay=/lib/firmware/imx-fire-uart3-overlay.dtbo >> /boot/uEnv.txt"
}
class UART:
    instance = None
    def __init__(self, tty = None, Baudrate = 9600, timeout = None):
        if tty is None:
            rev = GPIO.RPI_REVISION
            tty = rev_to_tty[rev]
            print("the default UART is %s"%(tty))
            if not os.path.exists(tty):
                meg = "\n\
#############################################################################\
\n\
\n\
Please use \'sudo sh -c echo \"%s\"\' then reboot to enable the default UART\
\n\
\n\
#############################################################################"%(rev_to_dtoverlay[rev])
                raise OSError (None, meg)
        if not self.instance:
            self.instance = serial.Serial(tty, Baudrate, timeout = timeout)
    def __getattr__(self, name):
        return getattr(self.instance, name)
def main():
    # https://pyserial.readthedocs.io/en/latest/shortintro.html
    ser = UART()
    print(ser.name)
    ser.write(b'hello')
    ser.close()
if __name__ == "__main__":
    main()
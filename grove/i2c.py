#!/usr/bin/env python
#
# This is the library for Grove Base Hat which used to connect grove sensors for raspberry pi.
# We use python module smbus2 instead of smbus.
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
import smbus2 as smbus
from smbus2 import i2c_msg
from grove.gpio import GPIO
import os
rev_to_bus = {
    1 : 0,
    2 : 1,
    3 : 1,
    'NPi_i_MX6ULL' : 1 ,
    "STM32MP1" : 1
}
rev_to_dtoverlay = {
    "NPi_i_MX6ULL" : "",
    'STM32MP1' : "uboot_overlay_addr2=/lib/firmware/stm32mp1-seeed-i2c4-overlay.dtbo >> /boot/uEnv.txt"
}
class Bus:
    instance = None
    MRAA_I2C = 0

    def __init__(self, bus=None):
        if bus is None:
            rev = GPIO.RPI_REVISION
            bus = rev_to_bus[rev]
            file_path = "/dev/i2c-%s"%(bus)
            if not os.path.exists(file_path):
                print("the default i2c is i2c-%s"%(bus))
                meg = "\n\
#############################################################################\
\n\
\n\
Please use \'sudo sh -c echo \"%s\"\' then reboot to enable the default I2C\
\n\
\n\
#############################################################################"%(rev_to_dtoverlay[rev])
                raise OSError (None, meg)
        if not self.instance:
            self.instance = smbus.SMBus(bus)
        self.bus = bus
        self.msg = i2c_msg
    def __getattr__(self, name):
        return getattr(self.instance, name)
def main():
    # https://github.com/kplindegaard/smbus2
    bus = Bus()
    print(bus.bus)
    print(bus.msg)
    bus.close()
if __name__ == "__main__":
    main()
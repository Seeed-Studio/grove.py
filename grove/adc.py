#!/usr/bin/env python
#
# This is the ADC library for Grove Base Hat which used to connect grove sensors for raspberry pi.
# 
# Grove Base Hat incorparates a micro controller STM32F030F4, raspberry pi does not have ADC unit,
# we use an external chip to transmit analog data to raspberry pi.
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
import grove.i2c


# 0x10 ~ 0x17: ADC raw data
# 0x20 ~ 0x27: input voltage
# 0x29: output voltage (Grove power supply voltage)
# 0x30 ~ 0x37: input voltage / output voltage
class ADC(object):
    def __init__(self, address=0x04):
        self.address = address
        self.bus = grove.i2c.Bus()

    def read_raw(self, channel):
        addr = 0x10 + channel
        return self.read_register(addr)

    # read input voltage (mV)
    def read_voltage(self, channel):
        addr = 0x20 + channel
        return self.read_register(addr)

    # input voltage / output voltage (%)
    def read(self, channel):
        addr = 0x30 + channel
        return self.read_register(addr)

    @property
    def name(self):
        id = self.read_register(0x0)
        if id == 0x4:
            return 'Grove Base HAT RPi'
        elif id == 0x5:
            return 'Grove Base HAT RPi Zero'

    @property
    def version(self):
        return self.read_register(0x3)

    # read 16 bits register
    def read_register(self, n):
        self.bus.write_byte(self.address, n)
        return self.bus.read_word_data(self.address, n)


if __name__ == '__main__':
    import time

    adc = ADC()
    while True:
        print(adc.read_voltage(0))
        time.sleep(1)


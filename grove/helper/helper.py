#!/usr/bin/env python
#
# This is the library for Grove Base Hat.
#
# Helper Classes
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
from grove.adc import *
import sys

_SlotsGPIORpi     = { 5:"D5", 12:"PWM", 16:"D16", 18:"D18", 22:"D22", 24:"D24", 26:"D26" }
_SlotsGPIORpiZero = { 5:"D5", 12:"PWM", 16:"D16"           }
_SlotsADCRpi      = { 0:"A0",  2:"A2",   4:"A4",   6:"A6"  }
_SlotsADCRpiZero  = { 0:"A0",  2:"A2",   4:"A4"            }
_SlotsPWMRpi      = {         12:"PWM",           18:"D18" }
_SlotsPWMRpiZero  = {         12:"PWM"                     }

class SlotHelper(object):
    # Slot types
    GPIO = 0
    ADC  = 1
    PWM  = 2
    I2C  = 3
    UART = 4

    def __init__(self, slot):
        adc = ADC()
        name = adc.name
        print("Hat Name = '{}'".format(name))
        if name == RPI_ZERO_HAT_NAME:
            self.__hat_type = RPI_ZERO_HAT_PID
            self.__slots_gpio = _SlotsGPIORpiZero
            self.__slots_adc  = _SlotsADCRpiZero
            self.__slots_pwm  = _SlotsPWMRpiZero
        elif name != RPI_HAT_NAME:
            print("Unknown hat, assume {}".format(RPI_HAT_NAME))
        if name != RPI_ZERO_HAT_NAME:
            self.__hat_type = RPI_HAT_PID
            self.__slots_gpio = _SlotsGPIORpi
            self.__slots_adc  = _SlotsADCRpi
            self.__slots_pwm  = _SlotsPWMRpi
        maps = {                       \
                SlotHelper.GPIO:self.__slots_gpio, \
                SlotHelper.ADC :self.__slots_adc,  \
                SlotHelper.PWM :self.__slots_pwm,  \
                }

        self._slots = maps.get(slot)
        self._slot  = slot

    def is_adapted(self, pin):
        if not self._slots:
            return False
        if not pin in self._slots.keys():
            return False
        return True

    def list_avail(self):
        if not self._slots:
            return

        maps = {                          \
                SlotHelper.GPIO: "GPIO",  \
                SlotHelper.ADC : "ADC",   \
                SlotHelper.PWM : "PWM",   \
                }

        print(" <pin> could be one of below values")
        print("       in the pin column for {} function".format(maps.get(self._slot)))
        print("   And connect the device to corresponding slot")
        print("==============")
        print(" pin | slot")
        print("==============")
        for pin, slot in self._slots.items():
            print('{:^5}|{:^5} '.format(pin, slot))

    def argv2pin(self):
        if len(sys.argv) < 2:
            print('Usage: {} <pin>'.format(sys.argv[0]))
            self.list_avail()
            sys.exit(1)

        pin = int(sys.argv[1])
        if not self.is_adapted(pin):
            self.list_avail()
            sys.exit(1)
        return pin


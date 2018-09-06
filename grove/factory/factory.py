#!/usr/bin/env python
#
# This is the library for Grove Base Hat.
#
# Factory Class
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
import sys
from enum import Enum
from grove.button      import *
from grove.led         import *
from grove.temperature import *
from grove.gpio        import *
from grove.lcd         import *

# GPIOWrapper settings
_wrapper_pir_motion = {
    'high-enable' : True,
    'direction'   : GPIO.IN,
    'status-attr' : "has_motion",
    'enable-attr' : "nothing",
    'disable-attr': "nothing"
}

_wrapper_buzzer = {
    'high-enable' : True,
    'direction'   : GPIO.OUT,
    'status-attr' : "sounding",
    'enable-attr' : "on",
    'disable-attr': "off"
}

_wrapper_electromagnet = {
    'high-enable' : True,
    'direction'   : GPIO.OUT,
    'status-attr' : "nothing",
    'enable-attr' : "on",
    'disable-attr': "off"
}

class __factory(object):
    ButtonEnum = Enum('Button', ("GPIO-LOW", "GPIO-HIGH", "I2C"))
    OneLedEnum = Enum('OneLed', ("GPIO-LOW", "GPIO-HIGH", "WS2812-PWM"))
    TemperEnum = Enum('Temper', ("NTC-ADC",  "MCP9808-I2C"))
    GPIOWrapperEnum = Enum('GPIOWrapper', ("PIRMotion", "Buzzer", "Electromagnet"))
    LcdEnum = Enum('Lcd', ("JHD1802", "SH1107G"))

    def __init__(self):
        pass

    def __avail_list(self, typ, enum):
        print("Factory.get: Wrong {} type specified {}".format(enum, typ))
        print("Available types: ", end='')
        for name,_ in enum.__members__.items():
            print(name, ',', sep='', end='')
        print("\b ")

    def getButton(self, typ, pin):
        if typ == "GPIO-LOW":
            return ButtonTypedGpio(pin, True)
        elif typ == "GPIO-HIGH":
            return ButtonTypedGpio(pin, False)
        elif typ == "I2C":
            # TODO
            return None
        else:
            self.__avail_list(typ, self.ButtonEnum)
            sys.exit(1)

    def getOneLed(self, typ, pin):
        if typ == "GPIO-LOW":
            return OneLedTypedGpio(pin, False)
        elif typ == "GPIO-HIGH":
            return OneLedTypedGpio(pin, True)
        elif typ == "WS2812-PWM":
            return OneLedTypedWs2812(pin)
        else:
            self.__avail_list(typ, self.OneLedEnum)
            sys.exit(1)

    def getTemper(self, typ, channel = None):
        if typ == "NTC-ADC":
            return TemperTypedNTC(channel)
        elif typ == "MCP9808-I2C":
            return TemperMCP9808()
        else:
            self.__avail_list(typ, self.TemperEnum)
            sys.exit(1)

    def getGpioWrapper(self, typ, pin):
        if typ == "PIRMotion":
            return GPIOWrapper(pin, _wrapper_pir_motion)
        elif typ == "Buzzer":
            return GPIOWrapper(pin, _wrapper_buzzer)
        elif typ == "Electromagnet":
            return GPIOWrapper(pin, _wrapper_electromagnet)
        else:
            self.__avail_list(typ, self.GPIOWrapperEnum)
            sys.exit(1)

    def getLcd(self, typ):
        if typ == "JHD1802":
            return JHD1802()
        elif typ == "SH1107G":
            return SH1107G_SSD1327()
        else:
            self._avail_list(typ, self.LcdEnum)


Factory = __factory()


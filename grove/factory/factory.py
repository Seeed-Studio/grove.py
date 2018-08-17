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
from enum import Enum
from grove.button import *
from grove.led    import *
import sys

class __factory(object):
    ButtonEnum = Enum('Button', ("GPIO-LOW", "GPIO-HIGH", "I2C"))
    OneLedEnum = Enum('OneLed', ("GPIO-LOW", "GPIO-HIGH", "PWM"))

    def __init__(self):
        pass

    def __avail_list(self, typ, enum):
        print("getButton: Wrong Button type specified {}".format(typ))
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
        elif typ == "PWM":
            # TODO
            return None
        else:
            self.__avail_list(typ, self.OneLedEnum)
            sys.exit(1)

Factory = __factory()


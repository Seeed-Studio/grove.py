#!/usr/bin/env python
#
# This is the library for Grove Base Hat.
#
# Temper(ature) Classes
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
import threading
from grove.i2c import Bus as I2C
from grove.temperature import Temper
from upm.pyupm_mcp9808 import MCP9808

class TemperMCP9808(Temper):
    def __init__(self):
        self.mcp = MCP9808(I2C.MRAA_I2C)
        self.mcp.setMode(True)  # Celsius
        self._resolution = Temper.RES_1_2_CELSIUS

    def _derive_res(self, res):
        ares = -1
        if res >= Temper.RES_1_2_CELSIUS:
            ares = MCP9808.RES_LOW
        elif res >= Temper.RES_1_4_CELSIUS:
            ares = MCP9808.RES_MIDDLE
        elif res >= Temper.RES_1_8_CELSIUS:
            ares = MCP9808.RES_HIGH
        elif res >= Temper.RES_1_16_CELSIUS:
            ares = MCP9808.RES_PRECISION

        if ares < 0:
            return False
        self.mcp.setResolution(ares)
        # print("ares = {}".format(ares))
        return True

    @property
    def temperature(self):
        return self.mcp.getTemp()


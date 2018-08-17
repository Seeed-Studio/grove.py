#!/usr/bin/env python
#
# This is the library for Grove Base Hat.
#
# Button Base Class
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

class Button(object):
    # event bits
    EV_RAW_STATUS    = 1 << 0
    EV_SINGLE_CLICK  = 1 << 1
    EV_DOUBLE_CLICK  = 1 << 2
    EV_LONG_PRESS    = 1 << 3
    EV_LEVEL_CHANGED = 1 << 4
    # EV_HAS           = 1 << 31

    pins = []

    def __init__(self, pin):
        self.__on_obj = None
        self.__on_event = None
        self.__event = 0
        self.pins.append(pin)
        # To use with button array
        self.__index = self.pins.index(pin)

    def get_on_event(self):
        return self.__on_obj, self.__on_event

    def on_event(self, obj, callback):
        if not obj:
            return
        if not callable(callback):
            return
        self.__on_obj, self.__on_event = obj, callback

    def is_pressed(self):
        return False

    # call by derivate class
    def _send_event(self, event, pressed, tm):
        if not callable(self.__on_event):
            return

        evt = {
                'index': self.__index,
                'code' : event,
                'pressed': pressed,
                'time' : tm,
        }
        self.__on_event(self.__on_obj, evt)

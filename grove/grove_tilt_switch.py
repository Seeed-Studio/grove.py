#!/usr/bin/env python
#
# This library is for Grove - Tilt Switch(https://www.seeedstudio.com/Grove-Tilt-Switch-p-771.html)
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
import time
from grove.gpio import GPIO


class GroveTiltSwitch(GPIO):
    def __init__(self, pin):
        super(GroveTiltSwitch, self).__init__(pin, GPIO.IN)
        self._on_trigger = None
        self._on_release = None

    @property
    def on_trigger(self):
        return self._on_trigger

    @on_trigger.setter
    def on_trigger(self, callback):
        if not callable(callback):
            return

        if self.on_event is None:
            self.on_event = self._handle_event

        self._on_trigger = callback

    @property
    def on_release(self):
        return self._on_release

    @on_release.setter
    def on_release(self, callback):
        if not callable(callback):
            return

        if self.on_event is None:
            self.on_event = self._handle_event

        self._on_release = callback

    def _handle_event(self, pin, value):

        if value:
            if callable(self._on_trigger):
                self._on_trigger()
        else:
            if callable(self._on_release):
                self._on_release()

Grove = GroveTiltSwitch


def main():
    from grove.helper import SlotHelper
    sh = SlotHelper(SlotHelper.GPIO)
    pin = sh.argv2pin()

    swicth = GroveTiltSwitch(pin)

    def on_trigger():
        print('Triggered')
    def on_release():
        print("Released.")

    swicth.on_trigger = on_trigger
    swicth.on_release = on_release

    while True:
        time.sleep(1)


if __name__ == '__main__':
    main()

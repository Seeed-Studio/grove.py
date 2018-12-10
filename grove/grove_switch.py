
#!/usr/bin/env python
#
# This library is for Grove - Switch(P)(https://www.seeedstudio.com/Grove-Switch%28P%29-p-1252.html)
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

    @property
    def state(self):
        return super(GroveTiltSwitch, self).read()


Grove = GroveTiltSwitch


def main():
    from grove.helper import SlotHelper
    sh = SlotHelper(SlotHelper.GPIO)
    pin = sh.argv2pin()

    swicth = GroveTiltSwitch(pin)

    while True:
        if swicth.state is 1:
            print("on")
        else:
            print("off")
        time.sleep(1)


if __name__ == '__main__':
    main()

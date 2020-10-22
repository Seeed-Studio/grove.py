#!/usr/bin/env python
#
# This library is for Grove - 4 Digit Display(https:#www.seeedstudio.com/Grove-Servo-p-1241.html) which has 4 red seven-segment displays
# This is the library for Grove Base Hat which used to connect grove sensors for raspberry pi.
#

"""
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
"""
import time
from grove.i2c import Bus

display_font4 = {
    'first_dot': 0x0080,                 # 'upper .'
    'second_dot': 0x2000,                 # 'lower .'
    '0': 0x4478,
    '1': 0x0060,
    '2': 0x0758,
    '3': 0x0770,
    '4': 0x4360,
    '5': 0x4730,
    '6': 0x4738,
    '7': 0x0070,
    '8': 0x4778,
    '9': 0x4770,
    'A': 0x4378,
    'B': 0x2d70,
    'C': 0x4418,
    'D': 0x2c70,
    'E': 0x4718,
    'F': 0x4318,
    'G': 0x4538,
    'H': 0x4368,
    'I': 0x2c10,
    'J': 0x0478,
    'K': 0x2806,
    'L': 0x4408,
    'M': 0x40ea,
    'N': 0x40ec,
    'O': 0x4478,
    'P': 0x4358,
    'Q': 0x447c,
    'R': 0x435c,
    'S': 0x0494,
    'T': 0x2810,
    'U': 0x4468,
    'V': 0x500a,
    'W': 0x506c,
    'X': 0x1086,
    'Y': 0x0882,
    'Z': 0x1412,
}

display_font2 = {
    'dot': 0x4000,
    '0': 0xa145,
    '1': 0x8001,
    '2': 0x3107,
    '3': 0xb007,
    '4': 0x9043,
    '5': 0xb046,
    '6': 0xb146,
    '7': 0x8005,
    '8': 0xb147,
    '9': 0xb047,
    'A': 0x9147,
    'B': 0xb415,
    'C': 0x2144,
    'D': 0xa415,
    'E': 0x3146,
    'F': 0x1146,
    'G': 0xb144,
    'H': 0x9143,
    'I': 0x2414,
    'J': 0xa101,
    'K': 0x0c18,
    'L': 0x2140,
    'M': 0x8169,
    'N': 0x8961,
    'O': 0xa145,
    'P': 0x1147,
    'Q': 0xa945,
    'R': 0x1947,
    'S': 0x2824,
    'T': 0x0414,
    'U': 0xa141,
    'V': 0x8821,
    'W': 0x8b41,
    'X': 0x0a28,
    'Y': 0x0428,
    'Z': 0x220c,
}

REG_INIT = 0x21
DISP_ON = 0x81
REG_BRIGHT = 0xE0
BRIGHT_DARKEST = 0
BRIGHT_DEFAULT = 6
BRIGHT_HIGHEST = 15

BLINK_OFF = 0
BLINK_2HZ = 1
BLINK_1HZ = 2

FOUR_TUBES = 0
TWO_TUBES = 1


class GroveAlphanumDisplay(object):

    def __init__(self, address=0x71, brightness=BRIGHT_DEFAULT, display_type=FOUR_TUBES):
        self.address = address
        self.display_type = display_type
        self.font = display_font4 if display_type == FOUR_TUBES else display_font2
        self.first_dot = False
        self.second_dot = False

        self.bus = Bus()
        self.data = [0] * 4 if self.display_type == FOUR_TUBES else 2

        self.bus.write_i2c_block_data(self.address, REG_INIT, [])
        self.bus.write_i2c_block_data(self.address, DISP_ON, [])
        self.set_brightness(brightness)

    def clear(self):
        self.data = [0] * 4 if self.display_type == FOUR_TUBES else 2
        self.first_dot = False
        self.second_dot = False
        self._show()

    def show(self, data):
        if type(data) is str:
            length = min(len(data), len(self.data))
            for i in range(length):
                self.data[i] = self.font.get(data[i], 0)
        else:
            raise ValueError('Not support {}'.format(type(data)))
        self._show()

    def _show(self):
        wire_bytes = [0, 0]
        byte_10 = 0
        byte_11 = 0

        if self.display_type == FOUR_TUBES:
            for d in self.data:
                wire_bytes += [d & 0xFF, (d >> 8) & 0xFF]
            for i, d in enumerate(self.data):
                if i == 0:
                    byte_10 |= (1 if (d & 0x02) else 0) << 4
                    byte_10 |= (1 if (d & 0x04) else 0) << 3
                elif i == 1:
                    byte_10 |= (1 if (d & 0x02) else 0) << 6
                    byte_11 |= (1 if (d & 0x04) else 0) << 6
                elif i == 2:
                    byte_10 |= (1 if (d & 0x02) else 0) << 5
                    byte_11 |= (1 if (d & 0x04) else 0) << 1
                else:
                    byte_11 |= (1 if (d & 0x02) else 0) << 2
                    byte_11 |= (1 if (d & 0x04) else 0) << 0

            if self.first_dot:
                byte_10 |= self.font['first_dot'] & 0xFF
                byte_11 |= (self.font['first_dot'] >> 8) & 0xFF
            if self.second_dot:
                byte_10 |= self.font['second_dot'] & 0xFF
                byte_11 |= (self.font['second_dot'] >> 8) & 0xFF

        else:
            for i in [1, 0]:
                value = self.data[i]
                if i == 1 and self.first_dot:
                    value |= self.font['dot']
                if i == 0 and self.second_dot:
                    value |= self.font['dot']
                wire_bytes += [(value >> 8) & 0xFF, value & 0xFF]

            wire_bytes += [0] * 4

        wire_bytes += [byte_10, byte_11]

        print(' '.join([f'0x{b:02x}' for b in wire_bytes]))

        self.bus.write_i2c_block_data(self.address, 0, wire_bytes)

    def set_brightness(self, brightness):
        if brightness > BRIGHT_HIGHEST or brightness < 0:
            brightness = BRIGHT_HIGHEST

        self.bus.write_byte(self.address, REG_BRIGHT | brightness)

    def set_blink_type(self, blink_type):
        if 0 < blink_type <= 2:
            self.bus.write_byte(self.address, 0x81 | (blink_type << 1))

    def set_dots(self, first, second):
        self.first_dot = first
        self.second_dot = second
        self._show()


Grove = GroveAlphanumDisplay


def main():
    display = GroveAlphanumDisplay()

    count = 0
    while True:
        t = time.strftime("%H%M", time.localtime(time.time()))
        display.first_dot = not display.first_dot
        display.second_dot = not display.second_dot

        display.show(t)

        time.sleep(1)

        count += 1

        if count % 60 == 0:
            display.set_blink_type(BLINK_OFF)
        if count % 60 == 20:
            display.set_blink_type(BLINK_1HZ)
        if count % 60 == 40:
            display.set_blink_type(BLINK_2HZ)


if __name__ == '__main__':
    main()

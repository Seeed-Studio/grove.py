#!/usr/bin/env python
#
# This is the library for Grove Base Hat.
#
# JHD1802M0 Classes
#
'''
## License

The MIT License (MIT)

Grove Base Hat for the Raspberry Pi, used to connect grove sensors.
Copyright (C) 2018  Seeed Technology Co.,Ltd. 
'''
import upm.pyupm_jhd1313m1 as upmjhd
from grove.display.base import Display
import sys, mraa

class JHD1802(Display):
    def __init__(self, address = 0x3E):
        self._bus = mraa.I2c(0)
        self._addr = address
        self._bus.address(self._addr)
        if self._bus.writeByte(0):
            print("Check if the LCD {} inserted, then try again"
                    .format(self.name))
            sys.exit(1)
        self.jhd = upmjhd.Jhd1313m1(0, address, address)

    @property
    def name(self):
        return "JHD1802"

    def type(self):
        return TYPE_CHAR

    def size(self):
        # Charactor 16x2
        # return (Rows, Columns)
        return 2, 16

    def clear(self):
        self.jhd.clear()

    def draw(self, data, bytes):
        return False

    def home(self):
        self.jhd.home()

    def setCursor(self, row, column):
        self.jhd.setCursor(row, column)

    def write(self, msg):
        self.jhd.write(msg)

    def _cursor_on(self, enable):
        if enable:
            self.jhd.cursorOn()
        else:
            self.jhd.cursorOff()

def main():
    import time

    lcd = JHD1802()
    rows, cols = lcd.size()
    print("LCD model: {}".format(lcd.name))
    print("LCD type : {} x {}".format(cols, rows))

    lcd.backlight(False)
    time.sleep(1)

    lcd.backlight(True)
    lcd.setCursor(0, 0)
    lcd.write("hello world!")
    lcd.setCursor(0, cols - 1)
    lcd.write('X')
    lcd.setCursor(rows - 1, 0)
    for i in range(cols):
        lcd.write(chr(ord('A') + i))

    time.sleep(3)
    lcd.clear()

if __name__ == '__main__':
    main()


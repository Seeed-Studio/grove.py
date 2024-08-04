#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
# Copyright (C) 2018  Seeed Technology Co.,Ltd.
#
# This is the library for Grove Base Hat
# which used to connect grove sensors for Raspberry Pi.
'''
This is the code for
    - `OLED Display 1.12"    <https://www.seeedstudio.com/Grove-OLED-Display-1-1-p-824.html>`_
    - `OLED Display 1.12" V2 <https://www.seeedstudio.com/Grove-OLED-Display-1-12-V2-p-3031.html>`_

Examples:

    .. code-block:: python

        import time
        from grove.factory import Factory

        oled = Factory.getDisplay("SH1107G")
        rows, cols = oled.size()
        print("OLED model: {}".format(oled.name))
        print("OLED type : {} x {}".format(cols, rows))

        oled.setCursor(0, 0)
        oled.write("hello world!")
        oled.setCursor(0, cols - 1)
        oled.write('X')
        oled.setCursor(rows - 1, 0)
        for i in range(cols):
            oled.write(chr(ord('A') + i))

        time.sleep(3)
        oled.clear()
'''
from grove.display.base import *
# from upm.pyupm_lcd import *
from grove.i2c import Bus
import sys

# sphinx autoapi required
__all__ = ["SH1107G_SSD1327"]

BasicFont = [
        [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
        [0x00,0x00,0x5F,0x00,0x00,0x00,0x00,0x00],
        [0x00,0x00,0x07,0x00,0x07,0x00,0x00,0x00],
        [0x00,0x14,0x7F,0x14,0x7F,0x14,0x00,0x00],
        [0x00,0x24,0x2A,0x7F,0x2A,0x12,0x00,0x00],
        [0x00,0x23,0x13,0x08,0x64,0x62,0x00,0x00],
        [0x00,0x36,0x49,0x55,0x22,0x50,0x00,0x00],
        [0x00,0x00,0x05,0x03,0x00,0x00,0x00,0x00],
        [0x00,0x1C,0x22,0x41,0x00,0x00,0x00,0x00],
        [0x00,0x41,0x22,0x1C,0x00,0x00,0x00,0x00],
        [0x00,0x08,0x2A,0x1C,0x2A,0x08,0x00,0x00],
        [0x00,0x08,0x08,0x3E,0x08,0x08,0x00,0x00],
        [0x00,0xA0,0x60,0x00,0x00,0x00,0x00,0x00],
        [0x00,0x08,0x08,0x08,0x08,0x08,0x00,0x00],
        [0x00,0x60,0x60,0x00,0x00,0x00,0x00,0x00],
        [0x00,0x20,0x10,0x08,0x04,0x02,0x00,0x00],
        [0x00,0x3E,0x51,0x49,0x45,0x3E,0x00,0x00],
        [0x00,0x00,0x42,0x7F,0x40,0x00,0x00,0x00],
        [0x00,0x62,0x51,0x49,0x49,0x46,0x00,0x00],
        [0x00,0x22,0x41,0x49,0x49,0x36,0x00,0x00],
        [0x00,0x18,0x14,0x12,0x7F,0x10,0x00,0x00],
        [0x00,0x27,0x45,0x45,0x45,0x39,0x00,0x00],
        [0x00,0x3C,0x4A,0x49,0x49,0x30,0x00,0x00],
        [0x00,0x01,0x71,0x09,0x05,0x03,0x00,0x00],
        [0x00,0x36,0x49,0x49,0x49,0x36,0x00,0x00],
        [0x00,0x06,0x49,0x49,0x29,0x1E,0x00,0x00],
        [0x00,0x00,0x36,0x36,0x00,0x00,0x00,0x00],
        [0x00,0x00,0xAC,0x6C,0x00,0x00,0x00,0x00],
        [0x00,0x08,0x14,0x22,0x41,0x00,0x00,0x00],
        [0x00,0x14,0x14,0x14,0x14,0x14,0x00,0x00],
        [0x00,0x41,0x22,0x14,0x08,0x00,0x00,0x00],
        [0x00,0x02,0x01,0x51,0x09,0x06,0x00,0x00],
        [0x00,0x32,0x49,0x79,0x41,0x3E,0x00,0x00],
        [0x00,0x7E,0x09,0x09,0x09,0x7E,0x00,0x00],
        [0x00,0x7F,0x49,0x49,0x49,0x36,0x00,0x00],
        [0x00,0x3E,0x41,0x41,0x41,0x22,0x00,0x00],
        [0x00,0x7F,0x41,0x41,0x22,0x1C,0x00,0x00],
        [0x00,0x7F,0x49,0x49,0x49,0x41,0x00,0x00],
        [0x00,0x7F,0x09,0x09,0x09,0x01,0x00,0x00],
        [0x00,0x3E,0x41,0x41,0x51,0x72,0x00,0x00],
        [0x00,0x7F,0x08,0x08,0x08,0x7F,0x00,0x00],
        [0x00,0x41,0x7F,0x41,0x00,0x00,0x00,0x00],
        [0x00,0x20,0x40,0x41,0x3F,0x01,0x00,0x00],
        [0x00,0x7F,0x08,0x14,0x22,0x41,0x00,0x00],
        [0x00,0x7F,0x40,0x40,0x40,0x40,0x00,0x00],
        [0x00,0x7F,0x02,0x0C,0x02,0x7F,0x00,0x00],
        [0x00,0x7F,0x04,0x08,0x10,0x7F,0x00,0x00],
        [0x00,0x3E,0x41,0x41,0x41,0x3E,0x00,0x00],
        [0x00,0x7F,0x09,0x09,0x09,0x06,0x00,0x00],
        [0x00,0x3E,0x41,0x51,0x21,0x5E,0x00,0x00],
        [0x00,0x7F,0x09,0x19,0x29,0x46,0x00,0x00],
        [0x00,0x26,0x49,0x49,0x49,0x32,0x00,0x00],
        [0x00,0x01,0x01,0x7F,0x01,0x01,0x00,0x00],
        [0x00,0x3F,0x40,0x40,0x40,0x3F,0x00,0x00],
        [0x00,0x1F,0x20,0x40,0x20,0x1F,0x00,0x00],
        [0x00,0x3F,0x40,0x38,0x40,0x3F,0x00,0x00],
        [0x00,0x63,0x14,0x08,0x14,0x63,0x00,0x00],
        [0x00,0x03,0x04,0x78,0x04,0x03,0x00,0x00],
        [0x00,0x61,0x51,0x49,0x45,0x43,0x00,0x00],
        [0x00,0x7F,0x41,0x41,0x00,0x00,0x00,0x00],
        [0x00,0x02,0x04,0x08,0x10,0x20,0x00,0x00],
        [0x00,0x41,0x41,0x7F,0x00,0x00,0x00,0x00],
        [0x00,0x04,0x02,0x01,0x02,0x04,0x00,0x00],
        [0x00,0x80,0x80,0x80,0x80,0x80,0x00,0x00],
        [0x00,0x01,0x02,0x04,0x00,0x00,0x00,0x00],
        [0x00,0x20,0x54,0x54,0x54,0x78,0x00,0x00],
        [0x00,0x7F,0x48,0x44,0x44,0x38,0x00,0x00],
        [0x00,0x38,0x44,0x44,0x28,0x00,0x00,0x00],
        [0x00,0x38,0x44,0x44,0x48,0x7F,0x00,0x00],
        [0x00,0x38,0x54,0x54,0x54,0x18,0x00,0x00],
        [0x00,0x08,0x7E,0x09,0x02,0x00,0x00,0x00],
        [0x00,0x18,0xA4,0xA4,0xA4,0x7C,0x00,0x00],
        [0x00,0x7F,0x08,0x04,0x04,0x78,0x00,0x00],
        [0x00,0x00,0x7D,0x00,0x00,0x00,0x00,0x00],
        [0x00,0x80,0x84,0x7D,0x00,0x00,0x00,0x00],
        [0x00,0x7F,0x10,0x28,0x44,0x00,0x00,0x00],
        [0x00,0x41,0x7F,0x40,0x00,0x00,0x00,0x00],
        [0x00,0x7C,0x04,0x18,0x04,0x78,0x00,0x00],
        [0x00,0x7C,0x08,0x04,0x7C,0x00,0x00,0x00],
        [0x00,0x38,0x44,0x44,0x38,0x00,0x00,0x00],
        [0x00,0xFC,0x24,0x24,0x18,0x00,0x00,0x00],
        [0x00,0x18,0x24,0x24,0xFC,0x00,0x00,0x00],
        [0x00,0x00,0x7C,0x08,0x04,0x00,0x00,0x00],
        [0x00,0x48,0x54,0x54,0x24,0x00,0x00,0x00],
        [0x00,0x04,0x7F,0x44,0x00,0x00,0x00,0x00],
        [0x00,0x3C,0x40,0x40,0x7C,0x00,0x00,0x00],
        [0x00,0x1C,0x20,0x40,0x20,0x1C,0x00,0x00],
        [0x00,0x3C,0x40,0x30,0x40,0x3C,0x00,0x00],
        [0x00,0x44,0x28,0x10,0x28,0x44,0x00,0x00],
        [0x00,0x1C,0xA0,0xA0,0x7C,0x00,0x00,0x00],
        [0x00,0x44,0x64,0x54,0x4C,0x44,0x00,0x00],
        [0x00,0x08,0x36,0x41,0x00,0x00,0x00,0x00],
        [0x00,0x00,0x7F,0x00,0x00,0x00,0x00,0x00],
        [0x00,0x41,0x36,0x08,0x00,0x00,0x00,0x00],
        [0x00,0x02,0x01,0x01,0x02,0x01,0x00,0x00],
        [0x00,0x02,0x05,0x05,0x02,0x00,0x00,0x00],
]

class SH1107G_SSD1327(Display):
    '''
    OLED Display 1.12"(v2) use chip SSD1327 or SH1107G.

    Args:
        address(int): I2C device address, default to 0x3E.
    '''
    MAX_GRAY    = 100
    _REG_CMD    = 0x00
    _REG_DATA   = 0x40
    _PAGE_CNT   = 16
    _PAGE_BYTES = 128
    _TOTAL_BYTES= _PAGE_CNT * _PAGE_BYTES
    
    _DISPLAY_CMD_OFF = 0xAE;
    _DISPLAY_CMD_ON = 0xAF;

    _BASE_LOW_COLUMN_ADDR = 0x00;
    _BASE_HIGH_COLUMN_ADDR = 0x10;
    _BASE_PAGE_START_ADDR = 0xB0;
    def __init__(self, address = 0x3C):
        super(SH1107G_SSD1327, self).__init__()
        self._bus = Bus(1)
        self._addr = address

        if self._bus.write_byte(self._addr, 0):
            print("Check if the OLED SH1107G/SSD1307 inserted, then try again")
            sys.exit(1)
 
        id = self._bus.read_byte_data(self._addr, SH1107G_SSD1327._REG_CMD)
        # print(" id = 0x{:2x}".format(id))
        self._sh1107 = (id & 0x3F) == 0x07
        # if not self._sh1107:
        #     self._ssd1327 = sh1107(self._bus)
        #     return

        blk =     [0xAE]   # Display OFF
        blk.append(0xD5)   # Set Dclk
        blk.append(0x50)   # 100Hz
        blk.append(0x20)   # Set row address
        blk.append(0x81)   # Set contrast control
        blk.append(0x80)
        blk.append(0xA0)   # Segment remap
        blk.append(0xA4)   # Set Entire Display ON 
        blk.append(0xA6)   # Normal display
        blk.append(0xAD)   # Set external VCC
        blk.append(0x80)
        blk.append(0xC0)   # Set Common scan direction
        blk.append(0xD9)   # Set phase leghth
        blk.append(0x1F)
        blk.append(0xDB)   # Set Vcomh voltage
        blk.append(0x27)
        blk.append(0xAF)   # Display ON
        blk.append(0xB0)
        blk.append(0x00)
        blk.append(0x10)
        self._cmds(blk)
        self.clear()

    def _cmd(self, cmd):
        try:
            self._bus.write_byte_data(self._addr,
                                    SH1107G_SSD1327._REG_CMD, cmd)
        except IOError:
            print("*** Check if OLED module inserted ***")
            sys.exit(1)

    def _cmds(self, cmds):
        for c in cmds:
            self._cmd(c)

    def _datas(self, datas):
        length = len(datas)
        data = bytearray(length + 1)
        data[0] = SH1107G_SSD1327._REG_DATA
        for i in range(length):
            data[i + 1] = datas[i]
        try:
            self._bus.write_i2c_block_data(self._addr,
                                  SH1107G_SSD1327._REG_DATA, datas)
        except IOError:
            print("*** Check if OLED module inserted ***")
            sys.exit(1)

    @property
    def name(self):
        '''
        Get device name

        Returns:
            string: SH1107G/SSD1307 depends your device plugin.
        '''
        return "SH1107G" # if self._sh1107 else "SSD1327"

    def type(self):
        '''
        Get device type

        Returns:
            int: ``TYPE_GRAY``
        '''
        return TYPE_GRAY

    def size(self):
        # if not self._sh1107:
        #     # Gray OLED 96x96
        #     return 12, 12
        # Gray OLED 128x128
        return 16, 16

    def clear(self):
        '''
        Clears the screen and positions the cursor in the upper-left corner.
        '''
        # if not self._sh1107:
        #     self._ssd1327.clear()
        #     return
        zeros = [ 0x0 for dummy in range(SH1107G_SSD1327._TOTAL_BYTES) ]
        self.draw(zeros, SH1107G_SSD1327._TOTAL_BYTES)

    def draw(self, data, bytes):
        '''
        Quickly transfer/draw bulk data (specified by data) to OLED,
        transfer size specified by bytes.

        Args:
            data (list of int): the data to transfer/draw
            bytes (int)       : data size
        '''
        # if not self._sh1107:
        #     self._ssd1327.draw(data, bytes)
        #     return

        # all pages fill with data
        for i in range(SH1107G_SSD1327._PAGE_CNT):
            if i > bytes / SH1107G_SSD1327._PAGE_BYTES:
                return
            self._cmd(self._BASE_PAGE_START_ADDR + i)
            self._cmd(self._BASE_LOW_COLUMN_ADDR)
            self._cmd(self._BASE_HIGH_COLUMN_ADDR)
            # fill one PAGE bytes
            for k in range(0, SH1107G_SSD1327._PAGE_BYTES, 32):
                # I2C limit to 32 bytes each transfer
                begin = i * SH1107G_SSD1327._PAGE_BYTES + k
                end   = begin + 32
                self._datas(data[begin:end])

    def home(self):
        '''
        Positions the cursor in the upper-left of the OLED.
        That is, use that location in outputting subsequent text to the display.
        '''
        # if not self._sh1107:
        #     self._ssd1327.home()
        #     return
        self.setCursor(0, 0)

    def setCursor(self, row, column):
        '''
        Position the OLED cursor; that is, set the location
        at which subsequent text written to the OLED will be displayed.

        Args:
            row   (int): the row at which to position cursor, with 0 being the first row
            column(int): the column at which to position cursor, with 0 being the first column

	Returns:
	    None
        '''
        # if not self._sh1107:
        #     self._ssd1327.setCursor(row, column)
        #     return
        self._cmd(self._BASE_PAGE_START_ADDR + row)
        self._cmd(0x08 if column % 2 else self._BASE_LOW_COLUMN_ADDR)
        self._cmd(self._BASE_HIGH_COLUMN_ADDR + (column >> 1))

    def _putchar(self, c):
        asc = ord(c)
        if asc < 32 or asc > 127:
                asc = ord(' ')
        for i in range(8):
            fontmap = []
            fontmap.append(BasicFont[asc - 32][i])
            self._datas(fontmap)

    def write(self, msg):
        '''
        Write character(s) to the OLED.

        Args:
            msg (string): the character(s) to write to the display

        Returns:
            None
        '''
        # if not self._sh1107:
        #     self._ssd1327.write(msg)
        #     return
        for i in range(len(msg)):
            self._putchar(msg[i])

    def _backlight_on(self, en):
        self._cmd(self._DISPLAY_CMD_ON if en else self._DISPLAY_CMD_OFF)


def main():
    import time

    oled = SH1107G_SSD1327()
    rows, cols = oled.size()
    print("OLED model: {}".format(oled.name))
    print("OLED type : {} x {}".format(cols, rows))

    oled.backlight(False)
    time.sleep(1)

    oled.backlight(True)
    oled.setCursor(0, 0)
    oled.write("hello world!")
    oled.setCursor(0, cols - 1)
    oled.write('X')
    oled.setCursor(rows - 1, 0)
    for i in range(cols):
        oled.write(chr(ord('A') + i))

    time.sleep(3)
    oled.clear()

if __name__ == '__main__':
    main()


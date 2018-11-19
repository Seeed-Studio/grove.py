#!/usr/bin/env python
#
# This is the library for Grove Base Hat which used to connect i2c-type button.
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
import time
from grove.i2c import Bus
from grove.button import Button

grove_5way_tactile_keys = ("KEY A","KEY B","KEY C","KEY D","KEY E")
grove_6pos_dip_switch_keys = ("POS 1","POS 2","POS 3","POS 4","POS 5","POS 6")

class ButtonTypedI2c(Button):
    def __init__(self,address = 0x03):
        self.bus = Bus()
        self.addr = address
        self.dev_id = 0
        self.val = 0
        self.probeDevID()
        self.get_val()
        self.send_Byte(0x02)
        app1 = self.status_read()
     	while 1:
            self.status_read()
            time.sleep(1.0)
            continue
    def set_devID(self,reg,size):
		self.bus.write_byte_data(self.addr, reg, size)
    def send_Byte(self, reg):
        self.bus.write_byte(self.addr, reg)
    def get_devID(self, data):
       return self.bus.read_byte(self.addr, data)
    def get_data(self, reg, len):
        return self.bus.read_i2c_block_data(self.addr, reg, len)
	
    def probeDevID(self):
        for i in range (4):
            id = self.get_data(0x00, 4)
            did = 0
            for j in range(4):
                did = (did >> 8) | (int(id[j]) << 24)
            #print("DEV_ID = {:8X}".format(did))
            if (did >> 16) == 0x2886:
                self.dev_id = did
                return self.dev_id
            self.get_devID(True)

    def get_val(self):
        if (self.dev_id & 0xFFFF) == 0x0002:
            self.val = 5
            print("Grove 5_way tactile Switch Insert")
            self.key_names = grove_5way_tactile_keys
            return self.val
        elif (self.dev_id & 0xFFFF) == 0x0003:
            self.val = 6
            print("Grove 6_pos dip Switch Insert")
            self.key_names = grove_6pos_dip_switch_keys
            return self.val

    def status_read(self):
        app = self.get_data(0x01, 4 + self.val)
        #print("get event ={}".format(app))
        for i in range(0, self.val):
            print("{} : RAW- ".format(self.key_names[i]), end='')
            print ("{} ".format(app[i+4] & 1 and "HIGH" or "LOW"))
            if (self.dev_id & 0xFFFF) == 0x0002:
                print ("{} ".format(app[i+4] & 1 and "RELEASEND" or "PRESSED"))
            elif (self.dev_id & 0xFFFF) == 0x0003:
                print ("{} ".format(app[i+4] & 1 and "OFF" or "ON"))
        for i in range(0, self.val):
            if app[i+4] & ~1:
                print("{} ".format(self.key_names[i]))
                print(": EVENT - ")
            if app[i+4] & (1 << 1):
                print("SINGLE-CLICK")
            if app[i+4] & (1 << 2):
                print("DOUBLE-CLICL")
            if app[i+4] & (1 << 3):
                print("LONG-PRESS")
            if app[i+4] & (1 << 4):
                print("LEVEL-CHANGED")

            print("")
        return app


def main():
	switch = ButtonTypedI2c()

if __name__ == "__main__":
	main()

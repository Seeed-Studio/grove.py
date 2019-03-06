#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
#
# Grove Base Hat for the Raspberry Pi, used to connect grove sensors.
# Copyright (C) 2018  Seeed Technology Co.,Ltd. 
'''
This is the code for
    - `Grove - 5-Way Switch          <https://www.seeedstudio.com/Grove-5-Way-Switch-p-3136.html>`_
    - `Grove - 6-Position DIP Switch <https://www.seeedstudio.com/Grove-6-Position-DIP-Switch-p-3137.html>`_
'''
from __future__ import print_function
from grove.button import Button
from grove.factory import Factory
import time

__all__ = ['GroveMultiSwitch']

class GroveMultiSwitch(object):
    def __init__(self):
        self.btn = Factory.getButton("I2C", 0)
        self.__on_event = None
        self.btn.on_event(self, GroveMultiSwitch.__handle_event)

    @property
    def on_event(self):
        return self.__on_event

    @on_event.setter
    def on_event(self, callback):
        if not callable(callback):
            return
        self.__on_event = callback

    def __handle_event(self, evt):
        # print("event index:{} event:{} pressed:{}"
        #      .format(evt['index'], evt['code'], evt['pressed']))
        if callable(self.__on_event):
            self.__on_event(evt['index'], evt['code'], evt['time'])
            return

        name = self.btn.name(evt['index'])
        event = evt['code']
        print("{} : ".format(name), end='')
        print("{} ".format("HIGH" if evt['pressed'] else "LOW "), end='')
        print("SINGLE CLICK " if event & Button.EV_SINGLE_CLICK  else "", end='')
        print("DOUBLE CLICK " if event & Button.EV_DOUBLE_CLICK  else "", end='')
        print("LONG   PRESS " if event & Button.EV_LONG_PRESS    else "", end='')
        print("LEVEL  CHANGE" if event & Button.EV_LEVEL_CHANGED else "", end='')
        print("")



def main():
    import time
    print(\
""" Make sure Grove-5-Way-Switch or Grove-6-Position-DIP-Switch
   inserted in one I2C slot of Grove-Base-Hat
""")

    switch = GroveMultiSwitch()

    # remove ''' pairs below to begin your experiment
    '''
    # define a customized event handle your self
    def cust_on_event(index, event, tm):
        print("event with code {}, time {}".format(event, tm))

    switch.on_event = cust_on_event
    '''
    while True:
        time.sleep(1)


if __name__ == '__main__':
    main()

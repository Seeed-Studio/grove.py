#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
#
# Grove Base Hat for the Raspberry Pi, used to connect grove sensors.
# Copyright (C) 2018  Seeed Technology Co.,Ltd.
#
'''
This is the grove.gpio.GPIO implemented by mraa.Gpio.
'''
import mraa

__all__ = ['GPIO']

class GPIO(mraa.Gpio):
    OUT = mraa.DIR_OUT
    IN = mraa.DIR_IN
    
    def __init__(self, pin, direction = None):
        mraa_pin = mraa.getGpioLookup("GPIO%02d" % pin)
        super(GPIO, self).__init__(mraa_pin, raw = False)
        self.pin = pin

        if direction is not None:
            if direction == self.OUT:
                self.edge(mraa.EDGE_NONE)
            self.dir(direction)

        self._event_handle = None
    
    @staticmethod
    def _on_event(self):
        value = self.read()
        if self._event_handle:
            self._event_handle(self.pin, value)

    @property
    def on_event(self):
        return self._event_handle

    @on_event.setter
    def on_event(self, handle):
        if not callable(handle):
            return
        if self._event_handle is None:
            self.isr(mraa.EDGE_BOTH, self._on_event, self)

        self._event_handle = handle

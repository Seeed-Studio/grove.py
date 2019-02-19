#!/usr/bin/env python
#
# This is the library for Grove Base Hat.
#
# Display Base Classe
#
'''
## License

The MIT License (MIT)

Grove Base Hat for the Raspberry Pi, used to connect grove sensors.
Copyright (C) 2018  Seeed Technology Co.,Ltd. 
'''

class Display(object):
    def __init__(self):
        self._cursor = False
        self._backlight = False

    # To be derived
    def _cursor_on(self, en):
        pass

    def cursor(self, enable = None):
        if type(enable) == bool:
            self._cursor = enable
            self._cursor_on(enable)
        return self._cursor

    # To be derived
    def _backlight_on(self, en):
        pass

    def backlight(self, enable = None):
        if type(enable) == bool:
            self._backlight = enable
            self._backlight_on(enable)
        return self._backlight


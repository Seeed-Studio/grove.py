#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
#
# Grove Base Hat for the Raspberry Pi, used to connect grove sensors.
# Copyright (C) 2020  Seeed Technology Co.,Ltd.
import os
import os.path
import sys
import time
import threading
# These arrays contain tuples of all the relevant GPIO data for each board
# Platform. The fields are:
# - Linux GPIO pin number,
# - GPIO chip sysfs directory
# - Pin number (BOARD mode)
# - Pin number (BCM mode)
# - Pin name (CVM mode)
# - Pin name (TEGRA_SOC mode)
# - PWM chip sysfs directory
# - PWM ID within PWM chip
# The values are use to generate dictionaries that map the corresponding pin
# mode numbers to the Linux GPIO pin number and GPIO chip directory
NPi_i_MX6ULL = 'NPi_i_MX6ULL'

NPi_i_MX6ULL_PIN_DEFS = [
    ((1-1)*32+27, '/sys/class/gpio', 7,  4,  'GPIO09', 'AUD_MCLK', None, None),
    ((1-1)*32+3,  '/sys/class/gpio', 11, 17, 'UART1_RTS', 'UART1_RTS', None, None),
    ((4-1)*32+26, '/sys/class/gpio', 12, 18, 'I2S0_SCLK', 'DAP5_SCLK', None, None),
    ((1-1)*32+2,  '/sys/class/gpio', 13, 27, 'SPI1_SCK', 'SPI3_SCK', None, None),
    ((1-1)*32+0,  '/sys/class/gpio', 15, 22, 'GPIO12', 'TOUCH_CLK', None, None),
    ((4-1)*32+23, '/sys/class/gpio', 16, 23, 'SPI1_CS1', 'SPI3_CS1_N', None, None),
    ((4-1)*32+18, '/sys/class/gpio', 18, 24, 'SPI1_CS0', 'SPI3_CS0_N', None, None),
    ((1-1)*32+22, '/sys/class/gpio', 19, 10, 'SPI0_MOSI', 'SPI1_MOSI', None, None),
    ((1-1)*32+23, '/sys/class/gpio', 21, 9, 'SPI0_MISO', 'SPI1_MISO', None, None),
    ((4-1)*32+17, '/sys/class/gpio', 22, 25, 'SPI1_MISO', 'SPI3_MISO', None, None),
    ((1-1)*32+21, '/sys/class/gpio', 23, 11, 'SPI0_SCK', 'SPI1_SCK', None, None),
    ((1-1)*32+20, '/sys/class/gpio', 24, 8, 'SPI0_CS0', 'SPI1_CS0_N', None, None),
    ((1-1)*32+18, '/sys/class/gpio', 26, 7, 'SPI0_CS1', 'SPI1_CS1_N', None, None),
    ((4-1)*32+21, '/sys/class/gpio', 29, 5, 'GPIO01', 'SOC_GPIO41', None, None),
    ((4-1)*32+22, '/sys/class/gpio', 31, 6, 'GPIO11', 'SOC_GPIO42', None, None),
    ((4-1)*32+19, '/sys/class/gpio', 32, 12, 'GPIO07', 'SOC_GPIO44', '/sys/class/pwm', 0),
    ((4-1)*32+20, '/sys/class/gpio', 33, 13, 'GPIO13', 'SOC_GPIO54', '/sys/class/pwm', 0),
    ((4-1)*32+25, '/sys/class/gpio', 35, 19, 'I2S0_FS', 'DAP5_FS', None, None),
    ((4-1)*32+24, '/sys/class/gpio', 36, 16, 'UART1_CTS', 'UART1_CTS', None, None),
    ((1-1)*32+26, '/sys/class/gpio', 37, 26, 'SPI1_MOSI', 'SPI3_MOSI', None, None),
    ((4-1)*32+27, '/sys/class/gpio', 38, 20, 'I2S0_DIN', 'DAP5_DIN', None, None),
    ((4-1)*32+28, '/sys/class/gpio', 40, 21, 'I2S0_DOUT', 'DAP5_DOUT', None, None)
]
compats_imx6ull = (
    'fsl,imx6ull-14x14-evkfsl,imx6ulldebian',
)
debian_gpio_data = {
    NPi_i_MX6ULL: (
        NPi_i_MX6ULL_PIN_DEFS,
        {
            'P1_REVISION': 1,
            'RAM': '16384M',
            'REVISION': 'Unknown',
            'TYPE': 'board NX',
            'MANUFACTURER': 'NVIDIA',
            'PROCESSOR': 'ARM Carmel'
        }
    ),
}
class ChannelInfo(object):
    def __init__(self, channel, gpio_chip_dir, gpio, pwm_chip_dir, pwm_id):
        self.channel = channel
        self.gpio_chip_dir = gpio_chip_dir
        self.gpio = gpio
        self.pwm_chip_dir = pwm_chip_dir
        self.pwm_id = pwm_id
        
def get_data():
    compatible_path = '/proc/device-tree/compatible'
    # gpio_chip_dir = '/sys/class/gpio'
    
    with open(compatible_path, 'r') as f:
        compatibles = f.read().split('\x00')

    def matches(vals):
        return any(v in compatibles for v in vals)

    if matches(compats_imx6ull):
        model = NPi_i_MX6ULL
    else:
        raise Exception('Could not determine model')

    pin_defs, board_info = debian_gpio_data[model]
    pwm_dirs = {}

    def pwm_dir(chip_dir):
        if chip_dir is None:
            return None
        if chip_dir in pwm_dirs:
            return pwm_dirs[chip_dir]
        chip_pwm_dir = chip_dir + '/pwm'
        # Some PWM controllers aren't enabled in all versions of the DT. In
        # this case, just hide the PWM function on this pin, but let all other
        # aspects of the library continue to work.
        if not os.path.exists(chip_pwm_dir):
            return None
        for fn in os.listdir(chip_pwm_dir):
            if not fn.startswith('pwmchip'):
                continue
            chip_pwm_pwmchip_dir = chip_pwm_dir + '/' + fn
            pwm_dirs[chip_dir] = chip_pwm_pwmchip_dir
            return chip_pwm_pwmchip_dir
        return None

    def model_data(key_col, pin_defs):
        return {x[key_col]: ChannelInfo(
            x[key_col],
            x[1],
            x[0],
            pwm_dir(x[6]),
            x[7]) for x in pin_defs}
    channel_data = model_data(2, pin_defs)

    return model, board_info, channel_data

MODEL, BOARD_INFO, CHANNEL_DATA = get_data()
RPI_INFO = BOARD_INFO

def _channel_to_info(channel, need_gpio=False, need_pwm=False):
    if channel not in CHANNEL_DATA:
        raise ValueError("Channel %s is invalid" % str(channel))
    ch_info = CHANNEL_DATA[channel]
    if need_gpio and ch_info.gpio_chip_dir is None:
        raise ValueError("Channel %s is not a GPIO" % str(channel))
    if need_pwm and ch_info.pwm_chip_dir is None:
        raise ValueError("Channel %s is not a PWM" % str(channel))
    return ch_info

_SYSFS_ROOT = '/sys/class/gpio'

def _export_gpio(gpio):
    if os.path.exists(_SYSFS_ROOT + "/gpio%i" % gpio):
        return

    with open(_SYSFS_ROOT + "/export", "w") as f_export:
        f_export.write(str(gpio))

    while not os.access(_SYSFS_ROOT + "/gpio%i" % gpio + "/value",
                        os.R_OK | os.W_OK):
        time.sleep(0.01)

def _unexport_gpio(gpio):
    if not os.path.exists(_SYSFS_ROOT + "/gpio%i" % gpio):
        return
    with open(_SYSFS_ROOT + "/unexport", "w") as f_unexport:
        f_unexport.write(str(gpio))

def _setup_single_out(gpio):
    _export_gpio(gpio)
    gpio_dir_path = _SYSFS_ROOT + "/gpio%i" % gpio + "/direction"
    with open(gpio_dir_path, 'w') as direction_file:
        direction_file.write("out")

def _setup_single_in(gpio):
    _export_gpio(gpio)
    gpio_dir_path = _SYSFS_ROOT + "/gpio%i" % gpio + "/direction"
    with open(gpio_dir_path, 'w') as direction:
        direction.write("in")

def _output_one(gpio, value):
    with open(_SYSFS_ROOT + "/gpio%s" % gpio + "/value", 'w') as value_file:
        value_file.write(str(int(bool(value))))
def _input_one(gpio):
    with open(_SYSFS_ROOT + "/gpio%i" % gpio + "/value") as value:
        value_read = int(value.read())
        return value_read
class GPIO(object):

    # GPIO directions. UNKNOWN constant is for gpios that are not yet setup
    UNKNOWN = -1
    OUT = 0
    IN = 1
    DIR = None

    # Edge possibilities
    # These values (with _EDGE_OFFSET subtracted) must match gpio_event.py:*_EDGE
    # _EDGE_OFFSET = 30
    # RISING = 1 + _EDGE_OFFSET
    # FALLING = 2 + _EDGE_OFFSET
    # BOTH = 3 + _EDGE_OFFSET
    def __init__(self, pin, direction=None):
        self.pin = pin
        self.ch_info = _channel_to_info(self.pin, need_gpio=True)
        if direction is not None:
            self.dir(direction)
        self._event_handle = None

    def __del__(self):
        _unexport_gpio(self.ch_info.gpio)

    def dir(self, direction):
        # check direction is valid
        if direction != self.OUT and direction != self.IN:
            raise ValueError("An invalid direction was passed to setup()")
        self.DIR = direction
        if self.DIR == self.OUT:
            _setup_single_out(self.ch_info.gpio)
        elif self.DIR == self.IN:
            _setup_single_in(self.ch_info.gpio)

    def write(self, output):
        if self.OUT != self.DIR:
            raise RuntimeError("You must dir() the GPIO channel as an "
                            "output first")
        _output_one(self.ch_info.gpio, output)

    def read(self):
        return _input_one(self.ch_info.gpio)

    def _on_event(self, pin):
        value = self.read()
        if self._event_handle:
            self._event_handle(pin, value)

    @property
    def on_event(self):
        return self._event_handle

    @on_event.setter
    def on_event(self, handle):
        if not callable(handle):
            raise TypeError("Callback Parameter must be callable")
        if self._event_handle is None:
            if self.IN == self.DIR:
                raise RuntimeError("You must dir() the GPIO channel as an "
                                "input first")
            # RPi.GPIO.add_event_detect(self.pin, RPi.GPIO.BOTH, self._on_event)
        self._event_handle = handle


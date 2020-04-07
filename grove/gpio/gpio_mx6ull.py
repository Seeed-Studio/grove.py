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
import grp
import subprocess
try:
    import thread
except:
    import _thread as thread
from select import epoll, EPOLLIN, EPOLLET, EPOLLPRI
try:
    InterruptedError = InterruptedError
except:
    InterruptedError = IOError
from datetime import datetime
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
BCM = 3
BOARD = 2
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
    'fsl,imx6ull-14x14-evkfsl',
    'fsl,imx6ull',
)
gpio_data = {
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
    def __init__(self, channel, gpio_chip_dir, pin, pwm_chip_dir, pwm_id):
        self.channel = channel
        self.gpio_chip_dir = gpio_chip_dir
        self.pin = pin
        self.pwm_chip_dir = pwm_chip_dir
        self.pwm_id = pwm_id
def get_data():

    # pin_defs, board_info = gpio_data[model]
    pin_defs = NPi_i_MX6ULL_PIN_DEFS
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
    channel_data = model_data(BCM, pin_defs)
    return  channel_data
CHANNEL_DATA = get_data()
_SYSFS_ROOT = '/sys/class/gpio'


class _Gpios:
    def __init__(self, gpio, edge=None, bouncetime=None):
        self.edge = edge
        self.value_fd = open(_SYSFS_ROOT + "/gpio%i" % gpio + "/value", 'r')
        self.initial_thread = True
        self.initial_wait = True
        self.thread_added = False
        self.bouncetime = bouncetime
        self.gpio = gpio
        self.callbacks = []
        self.lastcall = 0
        self.event_occurred = False

    def __del__(self):
        self.value_fd.close()
        del self.callbacks

def _channel_to_info(channel, need_gpio=False, need_pwm=False):
    if channel not in CHANNEL_DATA:
        raise ValueError("Channel %s is invalid" % str(channel))
    ch_info = CHANNEL_DATA[channel]
    if need_gpio and ch_info.gpio_chip_dir is None:
        raise ValueError("Channel %s is not a GPIO" % str(channel))
    if need_pwm and ch_info.pwm_chip_dir is None:
        raise ValueError("Channel %s is not a PWM" % str(channel))
    return ch_info


# lock object for thread
_mutex = thread.allocate_lock()
# value = GPIO class object
_gpio_event_list = dict()
# epoll thread object
_epoll_fd_thread = None
# variable to keep track of thread state
_thread_running = False
def _get_gpio_obj_key(fd):
    for key in _gpio_event_list:
        if _gpio_event_list[key].value_fd == fd:
            return key
    return None
def _get_gpio_file_object(fileno):
    for key in _gpio_event_list:
        if _gpio_event_list[key].value_fd.fileno() == fileno:
            return _gpio_event_list[key].value_fd
    return None
def _poll_thread():
    global _thread_running

    _thread_running = True
    while _thread_running:
        try:
            events = _epoll_fd_thread.poll(maxevents=1)
            fd = events[0][0]
            _mutex.acquire()

            # check if file object has been deleted or closed from main thread
            fd = _get_gpio_file_object(fd)
            if fd is None or fd.closed:
                _mutex.release()
                continue

            # read file to make sure event is valid
            fd.seek(0)
            if len(fd.read().rstrip()) != 1:
                _thread_running = False
                _mutex.release()
                thread.exit()

            # check key to make sure gpio object has not been deleted
            # from main thread
            key = _get_gpio_obj_key(fd)
            if key is None:
                _mutex.release()
                continue

            gpio_obj = _gpio_event_list[key]

            # ignore first epoll trigger
            if gpio_obj.initial_thread:
                gpio_obj.initial_thread = False
                _gpio_event_list[key] = gpio_obj
                _mutex.release()

            else:
                # debounce the input event for the specified bouncetime
                time = datetime.now()
                time = time.second * 1E6 + time.microsecond
                if (gpio_obj.bouncetime is None or
                        (time - gpio_obj.lastcall >
                         gpio_obj.bouncetime * 1000) or
                        (gpio_obj.lastcall == 0) or gpio_obj.lastcall > time):
                    gpio_obj.lastcall = time
                    gpio_obj.event_occurred = True
                    _gpio_event_list[key] = gpio_obj
                    _mutex.release()
                    for cb_func in gpio_obj.callbacks:
                        cb_func()

        # if interrupted by a signal, continue to start of the loop
        except InterruptedError:
            if _mutex.locked():
                _mutex.release()
            continue
        except AttributeError:
            break
    thread.exit()

class SYSFSGPIO(object):
    _SYSFS_ROOT = '/sys/class/gpio'
    # Edge possibilities
    NO_EDGE = 0
    RISING_EDGE = 1
    FALLING_EDGE = 2
    BOTH_EDGE = 3
    # string representations for edges to write to sysfs
    _edge_str = ["none", "rising", "falling", "both"]
    def __init__(self, pin, direction=None):
        self.ch_info = _channel_to_info(pin, need_gpio=True)
        self.pin = self.ch_info.pin

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, t, value, traceback):
        self.close()

    def close(self):
        pin = self.pin
        self._line_fd = self._SYSFS_ROOT + "/gpio%i" % pin
        try:
            if self._line_fd is not None:
                os.close(self._line_fd)
        except OSError as e:
            raise GPIOError(e.errno, "Closing GPIO line: " + e.strerror)
        unexport_gpio()
        self._line_fd = None
        self.edge = "none"
        self.direction = "in"
        self.pin = None
    def export_gpio(self):
        pin = self.pin
        if os.path.exists(self._SYSFS_ROOT + "/gpio%i" % pin):
            return
        with open(self._SYSFS_ROOT + "/export", "w") as f_export:
            f_export.write(str(pin))
        while not os.path.exists(self._SYSFS_ROOT + "/gpio%i" % pin):
            time.sleep(0.1)
    def unexport_gpio(self):
        pin = self.pin
        if not os.path.exists(self._SYSFS_ROOT + "/gpio%i" % pin):
            return
        with open(self._SYSFS_ROOT + "/unexport", "w") as f_unexport:
            f_unexport.write(str(pin))
    def setup_out(self):
        pin = self.pin
        self.export_gpio()
        gpio_dir_path = self._SYSFS_ROOT + "/gpio%i" % pin + "/direction"
        with open(gpio_dir_path, 'w') as direction_file:
            direction_file.write("out")
    def setup_in(self):
        pin = self.pin
        self.export_gpio()
        gpio_dir_path = self._SYSFS_ROOT + "/gpio%i" % pin + "/direction"
        with open(gpio_dir_path, 'w') as direction:
            direction.write("in")
    def write_one(self, value):
        pin = self.pin
        with open(self._SYSFS_ROOT + "/gpio%s" % pin + "/value", 'w') as value_file:
            value_file.write(str(int(bool(value))))
    def read_one(self):
        pin = self.pin
        with open(self._SYSFS_ROOT + "/gpio%i" % pin + "/value") as value:
            value_read = int(value.read())
        return value_read
    def gpio_event_added(self):
        pin = self.pin
        if pin not in _gpio_event_list:
            return self.NO_EDGE
        return _gpio_event_list[pin].edge
    def get_gpio_object(self):
        if self.pin not in _gpio_event_list:
            return None
        return _gpio_event_list[self.pin]
    def set_edge(self):
        pin = self.pin
        edge = self.edge
        edge_path = self._SYSFS_ROOT + "/gpio%i" % pin + "/edge"
        with open(edge_path, 'w') as edge_file:
            edge_file.write(self._edge_str[edge])
    def add_edge_detect(self):
        global _epoll_fd_thread
        gpios = None
        res = self.gpio_event_added()

        # event not added
        if self.NO_EDGE == res:
            gpios = _Gpios(self.pin, self.edge, self.bouncetime)
            self.set_edge()

        # event already added
        elif self.edge == res:
            gpios = self.get_gpio_object()
            if ((self.bouncetime is not None and gpios.bouncetime != self.bouncetime) or
                    gpios.thread_added):
                return 1
        else:
            return 1
        # create epoll object for fd if not already open
        if _epoll_fd_thread is None:
            _epoll_fd_thread = epoll()
            if _epoll_fd_thread is None:
                return 2

        # add eventmask and fd to epoll object
        try:
            _epoll_fd_thread.register(gpios.value_fd, EPOLLIN | EPOLLET | EPOLLPRI)
        except IOError:
            self.remove_edge_detect()
            return 2

        gpios.thread_added = 1
        _gpio_event_list[self.pin] = gpios

        # create and start poll thread if not already running
        if not _thread_running:
            try:
                thread.start_new_thread(_poll_thread, ())
            except RuntimeError:
                self.remove_edge_detect()
                return 2
        return 0
    # Function used to add threaded event detection for a specified gpio channel.
    # Param gpio must be an integer specifying the channel, edge must be RISING,
    # FALLING or BOTH. A callback function to be called when the event is detected
    # and an integer bounctime in milliseconds can be optionally provided
    def add_event_detect(self, pin, edge, callback=None, bouncetime=None):

        self.bouncetime = bouncetime
        self.edge = edge
        self.callback = callback
        # edge must be rising, falling or both
        # if edge != RISING and edge != FALLING and edge != BOTH:
        #     raise ValueError("The edge must be set to RISING, FALLING, or BOTH")

        # if bouncetime is provided, it must be int and greater than 0
        if self.bouncetime is not None:
            if type(self.bouncetime) != int:
                raise TypeError("bouncetime must be an integer")

            elif self.bouncetime < 0:
                raise ValueError("bouncetime must be an integer greater than 0")
        
        result = self.add_edge_detect()

        # result == 1 means a different edge was already added for the channel.
        # result == 2 means error occurred while adding edge (thread or event poll)
        if result:
            error_str = None
            if result == 1:
                error_str = "Conflicting edge already enabled for this GPIO " + \
                            "channel"
            else:
                error_str = "Failed to add edge detection"

            raise RuntimeError(error_str)

        if callback is not None:
            self.add_edge_callback(lambda: callback(self.pin))
    def add_edge_callback(self, callback):
        if self.pin not in _gpio_event_list or not _gpio_event_list[self.pin].thread_added:
            return
        _gpio_event_list[self.pin].callbacks.append(callback)
    def remove_edge_detect(self):
        if self.pin not in _gpio_event_list:
            return

        if _epoll_fd_thread is not None:
            _epoll_fd_thread.unregister(_gpio_event_list[self.pin].value_fd)

        self.set_edge()

        _mutex.acquire()
        del _gpio_event_list[self.pin]
        _mutex.release()

class GPIO(object):

    # GPIO directions. UNKNOWN constant is for gpios that are not yet setup
    UNKNOWN = -1
    OUT = 0
    IN = 1
    DIR = None
    # Edge possibilities
    # These values (with _EDGE_OFFSET subtracted) must match gpio_event.py:*_EDGE
    _EDGE_OFFSET = 30
    RISING = 1 + _EDGE_OFFSET
    FALLING = 2 + _EDGE_OFFSET
    BOTH = 3 + _EDGE_OFFSET
    RPI_REVISION = NPi_i_MX6ULL
    def __init__(self, pin, direction=None):
        self.pin = pin
        self.gpio = SYSFSGPIO(self.pin)
        # self.pin = self.gpio.ch_info

        if direction is not None:
            self.dir(direction)
        self._event_handle = None

    def dir(self, direction):
        # check direction is valid
        if direction != self.OUT and direction != self.IN:
            raise ValueError("An invalid direction was passed to setup()")
        self.DIR = direction
        if self.DIR == self.OUT:
            self.gpio.setup_out()
        elif self.DIR == self.IN:
            self.gpio.setup_in()

    def write(self, output):
        if self.OUT != self.DIR:
            raise RuntimeError("You must dir() the GPIO channel as an "
                            "output first")
        self.gpio.write_one(output)

    def read(self):
        return self.gpio.read_one()

    def _on_event(self,pin):
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
            assert self.IN == self.DIR , "You must dir() the GPIO channel as an input first"
            self.gpio.add_event_detect(self.pin, self.BOTH - self._EDGE_OFFSET, self._on_event)
        self._event_handle = handle
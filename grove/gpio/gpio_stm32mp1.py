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
import ctypes
import fcntl
import collections
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
# - Linux GPIO line number,
# - GPIO dev gpiochip directory
# - Pin number (BOARD mode)
# - Pin number (BCM mode)
# - PWM chip sysfs directory
# - PWM ID within PWM chip
# The values are use to generate dictionaries that map the corresponding pin
# mode numbers to the Linux GPIO pin number and GPIO chip directory
STM32MP1 = 'STM32MP1'
BCM = 3
BOARD = 2
STM32MP1_PIN_DEFS = [
    (12, '/dev/gpiochip7', 3,  2,  None, None), #H12
    (8,  '/dev/gpiochip1', 5,  3,  None, None), #B8
    (14, '/dev/gpiochip0', 7,  4,  None, None), #A14
    (5,  '/dev/gpiochip5', 8,  14, None, None), #F5
    (6,  '/dev/gpiochip3', 10, 15, None, None), #D6
    (4,  '/dev/gpiochip3', 11, 17, None, None), #D4
    (10, '/dev/gpiochip1', 12, 18, None, None), #B10
    (10, '/dev/gpiochip4', 13, 27, None, None), #E10
    (2,  '/dev/gpiochip1', 15, 22, None, None), #B2
    (0,  '/dev/gpiochip2', 16, 23, None, None), #C0
    (7,  '/dev/gpiochip4', 18, 24, None, None), #E7
    (9,  '/dev/gpiochip5', 19, 10, None, None), #F9
    (7,  '/dev/gpiochip7', 21, 9,  None, None), #H7
    (8,  '/dev/gpiochip4', 22, 25, None, None), #E8
    (6,  '/dev/gpiochip7', 23, 11, None, None), #H6
    (6,  '/dev/gpiochip5', 24, 8,  None, None), #F6
    (3,  '/dev/gpiochip5', 26, 7,  None, None), #F3
    (15, '/dev/gpiochip5', 27, 0,  None, None), #F15
    (14, '/dev/gpiochip5', 28, 1,  None, None), #F14
    (3,  '/dev/gpiochip0', 29, 5,  None, None), #A3
    (14, '/dev/gpiochip4', 31, 6,  None, None), #E14
    (14, '/dev/gpiochip3', 32, 12, '/sys/class/pwm/pwmchip6', 0), #D14
    (15, '/dev/gpiochip3', 33, 13, '/sys/class/pwm/pwmchip7', 0), #D15
    (12, '/dev/gpiochip1', 35, 19, None, None), #B12
    (15, '/dev/gpiochip4', 36, 16, None, None), #E15
    (9,  '/dev/gpiochip4', 37, 26, None, None), #E9
    (2,  '/dev/gpiochip8', 38, 20, None, None), #I2
    (3,  '/dev/gpiochip2', 40, 21, None, None)  #C3
]
class ChannelInfo(object):
    def __init__(self, channel, gpio_chip_dir, pin, pwm_chip_dir, pwm_id):
        self.channel = channel
        self.gpio_chip_dir = gpio_chip_dir
        self.pin = pin
        self.pwm_chip_dir = pwm_chip_dir
        self.pwm_id = pwm_id
class _Gpios:
    def __init__(self, gpio, edge=None, bouncetime=None):
        self.edge = edge
        self.value_fd = None
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

class _CGpiochipInfo(ctypes.Structure):
    _fields_ = [
        ('name', ctypes.c_char * 32),
        ('label', ctypes.c_char * 32),
        ('lines', ctypes.c_uint32),
    ]


class _CGpiolineInfo(ctypes.Structure):
    _fields_ = [
        ('line_offset', ctypes.c_uint32),
        ('flags', ctypes.c_uint32),
        ('name', ctypes.c_char * 32),
        ('consumer', ctypes.c_char * 32),
    ]


class _CGpiohandleRequest(ctypes.Structure):
    _fields_ = [
        ('lineoffsets', ctypes.c_uint32 * 64),
        ('flags', ctypes.c_uint32),
        ('default_values', ctypes.c_uint8 * 64),
        ('consumer_label', ctypes.c_char * 32),
        ('lines', ctypes.c_uint32),
        ('fd', ctypes.c_int),
    ]


class _CGpiohandleData(ctypes.Structure):
    _fields_ = [
        ('values', ctypes.c_uint8 * 64),
    ]


class _CGpioeventRequest(ctypes.Structure):
    _fields_ = [
        ('lineoffset', ctypes.c_uint32),
        ('handleflags', ctypes.c_uint32),
        ('eventflags', ctypes.c_uint32),
        ('consumer_label', ctypes.c_char * 32),
        ('fd', ctypes.c_int),
    ]


class _CGpioeventData(ctypes.Structure):
    _fields_ = [
        ('timestamp', ctypes.c_uint64),
        ('id', ctypes.c_uint32),
    ]
def get_data():

    pin_defs = STM32MP1_PIN_DEFS

    def model_data(key_col, pin_defs):
        return {x[key_col]: ChannelInfo(
            x[key_col],
            x[1],
            x[0],
            x[4],
            x[5]) for x in pin_defs}
    channel_data = model_data(BCM, pin_defs)
    return  channel_data
CHANNEL_DATA = get_data()

def _channel_to_info(channel, need_gpio=False, need_pwm=False):
    if channel not in CHANNEL_DATA:
        raise ValueError("Channel %s is invalid" % str(channel))
    ch_info = CHANNEL_DATA[channel]
    if need_gpio and ch_info.gpio_chip_dir is None:
        raise ValueError("Channel %s is not a GPIO" % str(channel))
    if need_pwm and ch_info.pwm_chip_dir is None:
        raise ValueError("Channel %s is not a PWM" % str(channel))
    return ch_info

class GPIOError(IOError):
    """Base class for GPIO errors."""
    pass
class EdgeEvent(collections.namedtuple('EdgeEvent', ['edge', 'timestamp'])):
    def __new__(cls, edge, timestamp):
        """EdgeEvent containing the event edge and event time reported by Linux.
        Args:
            edge (str): event edge, either "rising" or "falling".
            timestamp (int): event time in nanoseconds.
        """
        return super(EdgeEvent, cls).__new__(cls, edge, timestamp)



class CDEVGPIO(object):
    # Constants scraped from <linux/gpio.h>
    _GPIOHANDLE_GET_LINE_VALUES_IOCTL = 0xc040b408
    _GPIOHANDLE_SET_LINE_VALUES_IOCTL = 0xc040b409
    _GPIO_GET_CHIPINFO_IOCTL = 0x8044b401
    _GPIO_GET_LINEINFO_IOCTL = 0xc048b402
    _GPIO_GET_LINEHANDLE_IOCTL = 0xc16cb403
    _GPIO_GET_LINEEVENT_IOCTL = 0xc030b404
    _GPIOHANDLE_REQUEST_INPUT = 0x1
    _GPIOHANDLE_REQUEST_OUTPUT = 0x2
    _GPIOEVENT_REQUEST_RISING_EDGE = 0x1
    _GPIOEVENT_REQUEST_FALLING_EDGE = 0x2
    _GPIOEVENT_REQUEST_BOTH_EDGES = 0x3
    _GPIOEVENT_EVENT_RISING_EDGE = 0x1
    _GPIOEVENT_EVENT_FALLING_EDGE = 0x2
    # GPIO directions. UNKNOWN constant is for gpios that are not yet setup
    OUT = 0
    IN = 1
    DIR = None
    _direction_str = ['out','in']
    # Edge possibilities
    NO_EDGE = 0
    RISING_EDGE = 1
    FALLING_EDGE = 2
    BOTH_EDGE = 3
    # string representations for edges to write to sysfs
    _edge_str = ["none", "rising", "falling", "both"]
    _gpio_event_dict = dict()
    # epoll thread object
    _epoll_fd_thread = None
    # variable to keep track of thread state
    _thread_running = False
    # lock object for thread
    _mutex = thread.allocate_lock()
    def __init__(self, pin):
        self.ch_info = _channel_to_info(pin, need_gpio=True)
        self.pin = pin
        self._line_fd = None
        # self._line = self.ch_info.pin
        self._chip_fd = None
        self._devpath = None
        # self.ch_info.gpio_chip_dir
        self._open()
    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, t, value, traceback):
        self.close()

    def close(self):
        try:
            if self._line_fd is not None:
                os.close(self._line_fd)
        except OSError as e:
            raise GPIOError(e.errno, "Closing GPIO line: " + e.strerror)

        try:
            if self._chip_fd is not None:
                os.close(self._chip_fd)
        except OSError as e:
            raise GPIOError(e.errno, "Closing GPIO chip: " + e.strerror)

        self._line_fd = None
        self._chip_fd = None
        self._edge = "none"
        self._direction = "in"
        self._line = None

    def _open(self):
        if not isinstance(self.ch_info.gpio_chip_dir, str):
            raise TypeError("Invalid path type, should be string.")
        if not isinstance(self.ch_info.pin, int):
            raise TypeError("Invalid line type, should be integer.")
        # Open GPIO chip
        try:
            self._chip_fd = os.open(self.ch_info.gpio_chip_dir, 0)
        except OSError as e:
            raise GPIOError(e.errno, "Opening GPIO chip: " + e.strerror)
        self._devpath = self.ch_info.gpio_chip_dir
        self._line = self.ch_info.pin
        self._reopen()
    def _reopen(self, direction = OUT ,edge = 'none'):
        self.DIR = direction
        # Close existing line
        if self._line_fd is not None:
            try:
                os.close(self._line_fd)
            except OSError as e:
                raise GPIOError(e.errno, "Closing existing GPIO line: " + e.strerror)
        if self._direction_str[direction] == "in":
            if edge == "none":
                request = _CGpiohandleRequest()

                request.lineoffsets[0] = self._line
                request.flags = CDEVGPIO._GPIOHANDLE_REQUEST_INPUT
                request.consumer_label = b"periphery"
                request.lines = 1

                try:
                    fcntl.ioctl(self._chip_fd, CDEVGPIO._GPIO_GET_LINEHANDLE_IOCTL, request)
                except (OSError, IOError) as e:
                    raise GPIOError(e.errno, "Opening input line handle: " + e.strerror)

                self._line_fd = request.fd
                self._direction = "in"
                self._edge = "none"
            else:
                request = _CGpioeventRequest()

                request.lineoffset = self._line
                request.handleflags = CDEVGPIO._GPIOHANDLE_REQUEST_INPUT
                request.eventflags = CDEVGPIO._GPIOEVENT_REQUEST_RISING_EDGE if \
edge == "rising" else CDEVGPIO._GPIOEVENT_REQUEST_FALLING_EDGE if edge == "falling" else CDEVGPIO._GPIOEVENT_REQUEST_BOTH_EDGES
                request.consumer_label = b"periphery"

                try:
                    fcntl.ioctl(self._chip_fd, CDEVGPIO._GPIO_GET_LINEEVENT_IOCTL, request)
                except (OSError, IOError) as e:
                    raise GPIOError(e.errno, "Opening input line event handle: " + e.strerror)
                self._line_fd = request.fd
                self._direction = "in"
                self._edge = edge
        else:
            request = _CGpiohandleRequest()

            request.lineoffsets[0] = self._line
            request.flags = CDEVGPIO._GPIOHANDLE_REQUEST_OUTPUT
            request.default_values[0] = False
            request.consumer_label = b"periphery"
            request.lines = 1

            try:
                fcntl.ioctl(self._chip_fd, CDEVGPIO._GPIO_GET_LINEHANDLE_IOCTL, request)
            except (OSError, IOError) as e:
                raise GPIOError(e.errno, "Opening output line handle: " + e.strerror)

            self._line_fd = request.fd
            self._direction = "out"
            self._edge = "none"
    def write_one(self, output):
        output = bool(output)
        if self.DIR != self.OUT:
            raise RuntimeError("You must dir() the GPIO channel as an "
                "output first")
        data = _CGpiohandleData()
        data.values[0] = output
        try:
            fcntl.ioctl(self._line_fd, CDEVGPIO._GPIOHANDLE_SET_LINE_VALUES_IOCTL, data)
        except (OSError, IOError) as e:
            raise GPIOError(e.errno, "Setting line value: " + e.strerror)
    def read_one(self):
        data = _CGpiohandleData()
        
        try:
            fcntl.ioctl(self._line_fd, CDEVGPIO._GPIOHANDLE_GET_LINE_VALUES_IOCTL, data)
        except (OSError, IOError) as e:
            raise GPIOError(e.errno, "Getting line value: " + e.strerror)

        return bool(data.values[0])

    def read_event(self):
        if self._edge == "none":
            raise GPIOError(None, "Invalid operation: GPIO edge not set")

        try:
            buf = os.read(self._line_fd, ctypes.sizeof(_CGpioeventData))
        except OSError as e:
            raise GPIOError(e.errno, "Reading GPIO event: " + e.strerror)

        event_data = _CGpioeventData.from_buffer_copy(buf)

        if event_data.id == CDEVGPIO._GPIOEVENT_EVENT_RISING_EDGE:
            edge = "rising"
        elif event_data.id == CDEVGPIO._GPIOEVENT_EVENT_FALLING_EDGE:
            edge = "falling"
        else:
            edge = "none"

        return edge
    def _get_gpio_obj_key(self,fd):
        for key in self._gpio_event_dict:
            if self._gpio_event_dict[key].value_fd == fd:
                return key
        return None
    def _gpio_event_added(self):
        pin = self.pin
        if pin not in self._gpio_event_dict:
            return self.NO_EDGE
        return self._gpio_event_dict[pin].edge
    def get_gpio_object(self):
        if self.pin not in self._gpio_event_dict:
            return None
        return self._gpio_event_dict[self.pin]
    def remove_edge_detect(self):
        if self.pin not in self._gpio_event_dict:
            return

        if self._epoll_fd_thread is not None:
            self._epoll_fd_thread.unregister(self._gpio_event_dict[self.pin].value_fd)

        self._mutex.acquire()
        del self._gpio_event_dict[self.pin]
        self._mutex.release()
    def add_edge_detect(self):
        gpios = None
        res = self._gpio_event_added()

        # event not added
        if self.NO_EDGE == res:
            gpios = _Gpios(self.pin, self._edge, self.bouncetime)
            gpios.value_fd = self._line_fd
        # event already added
        elif self._edge == res:
            gpios = self.get_gpio_object()
            if ((self.bouncetime is not None and gpios.bouncetime != self.bouncetime) or
                    gpios.thread_added):
                return 1
        else:
            return 1
        # create epoll object for fd if not already open
        if self._epoll_fd_thread is None:
            self._epoll_fd_thread = epoll()
            if self._epoll_fd_thread is None:
                return 2

        # add eventmask and fd to epoll object
        try:
            self._epoll_fd_thread.register(gpios.value_fd, EPOLLIN | EPOLLET | EPOLLPRI)
        except IOError:
            self.remove_edge_detect()
            return 2

        gpios.thread_added = 1
        self._gpio_event_dict[self.pin] = gpios

        # create and start poll thread if not already running
        if not self._thread_running:
            try:
                thread.start_new_thread(self._poll_thread, ())
            except RuntimeError:
                self.remove_edge_detect()
                return 2
        return 0
    def add_edge_callback(self, callback):
        if self.pin not in self._gpio_event_dict or not self._gpio_event_dict[self.pin].thread_added:
            return
        self._gpio_event_dict[self.pin].callbacks.append(callback)
    def add_event_detect(self, pin, edge, callback=None, bouncetime=None):
        if self.IN != self.DIR :
            raise TypeError("You must dir() the GPIO channel as an input first")
        self._edge = self._edge_str[edge]
        self._reopen(self.IN, self._edge)
        self.bouncetime = bouncetime
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
    def _get_gpio_file_object(self,fd):
        for key in self._gpio_event_dict:
            if key == fd:
                return self._gpio_event_dict[key].value_fd
        return None
    def _poll_thread(self):
        self._thread_running = True
        while self._thread_running:
            try:
                events = self._epoll_fd_thread.poll(maxevents=1)
                fd = events[0][0]
                self._mutex.acquire()
                # check if file object has been deleted or closed from main thread
                fd = self._get_gpio_file_object(fd)
                if fd is None:
                    self._mutex.release()
                    continue
                # read file to make sure event is valid
                event = self.read_event()
                if event == "none":
                    self._thread_running = False
                    self._mutex.release()
                    thread.exit()

                # check key to make sure gpio object has not been deleted
                # from main thread
                key = self._get_gpio_obj_key(fd)
                if key is None:
                    self._mutex.release()
                    continue

                gpio_obj = self._gpio_event_dict[key]

                # ignore first epoll trigger
                if gpio_obj.initial_thread:
                    gpio_obj.initial_thread = False
                    self._gpio_event_dict[key] = gpio_obj
                    self._mutex.release()

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
                        self._gpio_event_dict[key] = gpio_obj
                        self._mutex.release()
                        for cb_func in gpio_obj.callbacks:
                            cb_func()
            except AttributeError:
                break
        thread.exit()

        
class GPIO(object):
    # GPIO directions. UNKNOWN constant is for gpios that are not yet setup
    OUT = 0
    IN = 1
    DIR = None
    # Edge possibilities
    # These values (with _EDGE_OFFSET subtracted) must match gpio_event.py:*_EDGE
    _EDGE_OFFSET = 30
    RISING = 1 + _EDGE_OFFSET
    FALLING = 2 + _EDGE_OFFSET
    BOTH = 3 + _EDGE_OFFSET
    RPI_REVISION = STM32MP1
    def __init__(self, pin, direction = OUT):
        self.pin = pin
        self.gpio = CDEVGPIO(self.pin)
        # self.pin = self.gpio.ch_info
        if direction is not None:
            self.dir(direction)
        
        self._event_handle = None

    def dir(self, direction):
        self.gpio._reopen(direction)
    def write(self, output):
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
            self.gpio.add_event_detect(self.pin, self.BOTH - self._EDGE_OFFSET, self._on_event)
        self._event_handle = handle
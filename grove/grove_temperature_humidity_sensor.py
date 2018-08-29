#!/usr/bin/env python

# This is the library for Grove Base Hat which used to connect grove sensors for raspberry pi.
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
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class DHT(object):
    DHT_TYPE = {
        'DHT11': '11',
        'DHT22': '22'
    }

    MAX_CNT = 50

    def __init__(self, dht_type, pin):        
        self.pin = pin
        if dht_type != self.DHT_TYPE['DHT11'] and dht_type != self.DHT_TYPE['DHT22']:
            print('ERROR: Please use 11|22 as dht type.')
            exit(1)
        self._dht_type = '11'
        self.dht_type = dht_type
        GPIO.setup(self.pin, GPIO.OUT)

    @property
    def dht_type(self):
        return self._dht_type

    @dht_type.setter
    def dht_type(self, type):
        self._dht_type = type

    def read(self):
        # Send Falling signal to trigger sensor output data
        # Wait for 20ms to collect 42 bytes data
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, 1)
        sleep(.5)
        GPIO.output(self.pin, 0)
        sleep(.018)
        GPIO.setup(self.pin, GPIO.IN)
        
        data = ''
        collector = []
        total_cnt = 0
        for i in range(42):
            cnt_pulse_high = 0 
            cnt_pulse_low = 0 
            while(GPIO.input(self.pin) and i != 41):
                total_cnt += 1
                cnt_pulse_high += 1
                if cnt_pulse_high > self.MAX_CNT:
                    self.sysExit("Read failed, please check if connection OK.")
            collector.append(cnt_pulse_high)
            
            while(not GPIO.input(self.pin) and i != 41):
                cnt_pulse_low += 1
                if cnt_pulse_low > self.MAX_CNT:
                    self.sysExit("Read failed, please check if connection OK.")
        
        average_cnt = total_cnt / 42
        for i in range(42):
            if collector[i] > average_cnt:
                data += '1'
            else:
                data += '0'
        
        data1 = int(data[2:10], 2)
        data2 = int(data[10:18], 2)
        data3 = int(data[18:26], 2)
        data4 = int(data[26:34], 2)
        data5 = int(data[34:42], 2)

        if self._dht_type == self.DHT_TYPE['DHT11']:
            humi = int(data1)
            temp = int(data3)
        elif self._dht_type == self.DHT_TYPE['DHT22']:
            humi = float(int(data[2:18], 2)*0.1)
            temp = float(int(data[19:34],2)*0.2*(0.5-int(data[18], 2)))

        return humi, temp

    def sysExit(self, exit_code):
        print("Exit: {}".format(exit_code))
        exit(0)

Grove = DHT


def main():
    import sys
    import time

    if len(sys.argv) < 3:
        print('Usage: {} dht_type pin'.format(sys.argv[0]))
        sys.exit(1)

    sensor = DHT(sys.argv[1], int(sys.argv[2]))
    Type = sys.argv[1]
    
    while True:
        humi, temp = sensor.read()
        print('DHT{0}, humidity {1}%, temperature {2}*'.format(Type, humi, temp))
        time.sleep(1)


if __name__ == '__main__':
    main()


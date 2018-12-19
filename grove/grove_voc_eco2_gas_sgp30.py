#!/usr/bin/env python
#
# This is the code for Grove - VOC and eCO2 Gas Sensor (SGP30).
# (https://www.seeedstudio.com/Grove-VOC-and-eCO2-Gas-Sensor-SGP3-p-3071.html)
# which is a digital multi-pixel gas sensor designed for easy integration into air purifier, 
# demand-controlled ventilation, and IoT applications. 
#
# author: Peter Yang <turmary@126.com>
#
# Grove.py is the library for Grove Base Hat which used to
# connect grove sensors for raspberry pi.
#
# Acknowledgement:
# https://github.com/zinob/RPI_SGP30
# Copyright (c) 2018 Simon Albinsson

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
from grove.i2c import Bus
from sgp30 import Sgp30 as GroveVOC_eCO2GasSgp30
import time
import sys

Grove = GroveVOC_eCO2GasSgp30

def sgp30_data_display(reading, elapse):
    co2_eq_ppm, tvoc_ppb = reading.data
    print("\r  tVOC = {} ppb CO2eq = {} ppm elapse = {:8.2f}S ".format(
                             tvoc_ppb, co2_eq_ppm, elapse),
          end = "", file = sys.stderr)
    return


def file_get_modify_time(path):
    import os

    if not os.path.exists(path):
        return None
    fp = unicode(path, 'utf8')
    t = os.path.getmtime(fp)
    return t

def main():
    print(\
""" Make sure Grove-VOC-eCO2-Gas-Sensor(SGP30)
   inserted in one I2C slot of Grove-Base-Hat

Baseline operations reference:
   http://wiki.seeedstudio.com/Grove-VOC_and_eCO2_Gas_Sensor-SGP30/
""")

    # configuration
    baseline_conf = "/tmp/SGP30_baseline"
    # Baseline file used to store baseline compensation parameters.
    sgp = GroveVOC_eCO2GasSgp30(Bus(), baseline_filename = baseline_conf)

    sgp.i2c_geral_call()
    sgp.read_features()
    serial = sgp.read_serial()
    print("SGP30 SERIAL: {}".format(serial.raw))

    # sgp initialize
    sgp.init_sgp()

    # Load baseline if applicable
    t = file_get_modify_time(baseline_conf)
    if not t is None and time.time() - t < 7.0 * 24 * 3600:
        print("Try to set baseline: {}".format(sgp.try_set_baseline()))
    else:
        print("*** Baseline unexist or expired")

    print("First reading: ")
    print("  DATA = {}".format(sgp.read_measurements().data))
    print("SGP30 need at least 15 seconds to warm up")
    for i in range(20):
        time.sleep(1)
        print(".", end = "", file = sys.stderr)
    print()

    print("Has to run for 12 hours to get really stable data/baseline")
    start = time.time()
    while time.time() - start <= 12.0 * 3600:
        reading = sgp.read_measurements()
        sgp30_data_display(reading, time.time() - start)
        time.sleep(0.5)

    print("\nBaseline stored")
    sgp.store_baseline()


if __name__ == '__main__':
    main()

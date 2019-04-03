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
    - `Grove - 2.5A DC current sensor  <https://www.seeedstudio.com/Grove-2-5A-DC-Current-Sensor-ACS70331-p-2929.html>`_
    - `Grove - 5A AC/DC current sensor <https://www.seeedstudio.com/Grove-5A-DC-AC-Current-Sensor-ACS70331-p-2928.html>`_
    - `Grove - 10A current sensor      <https://www.seeedstudio.com/Grove-10A-DC-Current-Sensor-ACS725-p-2927.html>`_

Examples:
    .. code-block:: python

        import time
        from grove_current_sensor import Current

        pin = 0
        sensor_type = "2.5A"

        #if use 10A current sensor input: pin = 0 , sensor_type = "10A"
        if (sensor_type == "2.5A"):
            sensitivity = 1000.0 / 800.0
            Vref = 260
        if (sensor_type == "5A_DC"):
            sensitivity = 1000.0 / 200.0
            Vref = 1498
        if (sensor_type == "5A_AC"):
            sensitivity = 1000.0 / 200.0
            Vref = 1498
        if (sensor_type == "10A"):
            sensitivity = 1000.0 / 264.0
            Vref = 322
        averageValue = 500

        ADC = Current()
        while True:
            pin_voltage = ADC.get_nchan_vol_milli_data(pin)

            if(sensor_type == "5A_AC"):
                current = ADC.get_nchan_AC_current_data(pin,sensitivity,Vref,averageValue)
            else:
                current = ADC.get_nchan_current_data(pin,sensitivity,Vref,averageValue)

            current = round(current)
            print("pin_voltage(mV):")
            print(pin_voltage)
            print("current(mA):")
            print(current)
            print()
            time.sleep(1)
    
'''

import sys
import time
from grove.i2c import Bus

ADC_DEFAULT_IIC_ADDR = 0X04

ADC_CHAN_NUM = 8

REG_RAW_DATA_START = 0X10
REG_VOL_START = 0X20
REG_RTO_START = 0X30

REG_SET_ADDR = 0XC0

__all__ = ['Current','Bus']

class Current():
    '''
    Grove Current Sensor class
    '''

    def __init__(self,bus_num=1,addr=ADC_DEFAULT_IIC_ADDR):
        '''
        Init iic.
        Args: 
            bus_num(int): the bus number
            addr(int): iic address
        '''
        self.bus = Bus(bus_num)
        self.addr = addr
  
    def get_nchan_vol_milli_data(self,n):
        '''
        Get n chanel data with unit mV.
        Args:
            n(int): the adc pin
        Returns: 
            val: voltage value
        '''
        data = self.bus.read_i2c_block_data(self.addr,REG_VOL_START+n,2)
        val = data[1]<<8|data[0]
        return val

    def get_nchan_current_data(self,n,sensitivity,Vref,averageValue):
        '''
        2.5A/5A DC/10A cunrrent sensor get n chanel data with unit mA.
        Args: 
            n(int): the adc pin
            sensitivity(float): The coefficient by which voltage is converted into current
            Vref(int): Initial voltage at no load
            averageValue(int): Average acquisition frequency
        Returns: 
            currentVal: current value
        '''
        val = 0
        for i in range(averageValue):
            data = self.bus.read_i2c_block_data(self.addr,REG_VOL_START+n,2)
            val += data[1]<<8|data[0]
        val = val / averageValue
        currentVal = (val - Vref) * sensitivity
        return currentVal

    def get_nchan_AC_current_data(self,n,sensitivity,Vref,averageValue):
        '''
        5A current sensor AC output and get n chanel data with unit mA.
        Args:
            n(int): the adc pin
            sensitivity(float): The coefficient by which voltage is converted into current
            Vref(int): Initial voltage at no load
            averageValue(int): Average acquisition frequency
        Returns: 
            currentVal: current value
        '''
        sensorValue = 0
        for i in range(averageValue):
            data=self.bus.read_i2c_block_data(self.addr,REG_VOL_START+n,2)
            val=data[1]<<8|data[0]
            if(val > sensorValue):
                sensorValue=val
            time.sleep(0.00004)
        currentVal = ((sensorValue - Vref) * sensitivity)*0.707
        return currentVal   

ADC = Current()
def main():
    pin = int(sys.argv[1])
    sensor_type = sys.argv[2]

    if (sensor_type == "2.5A"):
        sensitivity = 1000.0 / 800.0
        Vref = 260
    if (sensor_type == "5A_DC"):
        sensitivity = 1000.0 / 200.0
        Vref = 1498
    if (sensor_type == "5A_AC"):
        sensitivity = 1000.0 / 200.0
        Vref = 1498
    if (sensor_type == "10A"):
        sensitivity = 1000.0 / 264.0
        Vref = 322
    averageValue = 500
    
    while True:
        pin_voltage = ADC.get_nchan_vol_milli_data(pin)

        if(sensor_type == "5A_AC"):
            current = ADC.get_nchan_AC_current_data(pin,sensitivity,Vref,averageValue)
        else:
            current = ADC.get_nchan_current_data(pin,sensitivity,Vref,averageValue)
        
        current = round(current)
        print("pin_voltage(mV):")
        print(pin_voltage)
        print("current(mA):")
        print(current)
        print()
        time.sleep(1)
    
if __name__ == '__main__':
    main()
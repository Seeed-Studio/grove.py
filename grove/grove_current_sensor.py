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
    - `Grove - 2.5A DC current sensor  <https://www.seeedstudio.com>`_
    - `Grove - 5A AC/DC current sensor <https://www.seeedstudio.com>`_
    - `Grove - 10A current sensor      <https://www.seeedstudio.com>`_
Examples:
    .. code-block:: python
        import time
        from grove.i2c import Bus

        while True:
            # pin number your device plugin
            pin = 0
            # Multiple measurements reduce errors
            averageValue = 500
            
            #IF it's 2.5A current sensor
            sensitivity = 1000.0 / 800.0
            Vref = 260
    
            pin_voltage = ADC.get_nchan_vol_milli_data(pin)
    
            #IF it's 2.5A/5A DC/10A cunrrent sensor   
            current = ADC.get_nchan_current_data(pin,sensitivity,Vref,averageValue)         
    
            current = round(current)
            print("pin_voltage(mV):")
            print(pin_voltage)
            print("current(mA):")
            print(current)
            print
            time.sleep(1)
'''

import time
from grove.i2c import Bus

ADC_DEFAULT_IIC_ADDR = 0X04

ADC_CHAN_NUM = 8

REG_RAW_DATA_START = 0X10
REG_VOL_START = 0X20
REG_RTO_START = 0X30

REG_SET_ADDR = 0XC0

#sensitivity = 1000.0 / 800.0
#Vref = 260              #The value of the sensorValue is read when there is no current load.
#averageValue = 10       #Take the average of 10 times

class Pi_hat_adc():

    def __init__(self,bus_num=1,addr=ADC_DEFAULT_IIC_ADDR):
        self.bus = Bus(bus_num)
        self.addr = addr

    #get n chanel data with unit mv.  
    def get_nchan_vol_milli_data(self,n):
        data = self.bus.read_i2c_block_data(self.addr,REG_VOL_START+n,2)
        val = data[1]<<8|data[0]
        return val

    #2.5A/5A DC/10A cunrrent sensor get n chanel data with unit mA.  
    def get_nchan_current_data(self,n,sensitivity,Vref,averageValue):
        val = 0
        for i in range(averageValue):
            data = self.bus.read_i2c_block_data(self.addr,REG_VOL_START+n,2)
            val += data[1]<<8|data[0]
        val = val / averageValue
        currentVal = (val - Vref) * sensitivity
        return currentVal

    #5A current sensor AC output and get n chanel data with unit mA.  
    def get_nchan_AC_current_data(self,n):
        sensorValue = 0
        for i in range(averageValue):
            data=self.bus.read_i2c_block_data(self.addr,REG_VOL_START+n,2)
            val=data[1]<<8|data[0]
            if(val > sensorValue):
                sensorValue=val
            time.sleep(0.00004)
        currentVal = ((sensorValue - Vref) * sensitivity)*0.707
        return currentVal   

ADC = Pi_hat_adc()
def main():
    while True:
        # pin number your device plugin
        pin = 0
        # Multiple measurements reduce errors
        averageValue = 500
        
        #IF it's 2.5A current sensor
        sensitivity = 1000.0 / 800.0
        Vref = 260

        #IF it's 5A current sensor 
        #sensitivity = 1000.0 / 200.0
        #Vref = 1498

        #IF it's 10A current sensor
        #sensitivity = 1000.0 / 264.0
        #Vref = 322

        pin_voltage = ADC.get_nchan_vol_milli_data(pin)

        #IF it's 2.5A/5A DC/10A cunrrent sensor   
        current = ADC.get_nchan_current_data(pin,sensitivity,Vref,averageValue)         
        #IF it's 5A AC output cunrrent sensor
        #current = ADC.get_nchan_AC_current_data(pin,sensitivity,Vref,averageValue)

        current = round(current)
        print("pin_voltage(mV):")
        print(pin_voltage)
        print("current(mA):")
        print(current)
        print
        time.sleep(1)

if __name__ == '__main__':
    main()
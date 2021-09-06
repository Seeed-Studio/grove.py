import time , sys, math
from adc import ADC
from datetime import date, time, datetime
# Log file
import os.path
import json
 
__all__ = ["OxygenSensor"]
 
VRefer = 3.3
total = 0
Measuredvout = 0
 
class O2Sensor:
 
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()
 
    @property
    def capture(self):
        value = self.adc.read(self.channel)
        if value != 0:
            voltage = value*3.3/1024.0
            sensed_value = voltage* 0.21 *100/ 2.0
            return sensed_value
        else:
            return 0
 
Grove = O2Sensor
 
def main():
    if len(sys.argv) < 2:
        print('Usage: {} adc_channel'.format(sys.argv[0]))
        sys.exit(1)
 
    sensor = O2Sensor(int(sys.argv[1]))
    
    print('Detecting 02 value...')
    time_stamp = datetime.now()
    file_name = '{}{}{}'.format(time_stamp.year, time_stamp.month, time_stamp.day) + '.json'
    clock = '{}:{}:{}'.format(time_stamp.hour, time_stamp.minute, time_stamp.second)
    capture = sensor.capture
    print('{clock} Detected Value: {capture}'.format(clock=clock, capture=capture))

    data = {}
    data[time_stamp] = capture
    with open(file_name, 'w') as file:
        json.dump(data, file)
 
if __name__ == '__main__':
    main() 
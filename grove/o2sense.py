import time , sys, math
from adc import ADC
from datetime import date
 
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
    today = date.today()
    print('Detecting 02 value...')
 
    while True:
        print(today)
        print(time.time())
        print('Detected Value: {0}'.format(sensor.capture))
        time.sleep(1)
 
if __name__ == '__main__':
    main() 
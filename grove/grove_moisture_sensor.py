""""
The driver is for Grove - Moisture Sensor

https://www.seeedstudio.com/Grove-Moisture-Sensor-p-955.html
"""

import math
import sys
import time
from grove.adc import ADC


class GroveMoistureSensor:

    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    @property
    def moisture(self):
        value = self.adc.read(self.channel)
        return value

Grove = GroveMoistureSensor


def main():
    if len(sys.argv) < 2:
        print('Usage: {} adc_channel'.format(sys.argv[0]))
        sys.exit(1)

    sensor = GroveMoistureSensor(int(sys.argv[1]))

    print('Detecting moisture...')
    while True:
        m = sensor.moisture
        if 0 <= m and m < 300:
            result = 'Dry'
        elif 300 <= m and m < 600:
            result = 'Moist'
        else:
            result = 'Wet'
        print('Moisture value: {0}, {1}'.format(m, result))
        time.sleep(1)

if __name__ == '__main__':
    main()

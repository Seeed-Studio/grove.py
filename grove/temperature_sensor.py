
import math
from grove.adc import ADC


class TemperatureSensor:
    B = 4275.
    R0 = 100000.

    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()
    
    @property
    def temperature(self):
        value = self.adc.read(self.channel)
        if value <= 0 or value >= 1000:
            return float('nan')

        r = 1000. / value - 1.
        r = self.R0 * r

        return 1. / (math.log10(r / self.R0) / self.B + 1 / 298.15) - 273.15

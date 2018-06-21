
import smbus2 as smbus


class Bus:
    instance = None

    def __init__(self, bus=None):
        if bus is None:
            bus = 1     # for Pi 2+

        if not bus.instance:
            Bus.instance = smbus.SMBus(bus)

    def __getattr__(self, name):
        return getattr(self.instance, name)



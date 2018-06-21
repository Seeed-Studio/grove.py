
import grove.i2c


# 0x10 ~ 0x17: ADC raw data
# 0x20 ~ 0x27: input voltage
# 0x29: output voltage (Grove power supply voltage)
# 0x30 ~ 0x37: input voltage / output voltage
class ADC(object):
    def __init__(self, address=0x04):
        self.address = address
        self.bus = grove.i2c.Bus()

    def read_raw(self, channel):
        addr = 0x10 + channel
        return self.read_register(addr)

    # read input voltage (mV)
    def read_voltage(self, channel):
        addr = 0x20 + channel
        return self.read_register(addr)

    # input voltage / output voltage (%)
    def read(self, channel):
        addr = 0x30 + channel
        return self.read_register(addr)

    @property
    def name(self):
        id = self.read_register(0x0)
        if id == 0x4:
            return 'Grove Base HAT RPi'
        elif id == 0x5:
            return 'Grove Base HAT RPi Zero'

    @property
    def version(self):
        return self.read_register(0x3)

    # read 16 bits register
    def read_register(self, n):
        self.bus.write_byte(self.address, n)
        return self.bus.read_word_data(self.address, n)


if __name__ == '__main__':
    import time

    adc = ADC()
    while True:
        print(adc.read_voltage(0))
        time.sleep(1)


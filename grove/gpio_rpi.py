
import RPi.GPIO

RPi.GPIO.setmode(RPi.GPIO.BCM)


class GPIO(object):
    OUT = RPi.GPIO.OUT
    IN = RPi.GPIO.IN
    
    def __init__(self, pin):
        self.pin = pin

    def dir(self, direction):
        RPi.GPIO.setup(self.pin, direction)

    def write(self, output):
        RPi.GPIO.output(self.pin, output)

    def read(self):
        return RPi.GPIO.input(self.pin)

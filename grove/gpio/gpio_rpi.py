
import RPi.GPIO

RPi.GPIO.setmode(RPi.GPIO.BCM)


class GPIO(object):
    OUT = RPi.GPIO.OUT
    IN = RPi.GPIO.IN
    
    def __init__(self, pin, direction=None):
        self.pin = pin
        if direction is not None:
            self.dir(direction)

        self._event_handle = None

    def dir(self, direction):
        RPi.GPIO.setup(self.pin, direction)

    def write(self, output):
        RPi.GPIO.output(self.pin, output)

    def read(self):
        return RPi.GPIO.input(self.pin)

    def _on_event(self, pin):
        value = self.read()
        if self._event_handle:
            self._event_handle(pin, value)

    @property
    def on_event(self):
        return self._event_handle

    @on_event.setter
    def on_event(self, handle):
        if self._event_handle is None and callable(handle):
            self._event_handle = handle
            RPi.GPIO.add_event_detect(self.pin, RPi.GPIO.BOTH, self._on_event)


import mraa


class GPIO(mraa.Gpio):
    OUT = mraa.DIR_OUT
    IN = mraa.DIR_IN
    
    def __init__(self, pin, direction=None):
        super(GPIO, self).__init__(pin, raw = True)
        self.pin = pin

        if direction is not None:
            self.dir(direction)

        self._event_handle = None
    
    @staticmethod
    def _on_event(self):
        value = self.read()
        if self._event_handle:
            self._event_handle(self.pin, value)

    @property
    def on_event(self):
        return self._event_handle

    @on_event.setter
    def on_event(self, handle):
        if not callable(handle):
            return
        if self._event_handle is None:
            self.isr(mraa.EDGE_BOTH, self._on_event, self)

        self._event_handle = handle

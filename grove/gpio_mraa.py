
import mraa

class GPIO(object):
    OUT = mraa.DIR_OUT
    IN = mraa.DIR_IN
    
    def __init__(self, pin):
        self.instance = mraa.Gpio(pin)
        
    def __getattr__(self, name):
        return getattr(self.instance, name)
import platform as _platform_
import re

####################### Utils #######################

class _supportBoard:
    RaspberryPi = 0,
    BeagleBone = 1,
    UnKnownBoard = -1


class _utils:
    """
    ## basic adapter
    """
    SUCESS = True
    FAIL = False

    # return any of Windows,Linux etc
    @staticmethod
    def _platform():
        return _platform_.system()

    @staticmethod
    def _tryImport(importStatement: str):
        try:
            exec(importStatement)
            return _utils.SUCESS
        except:
            return _utils.FAIL

    @staticmethod
    def _board():
        # raspberry pi
        if _utils.isRaspberryPi():
            return _supportBoard.RaspberryPi
        elif _utils.isBeagleBone():
            return _supportBoard.BeagleBone
        else:
            return _supportBoard.UnKnownBoard

    @staticmethod
    def isRaspberryPi(cachedInfo=None):
        hardware_regex = r'BCM(\d{4})$' # BCMxxxx
        cpu_info = cachedInfo or _utils.get_cpuinfo()
        is_rpi = bool(re.match(hardware_regex, cpu_info['Hardware']))
        return is_rpi

    @staticmethod
    def isBeagleBone(cachedInfo=None):
        hardware_regex = r'.+AM(.{4})'  # AMxxxx
        cpu_info = cachedInfo or _utils.get_cpuinfo()
        is_rpi = bool(re.match(hardware_regex, cpu_info['Hardware']))
        return is_rpi

    @staticmethod
    def get_cpuinfo():
        info = None
        entry_regex = r'(.+\w)\s*?:\s+?(.*)'
        try:
            # If permissions are correct, no error should occur.
            with open('/proc/cpuinfo', 'r') as rpi_cpu_info:
                cpu_info = rpi_cpu_info.read()

            info = dict(re.findall(entry_regex, cpu_info, re.MULTILINE))
        except:
            pass

        return info


####################### Adapter #######################

class _I2CAdapter:
    """
    ### I2C adapter
    """
    @staticmethod
    def bus():
        """Get Current Platform bus-index"""
        _bus_ = 0
        cpuInfo = _utils.get_cpuinfo()
        # raspberry pi
        if _utils.isRaspberryPi(cpuInfo):
            if _utils._tryImport("import RPi.GPIO as GPIO"):
                import RPi.GPIO as GPIO
                rev = GPIO.RPI_REVISION
            else:
                rev = 3
            if rev == 2 or rev ==3:
                _bus_ = 1 # for Pi 2+
            else:
                _bus_ = 0
        # beaglebone
        elif _utils.isBeagleBone(cpuInfo):
            if _utils._tryImport("import Adafruit_BBIO.GPIO as GPIO"):
                import Adafruit_BBIO.GPIO as GPIO
                _bus_ = 2

        return _bus_


####################### API #######################

class Adapter:
    """
    API Class
    ## Support Platform: [
            RaspberryPi, 
            BeagleBone,
        ]
    """

    # utils
    # class utils(_utils): pass

    # support board list
    class supportBoard(_supportBoard): pass

    # I2C adapter
    class i2c(_I2CAdapter): pass


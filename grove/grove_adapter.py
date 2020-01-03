import platform as _platform_
import re
import subprocess

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
    def bus(port):
        """Get Current Platform bus-index"""
        _bus_ = 0
        cpuInfo = _utils.get_cpuinfo()
        # raspberry pi
        if _utils.isRaspberryPi(cpuInfo):
            if port is None:
                try:
                    import RPi.GPIO as GPIO
                    rev = GPIO.RPI_REVISION
                except:
                    rev = 3
                if rev == 2 or rev ==3:
                    _bus_ = 1 # for Pi 2+
                else:
                    _bus_ = 0
            else:
                _bus_ = port
        # beaglebone
        elif _utils.isBeagleBone(cpuInfo):
            configBBI2CPort = [1, 2]
            if port is None:
                _bus_ = 2
                print("BBBoard Default I2C is I2C-2")
            else:
                _bus_ = port
            if _bus_ not in configBBI2CPort:
                return _bus_

            # config i2c mode
            i2cPinmux = {
                "i2c-1": [("P9_17", "P9_18"), ("P9_24", "P9_26")],
                "i2c-2": [("P9_19", "P9_20"), ("P9_21", "P9_22")]
            }
            i2cModeFmt = "config-pin %s i2c;"
            gpioModeFmt = "config-pin %s gpio;"

            cmd = ""
            key = "i2c-%s" % str(_bus_)
            i2cPinmuxTuple = i2cPinmux[key][0]
            gpioPinmuxTuple = i2cPinmux[key][1]
            try:
                # auto check current pinmux
                checkRes = []
                import Adafruit_BBIO.GPIO as GPIO
                for pinmuxTuple in i2cPinmux[key]:
                    GPIO.setup(pinmuxTuple[0], GPIO.IN)
                    GPIO.setup(pinmuxTuple[1], GPIO.IN)
                    checkRes.append(
                        GPIO.input(pinmuxTuple[0]) & 
                        GPIO.input(pinmuxTuple[1])
                    )
                if checkRes[0] == 0 and checkRes[1] == 1:
                    i2cPinmuxTuple = i2cPinmux[key][1] 
                    gpioPinmuxTuple = i2cPinmux[key][0]
            except:
                pass
            cmd += i2cModeFmt % i2cPinmuxTuple[0]
            cmd += i2cModeFmt % i2cPinmuxTuple[1]
            cmd += gpioModeFmt % gpioPinmuxTuple[0]
            cmd += gpioModeFmt % gpioPinmuxTuple[1]
            # print(cmd)
            subprocess.Popen(cmd, shell=True).wait()

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



try:
    from grove.gpio.gpio_rpi import GPIO
except ImportError:
    print('RPi.GPIO is not available. Try to use MRAA')
    try:
        from grove.gpio.gpio_mraa import GPIO
    except ImportError:
        from grove.gpio.gpio_debian import GPIO
from grove.gpio.wrapper import GPIOWrapper

__all__ = ['GPIO', 'GPIOWrapper']


try:
    from grove.gpio.gpio_rpi import GPIO
except ImportError:
    from grove.gpio.gpio_linux import GPIO
from grove.gpio.wrapper import GPIOWrapper

__all__ = ['GPIO', 'GPIOWrapper']

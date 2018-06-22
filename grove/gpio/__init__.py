
try:
    from grove.gpio_rpi import GPIO
except ImportError:
    print('RPi.GPIO is not available. Try to use MRAA')
    from grove.gpio_mraa import GPIO


compats_imx6ull = (
    'fsl,imx6ull-14x14-evkfsl',
    'fsl,imx6ull',
)

def matches(vals):
    compatible_path = '/proc/device-tree/compatible'
    with open(compatible_path, 'r') as f:
        compatibles = f.read().split('\x00')
    return any(v in compatibles for v in vals)

try:
    from grove.gpio.gpio_rpi import GPIO
except ImportError:
    if matches(compats_imx6ull):
        from grove.gpio.gpio_mx6ull import GPIO
    else:
        raise Exception('Could not determine model')
from grove.gpio.wrapper import GPIOWrapper

__all__ = ['GPIO', 'GPIOWrapper']

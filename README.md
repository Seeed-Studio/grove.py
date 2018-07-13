grove.py
========

[![Build Status](https://travis-ci.org/Seeed-Studio/grove.py.svg?branch=master)](https://travis-ci.org/Seeed-Studio/grove.py)
[![](https://img.shields.io/pypi/v/grove.py.svg)](https://pypi.python.org/pypi/grove.py)

Python library for Seeedstudio Grove Devices on Raspberry Pi.



### Install grove.py from pypi 
- For Python2
```shell
sudo pip install grove.py
```

- For Python3
```shell
sudo pip3 install grove.py
```
### Install grove.py from source code

```shell
git clone https://github.com/Seeed-Studio/grove.py
cd grove.py
sudo pip install .
```

### Install MRAA and UPM for Raspberry Pi

- Add repository
```
echo "deb https://seeed-studio.github.io/pi_repo/ stretch main" | sudo tee /etc/apt/sources.list.d/seeed.list
```

- Add public GPG key
```
curl https://seeed-studio.github.io/pi_repo/public.key | sudo apt-key add -
```
or
```
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys BB8F40F3
```


- Install MRAA & UPM
```
sudo apt update
sudo apt install python-mraa python-upm
```

### Usage
After installing `grove.py`, A few CLI commands with prefix `grove_` is available, such as `grove_led`, `grove_button`, `grove_ultrasonic_ranger` and etc. For I2C Grove devices, the default bus is used (I2C 1 on Pi). For digital input & output Grove devices, pin numbers should be provided as the arguments of these commands.

```shell
grove_i2c_color_sensor_v2
grove_led 12
grove_button 22
grove_ultrasonic_sensor 12 13
```

#### For digital output device like Grove - LED
```python
import time
from grove.grove_led import GroveLed

led = GroveLed(12)

while True:
    led.on()
    time.sleep(1)
    led.off()
    time.sleep(1)
```

#### For digital input device like Grove - Button
```python
import time
from grove.grove_button import GroveButton

button = GroveButton(12)

def on_press(t):
    print('Button is pressed')

button.on_press = on_press

while True:
    time.sleep(1)

```

#### Basic GPIO Input & Output
```python
import time
from grove.gpio import GPIO

led = GPIO(12, GPIO.IN)
button = GPIO(22, GPIO.OUT)

def on_button_event(pin, value):
    print('pin {} is {}'.format(pin, value))
    led.write(value)

button.on_event = on_button_event

while True:
    time.sleep(1)

```

#### For Grove 4 Digit Display
```python
import time
from grove.grove_4_digit_display import Grove4DigitDisplay

display = Grove4DigitDisplay(12, 13))

count = 0
while True:
    t = time.strftime("%H%M", time.localtime(time.time()))
    display.show(t)
    display.set_colon(count & 1)
    count += 1
    time.sleep(1)
```

#### For Grove I2C Color Sensor V2
```python
import time
from grove.grove_i2c_color_sensor_v2 import GroveI2CColorSensorV2
sensor = GroveI2cColorSensorV2()

print('Raw data of red-filtered, green-filtered, blue-filtered and unfiltered photodiodes')
while True:
    # r, g, b = sensor.rgb
    r, g, b, clear = sensor.raw
    print((r, g, b, clear))
    time.sleep(1.0)
```
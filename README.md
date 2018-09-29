grove.py
========

[![Build Status](https://travis-ci.org/Seeed-Studio/grove.py.svg?branch=master)](https://travis-ci.org/Seeed-Studio/grove.py)
[![](https://img.shields.io/pypi/v/grove.py.svg)](https://pypi.python.org/pypi/grove.py)

Python library for Seeedstudio Grove Devices on Raspberry Pi.

<br><br>
# Archtecture
To operate grove sensors, the grove.py depends many hardware interface libraries such as mraa/smbus2/rpi.gpi/rpi_ws281x. 

<br>

![](images/grove-py-arch.png)

<br><br>
# Installation
### Install Dependencies
#### Install MRAA and UPM for Raspberry Pi

- Add repository

```shell
echo "deb https://seeed-studio.github.io/pi_repo/ stretch main" | sudo tee /etc/apt/sources.list.d/seeed.list
```

- Add public GPG key

```shell
curl https://seeed-studio.github.io/pi_repo/public.key | sudo apt-key add -
```
or

```shell
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys BB8F40F3
```

- Install MRAA & UPM

```shell
sudo apt update
# Python2
sudo apt install python-mraa python-upm
# Python3
sudo apt install python3-mraa python3-upm
```

#### Install library raspberry-gpio-python
```shell
sudo apt update
sudo apt install python-rpi.gpio python3-rpi.gpio
```

#### Install library rpi_ws281x
```shell
sudo pip install rpi_ws281x
sudo pip3 install rpi_ws281x
```

<br>

### Install grove.py
#### From PyPI
- For Python2

```shell
sudo pip install grove.py
```

- For Python3

```shell
sudo pip3 install grove.py
```
#### From source code
```shell
git clone https://github.com/Seeed-Studio/grove.py
cd grove.py
# Python2
sudo pip install .
# Python3
sudo pip3 install .
```

<br>

### Online install
install/update all dependencies and latest grove.py
```shell
curl -sL https://github.com/Seeed-Studio/grove.py/raw/master/install.sh | sudo bash -s -
```

<br><br>
# Usage
## CLI(command line interface)
After installing `grove.py`, A few CLI commands with prefix `grove_` is available, such as `grove_led`, `grove_button`, `grove_ultrasonic_ranger` and etc. For I2C Grove devices, the default bus is used (I2C 1 on Pi). For digital input & output Grove devices, pin numbers should be provided as the arguments of these commands.

```shell
sudo grove_pwm_buzzer
grove_i2c_color_sensor_v2
grove_led 12
grove_button 22
grove_ultrasonic_sensor 12 13
......
```

### Temperature Sensor
```shell
grove_temperature_sensor
```

### Thumb Joystick
```shell
grove_thumb_joystick
```

### I2C High Accuracy Temperature Sensor(MCP9808)
```shell
grove_high_accuracy_temperature
```

### Mech Keycap
```shell
grove_mech_keycap
```

### Red/Yellow/Blue LED Button
```shell
# single click to light on
# double click to blink
# long press   to light off
grove_ryb_led_button
```

<br><br>
## GUI(graphical user interface)
You can copy below codes directly, and paste into any Python IDE (such as Thonny Python IDE) to run the demo and see the effect.
### Grove - LED
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

### Relay
```python
import time
from grove.factory import Factory

relay = Factory.getGpioWrapper("Relay",16)
while True:
    relay.on()
    time.sleep(2)
    relay.off()
    time.sleep(5)
```

### Button
```python
import time
from grove.factory import Factory

pin = 12
button = Factory.getButton("GPIO-HIGH", pin)

while True:
    if button.is_pressed():
        print('Button is pressed')
    else:
        print('Button is released')
    time.sleep(1)
```

### Basic GPIO Input & Output
```python
import time
from grove.gpio import GPIO

led = GPIO(12, GPIO.OUT)
button = GPIO(22, GPIO.IN)

while True:
    if button.read():
        led.write(1)
    else:
        led.write(0)
    time.sleep(0.1)
```

### PIR Motion Sensor
#### mini PIR motion sensor
```python
import time
from grove.factory import Factory

### connect to pin 5(slot D5)
pir = Factory.getGpioWrapper("PIRMotion", 5)
while True:
    if pir.has_motion():
        print("Hi, people is moving")
    else:
        print("Watching")
    time.sleep(1)
```

### Buzzer
```python
import time
from grove.factory import Factory

buzzer = Factory.getGpioWrapper("Buzzer", 12)
while True:
    buzzer.on()
    time.sleep(1)
    buzzer.off()
    time.sleep(3)
```

### Electromagnet
```python
import time
from grove.factory import Factory

magnet = Factory.getGpioWrapper("Electromagnet", 12)
while True:
    magnet.on()
    time.sleep(1)
    magnet.off()
    time.sleep(3)
```

### 4 Digit Display
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

### I2C Color Sensor V2
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

### I2C Motor Driver
use along with DC-Motor
```python
import time
from grove.grove_i2c_motor_driver import MotorDriver

motor = MotorDriver()
while True:
    # speed range: 0(lowest) - 100(fastest)
    motor.set_speed(100)
    # channel 1 only
    # to set channel 1&2: motor.set_speed(100, 100)

    # direction: True(clockwise), False(anti-clockwise)
    motor.set_dir(True)
    # channel 1 only,
    # to set channel 1&2: motor.set_dir(True, True)

    time.sleep(2)

    motor.set_speed(70)
    motor.set_dir(False)
    time.sleep(2)
```

use along with Stepper Motor 24BYJ48/28BYJ48

connections between 24BYJ48/28BYJ48 and I2C-Motor-Driver
<div>
  <table border="0">
    <tr align="center">
      <th>I2C-Motor-Driver</th>
      <th>24BYJ48 Wires</th>
      <th>28BYJ48 Wires</th>
    </tr>
    <tr align="center">
      <td>J1.M1-/OUT1</td>
      <td>Blue</td>
      <td>Blue</td>
    </tr>
    <tr align="center">
      <td>J1.M1+/OUT2</td>
      <td>Pink</td>
      <td>Orange</td>
    </tr>
    <tr align="center">
      <td>J2.M2-/OUT3</td>
      <td>Orange</td>
      <td>Yellow</td>
    </tr>
    <tr align="center">
      <td>J2.M2+/OUT4</td>
      <td>Yellow</td>
      <td>Pink</td>
    </tr>
  </table>
</div>

```python
from grove.factory import Factory
import time

motor = Factory.getStepperMotor("24BYJ48")
# If it's 28BYJ48
# motor = Factory.getStepperMotor("28BYJ48")
ANGLE = 360 # rotate 360 degrees = 1 cycle
motor.rotate(ANGLE)
# set speed to max rpm, for Motor 24BYJ48, it's 30 RPM.
# direction is clockwise, anti-clockwise use negative value (-30)
SPEED = motor.speed_max # SPEED = 30
motor.speed(SPEED)
motor.enable(True) # enable the motor, begin to run

seconds = ANGLE / 360.0 / SPEED * 60
print("Motor {} rotate {} degrees, time = {:.2f}".format(motor.name, ANGLE, time.time()))
print("      with speed {} RPM".format(SPEED))
print("      will be stop after {:4.2f} seconds".format(seconds))
while True:
    left = motor.rotate()
    if left < 1e-5: break
    print("Angle left {:6.2f} degrees, time = {:.2f}".format(left, time.time()))
    time.sleep(1.0)

print("Motor run ended, time = {:.2f} !".format(time.time()))
```

#### Buzzer PWM mode
```python
from mraa import getGpioLookup
from upm import pyupm_buzzer as GroveBuzzer

# Grove Base Hat for Raspberry Pi
#   PWM JST SLOT - PWM[12 13 VCC GND]
pin = 12
# Create the buzzer object using RaspberryPi GPIO12
mraa_pin = getGpioLookup("GPIO%d" % pin)
buzzer = GroveBuzzer.Buzzer(mraa_pin)
# 1000 Hz sound last 2 seconds
print(buzzer.playSound(1000, 2000000))
```

### Temperature & Humidity Sensor(DHT11)
```python
import time
from grove.grove_temperature_humidity_sensor import DHT

# DHT11 type
# insert to GPIO pin 5, slot D5
dht11 = DHT("11", 5)

while True:
    humi, temp = dht11.read()
    print('DHT{0}, humidity {1:.1f}%, temperature {2:.1f}*'.format(dht11.dht_type, humi, temp))
    time.sleep(1)
```

### LCD 16x2 Characters
#### OLED Display 1.12"
```python
import time
from grove.factory import Factory

# LCD 16x2 Characters
lcd = Factory.getLcd("JHD1802")
# If it's OLED Display 1.12"
# lcd = Factory.getLcd("SH1107G")
rows, cols = lcd.size()
print("LCD model: {}".format(lcd.name))
print("LCD type : {} x {}".format(cols, rows))

lcd.setCursor(0, 0)
lcd.write("hello world!")
lcd.setCursor(0, cols - 1)
lcd.write('X')
lcd.setCursor(rows - 1, 0)
for i in range(cols):
    lcd.write(chr(ord('A') + i))

time.sleep(3)
lcd.clear()
```

### Ultrasonic Ranger
```python
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
import time

sonar = GroveUltrasonicRanger(12) # pin12, slot D12

print('Detecting distance...')
while True:
    print('{} cm'.format(sonar.get_distance()))
    time.sleep(1)
```


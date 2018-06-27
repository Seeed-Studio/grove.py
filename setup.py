
import io
from setuptools import setup


with open('README.md') as f:
    long_description = f.read()

requirements = ['smbus2']

def is_pi():
    found = False
    try:
        with io.open('/proc/cpuinfo', 'r') as cpuinfo:
            for line in cpuinfo:
                if line.startswith('Hardware'):
                    _, value = line.strip().split(':', 1)
                    value = value.strip()
                    if value in ('BCM2708', 'BCM2709', 'BCM2835', 'BCM2836'):
                        found = True
    except IOError:
        pass

    return found

if is_pi():
    requirements.append('RPi.GPIO')


setup(name='grove.py',
      version='0.1',
      description='Drivers of Seeedstudio Grove devices in Python',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Yihui Xiong',
      author_email='yihui.xiong@seeed.cc',
      url='https://github.com/seeed-studio/grove.py',
      packages=['grove'],
      include_package_data=True,
      install_requires=requirements,
      entry_points={
          'console_scripts': [
              'grove_4_digit_display=grove.grove_4_digit_display:main',
              'grove_i2c_color_sensor_v2=grove.grove_i2c_color_sensor_v2:main',
              'grove_ultrasonic_ranger=grove.grove_ultrasonic_ranger:main',
              'grove_temperature_sensor=grove.grove_temperature_sensor:main',
          ],
      },
      zip_safe=False)

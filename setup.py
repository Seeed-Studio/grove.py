
import io
from setuptools import setup, find_packages


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


setup(
    name='grove.py',
    version='0.2',
    description='Python library for Seeedstudio Grove devices',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Yihui Xiong',
    author_email='yihui.xiong@seeed.cc',
    url='https://github.com/seeed-studio/grove.py',
    packages=find_packages(include=['grove']),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'grove_led=grove.grove_led:main',
            'grove_button=grove.grove_button:main',
            'grove_4_digit_display=grove.grove_4_digit_display:main',
            'grove_i2c_color_sensor_v2=grove.grove_i2c_color_sensor_v2:main',
            'grove_ultrasonic_ranger=grove.grove_ultrasonic_ranger:main',
            'grove_temperature_sensor=grove.grove_temperature_sensor:main',
            'grove_gesture_sensor=grove.grove_gesture_sensor:main',
            'grove_i2c_motor_driver=grove.grove_i2c_motor_driver:main',
            'grove_light_sensor_v1.2=grove.grove_light_sensor_v1.2:main',
            'grove_mini_PIR_motion_sensor=grove.grove_mini_PIR_motion_sensor:main',
            'grove_moisture_sensor=grove.grove_moisture_sensor:main',
            'grove_oled_display_128x64=grove.grove_oled_display_128x64:main',
            'grove_piezo_vibration_sensor=grove.grove_piezo_vibration_sensor:main',
            'grove_recorder_v3_0=grove.grove_recorder_v3_0:main',
            'grove_relay=grove.grove_relay:main',
            'grove_servo=grove.grove_servo:main',
            'grove_slide_potentiometer=grove.grove_slide_potentiometer:main',
            'grove_sound_sensor=grove.grove_sound_sensor:main',
            'grove_switch=grove.grove_switch:main',
            'grove_tilt_switch=grove.grove_tilt_switch:main',
            'grove_touch_sensor=grove.grove_touch_sensor:main'
        ],
    },
    zip_safe=False,
    license = 'MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords=['grove'])

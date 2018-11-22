
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
    requirements.append('rpi_ws281x')


setup(
    name='grove.py',
    version='0.6',
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
            'grove_3_axis_compass_bmm150=grove.grove_3_axis_compass_bmm150:main',
            'grove_4_digit_display=grove.grove_4_digit_display:main',
            'grove_air_quality_sensor_v1_3=grove.grove_air_quality_sensor_v1_3:main',
            'grove_button=grove.grove_button:main',
            'grove_ryb_led_button=grove.grove_ryb_led_button:main',
            'grove_gesture_sensor=grove.grove_gesture_sensor:main',
            'grove_i2c_color_sensor_v2=grove.grove_i2c_color_sensor_v2:main',
            'grove_light_sensor_v1_2=grove.grove_light_sensor_v1_2:main',
            'grove_i2c_motor_driver=grove.grove_i2c_motor_driver:main',
            'grove_led=grove.grove_led:main',  
            'grove_loudness_sensor=grove.grove_loudness_sensor:main',
            'grove_mini_pir_motion_sensor=grove.grove_mini_pir_motion_sensor:main',  
            'grove_moisture_sensor=grove.grove_moisture_sensor:main',     
            'grove_oled_display_128x64=grove.grove_oled_display_128x64:main',                   
            'grove_piezo_vibration_sensor=grove.grove_piezo_vibration_sensor:main',
            'grove_recorder_v3_0=grove.grove_recorder_v3_0:main',
            'grove_relay=grove.grove_relay:main',
            'grove_rotary_angle_sensor=grove.grove_rotary_angle_sensor:main',
            'grove_servo=grove.grove_servo:main',
            'grove_slide_potentiometer=grove.grove_slide_potentiometer:main',
            'grove_sound_sensor=grove.grove_sound_sensor:main',
            'grove_switch=grove.grove_switch:main',
            'grove_temperature_humidity_sensor=grove.grove_temperature_humidity_sensor:main',
            'grove_temperature_sensor=grove.grove_temperature_sensor:main',
            'grove_high_accuracy_temperature=grove.grove_high_accuracy_temperature:main',
            'grove_thumb_joystick=grove.grove_thumb_joystick:main',
            'grove_tilt_switch=grove.grove_tilt_switch:main',
            'grove_touch_sensor=grove.grove_touch_sensor:main',
            'grove_ultrasonic_ranger=grove.grove_ultrasonic_ranger:main',
            'grove_water_sensor=grove.grove_water_sensor:main',
            'grove_collision_sensor=grove.grove_collision_sensor:main',
            'grove_pwm_buzzer=grove.grove_pwm_buzzer:main',
            'grove_mech_keycap=grove.grove_mech_keycap:main',
            'grove_lcd_1.2inches=grove.lcd.sh1107g:main',
            'grove_uv_sensor=grove.grove_uv_sensor:main',
            'grove_tem_hum_sht35=grove.grove_I2C_High_Accuracy_tem_hum_SHT35_sensor:main',
            'grove_button_i2c=grove.button.grove_button_i2c:main',
            'grove_temperature_humidity_sensor_sht31=grove.grove_temperature_humidity_sensor_sht3x:main'
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

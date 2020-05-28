'''
## License

The MIT License (MIT)

Grove Base Hat for the Raspberry Pi, used to connect grove sensors.
Copyright (C) 2020  Seeed Technology Co.,Ltd.
'''

import io
from setuptools import setup, find_packages


with open('README.md') as f:
    long_description = f.read()

requirements = ['smbus2','spidev','pyserial']


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
    name='Seeed_grove.py',
    version='0.3',
    description='Python library for Seeedstudio Grove devices',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='JunJie Chen',
    author_email='hansen.chen@seeed.cc',
    url='https://github.com/seeed-studio/grove.py',
    packages=find_packages(include=['grove']),
    include_package_data=True,
    install_requires=requirements,
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
    keywords=['grove','Seeed'])

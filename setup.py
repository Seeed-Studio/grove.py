

from setuptools import setup


with open('README.md') as f:
    long_description = f.read()


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
      install_requires=['smbus2'],
      zip_safe=False)

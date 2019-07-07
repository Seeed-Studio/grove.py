
# Install Dependencies
#### Install MRAA and UPM

- Add repository

```shell
# RPi
echo "deb https://seeed-studio.github.io/pi_repo/ stretch main" | sudo tee /etc/apt/sources.list.d/seeed.list
# Coral Dev Board
echo "deb https://seeed-studio.github.io/pi_repo/ mendel-beaker main" | sudo tee /etc/apt/sources.list.d/seeed.list
#For Nvidia Jetson nano
echo "deb https://seeed-studio.github.io/pi_repo/ bionic main" | sudo tee /etc/apt/sources.list.d/seeed.list
```

- Add public GPG key

```shell
curl https://seeed-studio.github.io/pi_repo/public.key | sudo apt-key add -
# or
# sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys BB8F40F3
```

- Install MRAA & UPM

```shell
sudo apt update
# Python2
sudo apt install python-mraa python-upm
# Python3
sudo apt install python3-mraa python3-upm
```

#### Install library raspberry-gpio-python for RPi
```shell
sudo apt update
sudo apt install python-rpi.gpio python3-rpi.gpio
```

#### Install library rpi_ws281x for RPi
```shell
sudo pip install rpi_ws281x
sudo pip3 install rpi_ws281x
```

<br><br>
# Install grove.py
From PyPI

> Note: This method could not get the lastest code most time.

```shell
# python2
sudo pip install grove.py
# python3
sudo pip3 install grove.py
```

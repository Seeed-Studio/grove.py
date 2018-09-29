#!/bin/bash
#
: <<'EOF'
The MIT License (MIT)

Seeed-Studio Raspberry Pi Hats.
  Peter Yang, turmary@126.com
Copyright (C) 2018  Seeed Technology Co.,Ltd. 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
EOF


_DEBUG=0

_package_name=grove.py
_seeed_source_list=/etc/apt/sources.list.d/seeed.list
_seeed_apt_key="BB8F 40F3"
_repo_package_url=https://github.com/Seeed-Studio/$_package_name/archive/master.zip

BLACKLIST=/etc/modprobe.d/raspi-blacklist.conf
CONFIG=/boot/config.txt
if [ $_DEBUG -ne 0 ]; then
  BLACKLIST=./raspi-blacklist.conf
  CONFIG=./config.txt
fi


set_config_var() {
  lua - "$1" "$2" "$3" <<EOF > "$3.bak"
local key=assert(arg[1])
local value=assert(arg[2])
local fn=assert(arg[3])
local file=assert(io.open(fn))
local made_change=false
for line in file:lines() do
  if line:match("^#?%s*"..key.."=.*$") then
    line=key.."="..value
    made_change=true
  end
  print(line)
end

if not made_change then
  print(key.."="..value)
end
EOF
mv "$3.bak" "$3"
}

get_i2c() {
  if grep -q -E "^(device_tree_param|dtparam)=([^,]*,)*i2c(_arm)?(=(on|true|yes|1))?(,.*)?$" $CONFIG; then
    echo 0
  else
    echo 1
  fi
}

do_i2c() {
  DEFAULT=--defaultno
  if [ $(get_i2c) -eq 0 ]; then
    DEFAULT=
  fi
  RET=$1
  if [ $RET -eq 0 ]; then
    SETTING=on
    STATUS=enabled
  elif [ $RET -eq 1 ]; then
    SETTING=off
    STATUS=disabled
  else
    return $RET
  fi

  set_config_var dtparam=i2c_arm $SETTING $CONFIG &&
  if ! [ -e $BLACKLIST ]; then
    touch $BLACKLIST
  fi
  sed $BLACKLIST -i -e "s/^\(blacklist[[:space:]]*i2c[-_]bcm2708\)/#\1/"
  sed /etc/modules -i -e "s/^#[[:space:]]*\(i2c[-_]dev\)/\1/"
  if ! grep -q "^i2c[-_]dev" /etc/modules; then
    printf "i2c-dev\n" >> /etc/modules
  fi
  dtparam i2c_arm=$SETTING
  modprobe i2c-dev
}

do_uninstall=false
if [ "$1" == "uninstall" ]; then
  do_uninstall=true
fi

# Everything else needs to be run as root
if [ $(id -u) -ne 0 ]; then
  printf "Script must be run as root. Try 'sudo $0'\n"
  exit 1
fi

### Uninstall this package ###
if [ "$do_uninstall" == "true" ]; then
  # To remove all users installation
  pip  uninstall -y $_package_name
  pip3 uninstall -y $_package_name
  apt-get -y remove python-grove-py
  apt-get -y remove python3-grove-py
  exit 0
fi

# install dependencies
## install MRAA and UPM for RPi
### add repository
if [ ! -f $_seeed_source_list ]; then
  echo "deb https://seeed-studio.github.io/pi_repo/ stretch main" | tee $_seeed_source_list
fi

### add public GPG key
if ! apt-key list | egrep "$_seeed_apt_key" > /dev/null; then
  curl https://seeed-studio.github.io/pi_repo/public.key | apt-key add -
fi

## install MRAA & UPM
apt update
### libmraa
apt install -y libmraa1
### python2
apt install -y python-mraa  python-upm
### python3
apt install -y python3-mraa python3-upm

## install library raspberry-gpio-python
apt install -y python-rpi.gpio python3-rpi.gpio

## install library rpi_ws281x
pip  install rpi_ws281x
pip3 install rpi_ws281x

### install I2C ###
if [ $(get_i2c) -ne 0 ]; then
  # enable i2c interface
  echo Enable I2C interface ...
  do_i2c 0
fi
echo I2C interface enabled...

# install this python repository
pip  install --upgrade $_repo_package_url
pip3 install --upgrade $_repo_package_url

sync
sleep 1
sync 

echo "#######################################################"
echo "  Lastest Grove.py from github install complete   !!!!!"
echo "#######################################################"
exit 0


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

function apt_install() {
  pkg_name=$1

  for ((i = 0; i < 3; i++)); {
    apt-get install -y $pkg_name
    pkg_status=$(dpkg -s $pkg_name | egrep "Status:.*" | awk '{ printf "%s", $2; }')
    [ "$pkg_status" == "install" ] && return 0
  }
  return 1
}

function pip_install() {
  local fields
  pkg_name=$1
  pip_cmd=${2}

  fields=( $pip_cmd )
  for ((i = 0; i < 3; i++)); {
    $pip_cmd
    pkg_status=$(${fields[0]} list --format=legacy | egrep "$pkg_name " | awk '{ printf "%s", $1; }')
    [ "$pkg_status" == "$pkg_name" ] && return 0
  }
  return 1
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

### install I2C ###
if [ $(get_i2c) -ne 0 ]; then
  # enable i2c interface
  echo Enable I2C interface ...
  do_i2c 0
fi
echo I2C interface enabled...


## Initial installation
r=0

## install MRAA & UPM
apt update

### libmraa
(( r == 0 )) && { apt_install libmraa1;    r=$?; }

### python2
(( r == 0 )) && { apt_install python-mraa; r=$?; }
(( r == 0 )) && { apt_install python-upm;  r=$?; }

### python3
(( r == 0 )) && { apt_install python3-mraa;r=$?; }
(( r == 0 )) && { apt_install python3-upm; r=$?; }

## install library raspberry-gpio-python
(( r == 0 )) && { apt_install python-rpi.gpio;  r=$?; }
(( r == 0 )) && { apt_install python3-rpi.gpio; r=$?; }

## install library libbma456
(( r == 0 )) && { apt_install libbma456; r=$?; }

## install library libbmi088
(( r == 0 )) && { apt_install libbmi088; r=$?; }

## install library bme680
(( r == 0 )) && { apt_install python-bme680;  r=$?; }
(( r == 0 )) && { apt_install python3-bme680; r=$?; }

## install library rpi-ws281x
(( r == 0 )) && { pip_install rpi-ws281x 'pip  install rpi-ws281x'; r=$?; }
(( r == 0 )) && { pip_install rpi-ws281x 'pip3 install rpi-ws281x'; r=$?; }

## install library smbus2
(( r == 0 )) && { pip_install smbus2 'pip  install smbus2'; r=$?; }
(( r == 0 )) && { pip_install smbus2 'pip3 install smbus2'; r=$?; }

## install library rpi-vl53l0x
(( r == 0 )) && { pip_install rpi-vl53l0x 'pip  install rpi-vl53l0x'; r=$?; }
(( r == 0 )) && { pip_install rpi-vl53l0x 'pip3 install rpi-vl53l0x'; r=$?; }

## install library sgp30
(( r == 0 )) && { pip_install sgp30 'pip  install sgp30'; r=$?; }
(( r == 0 )) && { pip_install sgp30 'pip3 install sgp30'; r=$?; }

# install this python repository
(( r == 0 )) && { pip_install grove.py "pip  install --upgrade $_repo_package_url"; r=$?; }
(( r == 0 )) && { pip_install grove.py "pip3 install --upgrade $_repo_package_url"; r=$?; }
(( r == 0 )) && { which grove_button > /dev/null; r=$?; }

(( r != 0 )) && {
	echo "-------------------------------------------------------"
	echo "     Grove.py installation FAILED, FAILED, FAILED      "
	echo "-------------------------------------------------------"
	exit 1
}

sync
sleep 1
sync 

echo "#######################################################"
echo "  Lastest Grove.py from github install complete   !!!!!"
echo "#######################################################"
exit 0


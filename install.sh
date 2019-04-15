#!/bin/bash
#
: <<'EOF'
The MIT License (MIT)

Seeed-Studio Raspberry Pi Hats.
  Peter Yang, turmary@126.com
Copyright (C) 2018 Seeed Technology Co.,Ltd.
EOF


_DEBUG=0

_install_extra_library=true

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
	egrep -q "^(device_tree_param|dtparam)=([^,]*,)*i2c(_arm)?(=(on|true|yes|1))?(,.*)?$" $CONFIG
	echo $?
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

alias  pip=' pip --no-cache-dir'
alias pip3='pip3 --no-cache-dir'

function pip_install() {
	local fields
	pkg_name=$1
	pip_cmd=${2}

	fields=( $pip_cmd )
	for ((i = 0; i < 3; i++)); {
		$pip_cmd
		pkg_status=$(${fields[0]} list --format=columns | egrep "$pkg_name " | awk '{ printf "%s", $1; }')
		[ "$pkg_status" == "$pkg_name" ] && return 0
	}
	return 1
}

function platform_get() {
	local dts_model platform

	dts_model=$(strings /proc/device-tree/model)

	case "$dts_model" in
	TI\ AM335x*)
		platform=bbb;;
	Raspberry\ Pi*)
		platform=rpi;;
	Freescale\ i\.MX8MQ\ Phanbell)
		platform=coral;;
	jetson-nano)
		platform=jetson_nano;;
	*)
		platform="unknown";;
	esac
	echo $platform
}



# Get platform type
platform=$(platform_get)

if [[ "$platform" == "jetson_nano" ]];then
	_install_extra_library=false
fi	

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
	# To remove all users installaon
	pip  uninstall -y $_package_name
	pip3 uninstall -y $_package_name
	apt-get -y remove python-grove-py
	apt-get -y remove python3-grove-py
	exit 0
fi

# install dependencies
### add repository
if [ ! -f $_seeed_source_list ]; then
	case "$platform" in
	coral)
		code_name="mendel-beaker";;
	rpi)
		code_name="stretch";;
	jetson_nano)
		code_name="bionic";;
	*)
		code_name="unknown";;
	esac
	echo "deb https://seeed-studio.github.io/pi_repo/ $code_name main" | tee $_seeed_source_list
fi

### add public GPG key
if ! apt-key list | egrep "$_seeed_apt_key" > /dev/null; then
	curl https://seeed-studio.github.io/pi_repo/public.key | apt-key add -
fi



## Initial installation
r=0

## Update apt source
apt update

case "$platform" in
coral)
	apt_install python-pip
	apt_install python3-pip
	apt_install python-setuptools
	apt_install python3-setuptools
	apt_install python-wheel
	apt_install python3-wheel

	## install library enum
	;;
jetson_nano)
	
	apt_install python-pip	
	apt_install python3-pip
	apt_install python-setuptools
	apt_install python3-setuptools
	apt_install python-wheel
	apt_install python3-wheel

	;;
rpi)
	### install I2C ###
	if [ $(get_i2c) -ne 0 ]; then
		# enable i2c interface
		echo Enable I2C interface ...
		do_i2c 0
	fi
	echo I2C interface enabled...

	## install library raspberry-gpio-python
	(( r == 0 )) && { apt_install python-rpi.gpio;  r=$?; }
	(( r == 0 )) && { apt_install python3-rpi.gpio; r=$?; }
	;;

*)
	echo "unsupport platform $platform, abort ..."
	exit 1
	;;
esac

## install MRAA & UPM
### libmraa
(( r == 0 )) && { apt_install libmraa1;    r=$?; }

### python2
(( r == 0 )) && { apt_install python-mraa; r=$?; }
(( r == 0 )) && { apt_install python-upm;  r=$?; }

### python3
(( r == 0 )) && { apt_install python3-mraa;r=$?; }
(( r == 0 )) && { apt_install python3-upm; r=$?; }

## install library libbma456
if [[ "$_install_extra_library" == "true" ]];then
	(( r == 0 )) && { apt_install libbma456; r=$?; }
fi

## install library libbmi088
if [[ "$_install_extra_library" == "true" ]];then
	(( r == 0 )) && { apt_install libbmi088; r=$?; }
fi

## install library rpi-ws281x
if [ "X$platform" == "Xrpi" ]; then
	(( r == 0 )) && { pip_install rpi-ws281x 'pip  install rpi-ws281x'; r=$?; }
	(( r == 0 )) && { pip_install rpi-ws281x 'pip3 install rpi-ws281x'; r=$?; }
fi

## install library smbus
(( r == 0 )) && { pip_install smbus  'pip  install smbus'; r=$?; }
(( r == 0 )) && { pip_install smbus  'pip3 install smbus'; r=$?; }

## install library smbus2
(( r == 0 )) && { pip_install smbus2 'pip  install smbus2'; r=$?; }
(( r == 0 )) && { pip_install smbus2 'pip3 install smbus2'; r=$?; }

## install library bme680

if [[ "$_install_extra_library" == "true" ]];then
	(( r == 0 )) && { pip_install bme680 'pip  install bme680'; r=$?; }
	(( r == 0 )) && { pip_install bme680 'pip3 install bme680'; r=$?; }
fi

## install library rpi-vl53l0x
if [[ "$_install_extra_library" == "true" ]];then
	(( r == 0 )) && { pip_install rpi-vl53l0x 'pip  install rpi-vl53l0x'; r=$?; }
	(( r == 0 )) && { pip_install rpi-vl53l0x 'pip3 install rpi-vl53l0x'; r=$?; }
fi

## install library sgp30
if [[ "$_install_extra_library" == "true" ]];then
	(( r == 0 )) && { pip_install sgp30 'pip  install sgp30'; r=$?; }
	(( r == 0 )) && { pip_install sgp30 'pip3 install sgp30'; r=$?; }
fi
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


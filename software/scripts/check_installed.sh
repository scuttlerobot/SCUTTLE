#!/bin/bash

spinner() {
    local i sp n
    sp='/-\|'
    n=${#sp}
    printf ' '
    while sleep 0.1; do
        printf "%s\b" "${sp:i++%n:1}"
    printf "%s\b" "${sp:i++%n:1}"
    done
}

#Promt for root password
[ "$UID" -eq 0 ] || exec sudo bash "$0" "$@"

# Check for internet connection.
printf "\nChecking for internet connection.\n"
wget -q --spider http://google.com
if [ $? -eq 0 ]; then
    echo ""
	echo -e "\e[1m\e[32mSuccess\e[0m"
    echo ""
else
	echo ""
	echo -e "\e[1m\e[31mERROR: No Internet Connection!\e[0m"
	echo -e "       \e[1m\e[31mPlease run setup_wpa_enterprise.py\e[0m" >&2
	echo ""
	exit
fi

echo "#################################################################" >> /home/debian/.install_log
date >> /home/debian/.install_log
echo "#################################################################" >> /home/debian/.install_log

PROGS=(git ftp zsh curl wget flac libx11-6 pure-ftpd python-pip python-dev libx11-dev python3-pip python3-pip3 python3-dev python-numpy python3-serial python3-numpy python3-opengl libsdl-ttf2.0-dev libsmpeg-dev libsdl1.2-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev libtiff5-dev fluid-soundfont-gm timgm6mb-soundfont xfonts-base xfonts-100dpi xfonts-75dpi xfonts-cyrillic fontconfig fonts-freefont-ttf python3-setuptools libfreetype6-dev build-essential python-smbus python3-pyaudio libsdl-image1.2-dev libsdl-mixer1.2-dev python3-opencv libopencv-dev mjpg-streamer-opencv-python libsdl2-dev)

printf "Running apt update."
spinner &
apt -qq update >> /home/debian/.install_log 2>&1
printf "\nDone.\n\n"

printf "Checking Installed Programs...\n\n"

# Check if apt packages installed
for i in "${PROGS[@]}"
do
	dpkg-query --list | grep " $i" > /dev/null 2>&1

	if [ $? -eq 1 ]; then
		echo -e "\e[1m\e[31m$i not installed!\e[0m"
		printf "Installing $i."
		spinner &
		yes | apt -qq install -y $i >> /home/debian/.install_log 2>&1
		dpkg-query --list | grep " $i" > /dev/null 2>&1
		if [ $? -eq 0 ]; then
			printf "\n"
			echo -e "\e[1m\e[32m$i installed!\e[0m"
        fi
	else
		echo -e "\e[1m\e[32m$i installed!\e[0m"
	fi
done

# Array of python modules to install.
PYMODS=(SpeechRecognition cayenne-mqtt bmp280 pygame Adafruit_GPIO)

# Install Python Libraries

printf "\nChecking Installed Python Libraries...\n\n"

for i in "${PYMODS[@]}"
do
	python3 -c "import $i" > /dev/null 2>&1

	if [ $? -eq 1 ]; then

		echo -e "\e[1m\e[31m$i not installed!\e[0m"
		printf "Installing $i."
		spinner &
		pip3 install --quiet $i >> /home/debian/.install_log 2>&1
        	python3 -c "import $i" > /dev/null 2>&1 || pip3 install --quiet $i >> /home/debian/.install_log 2>&1
		if [ $? -eq 0 ]; then
			printf "\n"
			echo -e "\e[1m\e[32m$i installed!\e[0m"
        fi
	else
		echo -e "\e[1m\e[32m$i installed!\e[0m"
	fi
done
printf "\n"
pip3 --quiet install --upgrade Adafruit_BBIO

reboot

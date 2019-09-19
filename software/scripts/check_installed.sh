#!/bin/bash

spinner() {
    local i sp n
    sp='/-\|'
    n=${#sp}
    printf ' '
    while sleep 0.1; do
        printf "%s\b" "${sp:i++%n:1}"
    done
}

#Promt root
[ "$UID" -eq 0 ] || exec sudo bash "$0" "$@"

# Check for internet connection.
echo "Checking for internet connection."
wget -q --spider http://google.com
if [ $? -eq 0 ]; then
	echo -e "\e[1m\e[32mSuccess\e[0m"
else
	echo ""
	echo -e "\e[1m\e[31mERROR: \nNo Internet Connection!\e[0m"
	echo -e "       \e[1m\e[31mPlease run setup_wpa_enterprise.py\e[0m" >&2
	echo ""
fi

PROGS=(git ftp zsh curl wget flac libx11-6 pure-ftpd python-pip python-dev libx11-dev python3-pip python3-dev python-numpy libopencv-dev python3-serial python3-opencv python3-numpy python3-opengl libsdl-ttf2.0-dev libsmpeg-dev libsdl1.2-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev libtiff5-dev fluid-soundfont-gm timgm6mb-soundfont xfonts-base xfonts-100dpi xfonts-75dpi xfonts-cyrillic fontconfig fonts-freefont-ttf python3-setuptools libfreetype6-dev build-essential python-smbus python3-pyaudio libsdl-image1.2-dev libsdl-mixer1.2-dev mjpg-streamer-opencv-python)

# Check if apt packages installed
for i in "${PROGS[@]}"
do
	dpkg-query --list | grep " $i" > /dev/null 2>&1

	if [ $? -eq 1 ]; then
		echo -e "\e[1m\e[31m$i not installed!\e[0m"
		printf "Installing $i."
		spinner &
		apt -qq install -y $i > /dev/null 2>&1
	else
		echo -e "\e[1m\e[32m$i installed!\e[0m"
	fi
done

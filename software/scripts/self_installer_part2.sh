# self_installer_part2.sh
# This script is used to install important packages for operating SCUTTLE.
# Instructions: Connect the blue to wifi, then run self_installer_part1.sh, allow
# your device to reboot, and then run self_installer_part2.sh

# Updates

  sudo apt-get update
  sudo apt-get upgrade -y
  sudo apt-get dist-upgrade -y

# Install required Packages

  sudo apt-get install -y git ftp zsh curl wget flac libx11-6 pure-ftpd python-pip python-dev libx11-dev python3-pip python3-dev python-numpy libopencv-dev \
  python3-serial python3-opencv python3-numpy python3-opengl libsdl-ttf2.0-dev libsmpeg-dev libsdl1.2-dev libportmidi-dev libswscale-dev libavformat-dev \
  libavcodec-dev libtiff5-dev fluid-soundfont-gm timgm6mb-soundfont xfonts-base xfonts-100dpi xfonts-75dpi xfonts-cyrillic fontconfig fonts-freefont-ttf \ 
  python3-setuptools libfreetype6-dev build-essential python-smbus python3-pyaudio libsdl-image1.2-dev libsdl-mixer1.2-dev mjpg-streamer-opencv-python
 
# Install Python Libraries

  sudo pip install --upgrade Adafruit_BBIO
  sudo pip3 install SpeechRecognition cayenne-mqtt bmp280 pygame
  
  # Fix Adafruit_BBIO.GPIO (default install is setup for bb black)
  
  sudo python3 /opt/source/rcpy/setup.py install
  sudo python3 /opt/source/pyctrl/setup.py install
  
  # Install Adafruit_GPIO.I2C

  cd /tmp
  git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
  cd Adafruit_Python_GPIO
  sudo python3 setup.py install

# Make SSH pretty

  echo " " > /etc/banner
  echo "        _____      _____     _    _     _______   _______    _          ______" >> /etc/banner
  echo "       / ____|    / ____|   | |  | |   |__   __| |__   __|  | |        |  ____|" >> /etc/banner
  echo "      | (___     | |        | |  | |      | |       | |     | |        | |__" >> /etc/banner
  echo "       \___ \    | |        | |  | |      | |       | |     | |        |  __|" >> /etc/banner
  echo "       ____) | _ | |____  _ | |__| |  _   | |   _   | |  _  | |____  _ | |____" >> /etc/banner
  echo "      |_____/ (_) \_____|(_) \____/  (_)  |_|  (_)  |_| (_) |______|(_)|______|" >> /etc/banner
  echo " " >> /etc/banner
  echo "      Sensing, Connected, Utility Transport Taxi for Level Environments" >> /etc/banner
  echo "      Texas A&M's Open-Source SCUTTLE Robot: https://github.com/dmalawey/Scuttle" >> /etc/banner
  echo " " >> /etc/banner
  echo -n "" > /etc/motd
  sudo sed -i 's|Banner none|Banner /etc/banner|g' /etc/ssh/sshd_config
  sudo /etc/init.d/ssh restart

# Change Hostname

  echo "scuttle" > /etc/hostname
  sudo sed -i 2d /etc/hosts
  sudo sed -i '2i127.0.1.1       scuttle.localdomain  scuttle' /etc/hosts

# Reboot

  sudo reboot

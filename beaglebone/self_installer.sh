# THIS IS NOT AT ALL A POLISHED SCRIPT
# USE AT YOUR OWN DISCRETION
# but it works pretty good.

# Check if Connected to internet

#ping -q -w 1 -c 1 `ip r | grep default | cut -d ' ' -f 3` > /dev/null && echo ok || echo error

#Grow root partition to fill SD card.
cd /opt/scripts/tools
git pull
sudo ./grow_partition.sh




# Updates


  sudo apt-get update
  sudo apt-get upgrade -y
  sudo apt-get dist-upgrade -y



# Install helpful tools

  sudo apt-get install -y pure-ftpd ftp

# Install Python Libraries

sudo pip install --upgrade Adafruit_BBIO
sudo apt-get install -y python3-serial

# Python Speech Recongnition

sudo apt-get install -y python3-pyaudio flac
sudo pip3 install SpeechRecognition

# Cayenne Library

sudo pip3 install cayenne-mqtt

  #sudo dd if=/dev/zero of=/dev/mmcblk1 bs=1M count=10

  #sudo apt update ; sudo apt install --only-upgrade bb-cape-overlays

  #uboot_overlay_pru=/lib/firmware/AM335X-PRU-RPROC-4-14-TI-00A0.dtbo

  #cd /opt/scripts/
  #git pull

  #sudo /opt/scripts/tools/update_kernel.sh --ti-channel --lts-4_14

  #sudo /opt/scripts/tools/developers/update_bootloader.sh

# Install OpenCV and other Libraries Color Tracking Relies on

  sudo apt-get install -y python-pip python3-pip libopencv-dev python3-opencv python-numpy

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

# Fix Adafruit_BBIO.GPIO

sudo python3 /opt/source/rcpy/setup.py install

sudo python3 /opt/source/pyctrl/setup.py install

# Fix Adafruit_GPIO.I2C

sudo apt-get install -y build-essential python-pip python-dev python-smbus git
git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
cd Adafruit_Python_GPIO
sudo python3 setup.py install

# Install zsh

sudo apt-get install -y git curl wget zsh

#sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

#sudo sed -i 2d /home/debian/.zshrc
#sudo sed -i '2iexport PATH=$HOME/bin:/usr/local/bin:/sbin:/usr/sbin:$PATH' /home/debian/.zshrc



#sudo -u debian sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

#sudo -u debian sed -i 2d /home/debian/.zshrc
#sudo -u debian sed -i '2iexport PATH=$HOME/bin:/usr/local/bin:/sbin:/usr/sbin:$PATH' /home/debian/.zshrc

sudo reboot

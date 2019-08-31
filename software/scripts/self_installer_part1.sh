# self_installer_part1.sh
# This script is used to install important packages for operating SCUTTLE.
# Instructions: Connect the blue to wifi, then run self_installer_part1.sh, allow
# your device to reboot, and then run self_installer_part2.sh

# Erase internal memory (EMMC).
  
  sudo dd if=/dev/zero of=/dev/mmcblk1 bs=1M count=10

# Check if Connected to internet

# ping -q -w 1 -c 1 `ip r | grep default | cut -d ' ' -f 3` > /dev/null && echo ok || echo error

# Grow root partition to fill SD card.

  cd /opt/scripts/tools
  git pull
  sudo ./grow_partition.sh
  sudo reboot # added 2019.08.30 to guarantee linux recognizes the increased drive partition size.
  
# END OF SELF-INSTALLER PART 1.  CONTINUE BY RUNNING PART 2.

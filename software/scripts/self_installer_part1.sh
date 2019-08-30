# THIS IS NOT AT ALL A POLISHED SCRIPT
# USE AT YOUR OWN DISCRETION
# but it works pretty good.

# PLEASE REPORT ALL ISSUES TO:
# https://github.com/MXET/SCUTTLE/issues

# Erase internal memory (EMMC).
  
  sudo dd if=/dev/zero of=/dev/mmcblk1 bs=1M count=10

# Check if Connected to internet

# ping -q -w 1 -c 1 `ip r | grep default | cut -d ' ' -f 3` > /dev/null && echo ok || echo error

# Grow root partition to fill SD card.

  cd /opt/scripts/tools
  git pull
  sudo ./grow_partition.sh
  sudo reboot # added 2019.08.30 to guarantee linux recognizes the new partition size.
  
# END OF SELF-INSTALLER PART 1.  CONTINUE BY RUNNING PART 2.

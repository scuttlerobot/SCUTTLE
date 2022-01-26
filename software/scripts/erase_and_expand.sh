#!/bin/bash

# Erase internal memory (EMMC).
  
  sudo dd if=/dev/zero of=/dev/mmcblk1 bs=1M count=10

# Grow root partition to fill SD card.

  cd /opt/scripts/tools
  git pull
  sudo ./grow_partition.sh
  sudo reboot

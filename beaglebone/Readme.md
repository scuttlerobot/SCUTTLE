# BEAGLEBONE SUBFOLDER README:

This folder links to the latest beaglebone image for SCUTTLE project.

## Beaglebone Image:
Please navigate to the "releases" tab of this github to download the latest image.

How to run self_installer.sh:
1) Use the wget command and paste the raw hyperlink of the self_installer.sh into your CLI.
2) use "sudo bash self_installer.sh" to run it
3) The install may take about 5 minutes. At finish, you'll see these characters again: "➜  ~"

## SHELL Cheat Sheet:

Report devices active on the i2c bus:
```sudo i2cdetect -y -r 1
  sudo:       Executes the command following as root user
  i2cdetect:  A program to scan an I2C bus for devices
  -y  :       Does not prompt
  -r 1:       I2C bus to read from. Here we read from I2C bus 1.```

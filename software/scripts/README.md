# SCRIPTS SUBFOLDER README:

These are linux scripts to run on your beaglebone blue after installing the proper debian image.

## Beaglebone Image:
Please go to [beagleboard.org](beagleboard.org/latest-images) and get the latest Debian IoT version.
<br> do not select a "Flasher," which is for automatically flashing the board.  We will flash the SD card.

How to run self_installer.sh:
1) Use the wget command and paste the raw hyperlink of the self_installer_part1.sh into your command line.
> Example: <br>
> wget https://raw.githubusercontent.com/MXET/SCUTTLE/master/software/scripts/self_installer_part1.sh
2) use "sudo bash self_installer.sh" to run the script.
3) The install may take about 5 minutes. At finish, you'll see these characters again: "➜  ~"
4) Following part1 there will be a reboot.  Reconnect and repeat steps 1 thru 3 for self_installer_part2.sh
5) Be prepared for part 2 to take 45 minutes.  It includes many libraries such as machine vision and speech recognition.

How to verify successful installations:
1) Navigate to the "check_installed.sh" script and run it by the same method as above.

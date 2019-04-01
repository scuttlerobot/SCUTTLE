# BEAGLEBONE SUBFOLDER README:

This folder links to the latest beaglebone image for SCUTTLE project.

## Beaglebone Image:
Please navigate to the "releases" tab of this github to download the latest image.

How to run self_installer.sh:
1) Use the wget command and paste the raw hyperlink of the self_installer.sh into your CLI.
2) use "sudo bash self_installer.sh" to run it
3) The install may take about 5 minutes. At finish, you'll see these characters again: "➜  ~"

## SHELL Cheat Sheet:

**Report devices active on the i2c bus:**
```
sudo i2cdetect -y -r 1

  sudo:       Executes the command following as root user
  i2cdetect:  A program to scan an I2C bus for devices
  -y  :       Does not prompt
  -r 1:       I2C bus to read from. Here we read from I2C bus 1.
  ```

**Report the messages from kernel ring buffer (system architecture, cpu, attached devices, etc)**
```
dmesg
  ```
  
**Check battery voltage (with example output)**
```
➜  ~ sudo rc_battery_monitor
2S Pack   Jack   #Cells   Cell
 8.22V   10.63V  3       3.54V   [1]    1088 killed     sudo rc_battery_monitor

  ```
**List USB devices connected (with example output)**
  ```
➜  ~ lsusb
Bus 001 Device 003: ID 2f24:0091
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
  ```

**Explicitly Show Debian Release Date**
  ```
debian@scuttle:~$ cat /etc/dogtag
BeagleBoard.org Debian Image 2018-10-07

  ```
  
**Check if you have a live internet connection**
  ```
debian@scuttle:~$ ping google.com
PING google.com (216.58.194.110) 56(84) bytes of data.
64 bytes from dfw06s48-in-f14.1e100.net (216.58.194.110): icmp_seq=1 ttl=55 time                                       =10.5 ms
64 bytes from dfw06s48-in-f14.1e100.net (216.58.194.110): icmp_seq=2 ttl=55 time                                       =16.3 ms
64 bytes from dfw06s48-in-f14.1e100.net (216.58.194.110): icmp_seq=3 ttl=55 time                                       =17.8 ms
64 bytes from dfw06s48-in-f14.1e100.net (216.58.194.110): icmp_seq=4 ttl=55 time                                       =16.5 ms
^C
--- google.com ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3005ms
rtt min/avg/max/mdev = 10.521/15.320/17.869/2.835 ms
  ```

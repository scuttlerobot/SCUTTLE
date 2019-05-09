# S.C.U.T.T.L.E. Software
This folder contains all scuttle software and software information.

<br>

## Python ([SCUTTLE/software/python](https://github.com/MXET/SCUTTLE/tree/master/software/python))

The python folder stores all the code needed to drive the SCUTTLE robot using simplified functions allowing the user to perform motor functions such as driving and turning as well as reading sensor values from onboard sensors and external sensors like the rotary encoders and compass. Using these functions helps anyone start writing their own programs for the SCUTTLE robot as quickly as possible.

<br>

## Scripts ([SCUTTLE/software/scripts](https://github.com/MXET/SCUTTLE/tree/master/software/scripts))

This folder contains scripts useful for installing all the libraries SCUTTLE relies on as well as performing maintenance tasks and installing additional software.

<br>

## MATLAB ([SCUTTLE/software/matlab](https://github.com/MXET/SCUTTLE/tree/master/software/matlab))

The MATLAB folder contains the MATLAB Controller Client that allows a user to control the SCUTTLE robot manually as well as show sensor readings and plot the live position of the SCUTTLE robot.

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

**Copy a GitHub repository to your device**
  ```
debian@scuttle:~$ git clone http://github.com/MXET/SCUTTLE
Cloning into 'SCUTTLE'...
remote: Enumerating objects: 262, done.
remote: Counting objects: 100% (262/262), done.
remote: Compressing objects: 100% (215/215), done.
remote: Total 1356 (delta 128), reused 99 (delta 41), pack-reused 1094
Receiving objects: 100% (1356/1356), 82.88 MiB | 1.17 MiB/s, done.
Resolving deltas: 100% (610/610), done.
debian@scuttle:~$
  ```

**Expand the partition on your Blue SD card**
  ```
cd /opt/scripts/tools #navigate to the right directory
git pull  #update the tools repository
sudo ./grow_partition.sh  # the command to expand the boot partition
sudo reboot # the command to reboot the blue
  ```

## Beaglebone Blue Cheat Sheet:

**Instructions to connect to SSH using putty:**
([beaglebone how-to-connect](https://www.dummies.com/computers/beaglebone/how-to-connect-your-beaglebone-via-ssh-over-usb/))
**Instructions to flash a new SD card with an image:**
([beagleboard.org getting started](http://beagleboard.org/getting-started#step3))


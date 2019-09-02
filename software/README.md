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
  
**Print the current connections**
  ```
iwconfig
  ```
  
**Copy a github repository**
  ```
git clone http://www.github.com/MXET/SCUTTLE
  ```
  This will copy all of the contents of SCUTTLE repo into a folder called SCUTTLE in the working directory.
  
**github - push updates from local to online repository**
  ```
git add -A
git commit # then make brief comment on your update
git push # then provide credentials as needed
  ```
  This will push the updates from your local device back to the online repo.

**github - pull updates from online to local repository**
  ```
git pull
  ```
  This will pull updates from online.  If it has conflicts and you want to force it, follow the steps in [this link](https://learn.adafruit.com/an-introduction-to-collaborating-with-version-control/https-credential-caching-and-ssh-keys).
  
## Windows Cheat Sheet:
**find out the IP address of a connected device**
Press the windows key, type "cmd" then ENTER.  In the command prompt, type ipconfig.  If you are connected to your linux device that is in access-point mode with your wireless wifi adapter, look at Wireless LAN section and the Default Gateway is the IP address of your linux device.

```
Wireless LAN adapter Wi-Fi:
   Connection-specific DNS Suffix  . :
   Link-local IPv6 Address . . . . . : fe80::8123:73e7:ace0:720c%15
   IPv4 Address. . . . . . . . . . . : 192.168.50.50
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 192.168.50.1
```

## Beaglebone Blue Cheat Sheet:

**Instructions to connect to SSH using putty:**
([beaglebone how-to-connect](https://www.dummies.com/computers/beaglebone/how-to-connect-your-beaglebone-via-ssh-over-usb/))

**Instructions to flash a new SD card with an image:**
([beagleboard.org getting started](http://beagleboard.org/getting-started#step3))

**Access NodeRed:**
Navigate to nodered: 192.168.8.1:1880

## Raspberry Pi Cheat Sheet:
**Instructions to connect to SSH using putty:**
([beaglebone how-to-connect](https://www.dummies.com/computers/beaglebone/how-to-connect-your-beaglebone-via-ssh-over-usb/))

**Instructions to flash a new SD card with an image:**
([beagleboard.org getting started](http://beagleboard.org/getting-started#step3))

**broadcom BCM pin numbering scheme:**
https://gpiozero.readthedocs.io/en/stable/recipes.html#pin-numbering

# Linux Cheatsheet

### File System Navigation and Information

`ls` - **List** - List the files and folders in a directory.<br>
`cd` - **Change Directory** - Move into a folder.<br>
`pwd` - **Print Working Directory** - Prints your current location to the terminal.<br>
`cp` - **Copy** - Copies a file from a location, to a location.<br>
`mv` - **Move** - Moves a file from a location, to a location.<br>
`touch` - **Touch** - Create a file.<br>
`mkdir` - **Make Directory** - Make a directory with given name.<br>
`nano` - File editor.<br>
`cat` - **Concatenate** - Concatenate files and print file contents to the terminal.<br>
`head` - Output the first part of files.<br>
`tail` - Output the last part of files.<br>
`more` - View a file and scroll through it.<br>
`less` - View a file and scroll through it. (Consumes less resources than `more`)<br>
`rm` - **Remove** - Remove files or directories.<br>
`rmdir` - **Remove Directory** - Remove empty directories.<br>
`file` - Determine file type.<br>

### System and User Info

`whoami` - **Who Am I?** - Print current user.<br>
`date` - Print or set the system date and time.<br>
`df` - Report file system disk space usage.<br>
`which` - Locate a command.<br>
`whereis` - Locate the binary, source, and manual page files for a command.<br>

### Searching

`grep` - Print lines that match patterns.<br>
`locate` - Find files by name.<br>

### Administrator

`sudo` - **Superuser Do** - Execute a command as root(superuser).<br>
`sudo su` - Switch to the root user.<br>

### Modify Permissions

`chown` - **Change Owner** - Change ownership of a file.<br>
`chmod` - **Change Mode** - Change file mode bits.<br>

### Network Information

`ping` - Send ICMP ECHO_REQUEST to network hosts.<br>
`ifconfig` - Configure a network interface.<br>
`iwconfig` - Configure a wireless network interface.<br>
`connmanctl` - **Connection Manager** - WiFi connection Utility.<br>

### Web Tools

`wget` - **Web Get** - Get a file from a server.<br>

### Process Management and Resource Monitoring

`top` - Display Linux processes.<br>
`htop` - Interactive process viewer.<br>
`kill` - Kill a process.<br>
`time` - Run programs and summarize system resource usage.<br>

### Installing Programs and Libraries

`apt-get` - APT package handling utility.<br>
`pip` - A tool for installing and managing Python packages.<br>
`pip2` - A tool for installing and managing Python2 packages.<br>
`pip3` - A tool for installing and managing Python3 packages.<br>

### Running Code and Scripts

`sh` - **SHell** - Command interpreter.<br>
`bash` - **Bourne Again SHell** - Command interpreter. (More updated than `sh`)<br>
`python` - Python interpreter (typically defaults to python2).<br>
`python2` - Python2 interpreter.<br>
`python3` - Python3 interpreter.<br>

### USB Information

`lsusb` - **List USB** - list USB devices.<br>

### Script Commands

`echo` - Display a line of text.<br>
`sleep` - Sleep for a specified number of seconds.<br>

### Command Help

`man` - **Manual** - an interface to the on-line reference manuals.<br>
`whatis` - **What Is** - display one-line manual page descriptions.<br>

### Power

`reboot` - Restart the device.<br>
`shutdown` - Power-off the device.<br>

### Other Helpful Commands

`ssh` - **Secure SHell** - OpenSSH SSH client. (remote login program)<br>
`git` - Code version control suite.<br>


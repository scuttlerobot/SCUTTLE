PYTHON SUBFOLDER README:

This folder keeps the programs for SCUTTLE robot in python.
As of 2019.02.01 the programs are written for beaglebone blue only.

**How to Run tamulink_wpa.py in Putty:**
1) create a new file using "touch tamulink_wpa.py"
2) open the file with "nano tamulink_wpa.py"
3) copy the file contents to your clipboard, and right click in Putty to paste.
4) "ctrl-X" to exit
5) "y" to save.
6) Run the script using "sudo python3 tamulink_wpa.py"

## How to install Pygame on your beaglebone blue

```
# Install required libsdl
sudo apt install libsdl1.2-dev -y

# Clone PyGame github repository
git clone https://github.com/pygame/pygame

# Move to pygame directory
cd pygame

# Build and Install PyGame
sudo python3 setup.py install
```
### Test PyGame Installation

Run ```python3```.

Type ```import pygame```.

Your installation was successful if you get an output similar to:
```
debian@scuttle:~$ python3
Python 3.5.3 (default, Sep 27 2018, 17:25:39)
[GCC 6.3.0 20170516] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import pygame
>>>
```
or
```
debian@scuttle:~$ python3
Python 3.5.3 (default, Sep 27 2018, 17:25:39) 
[GCC 6.3.0 20170516] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import pygame
pygame 2.0.0.dev0
Hello from the pygame community. https://www.pygame.org/contribute.html
>>> 
```

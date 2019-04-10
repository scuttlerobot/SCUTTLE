# S.C.U.T.T.L.E. Python
This folder contains all SCUTTLE python programs.

<br>

### Demos ([SCUTTLE/software/python/demos](https://github.com/MXET/SCUTTLE/tree/master/software/python/demos))

```demos``` contains programs demonstrating your SCUTTLE.

<br>

### Examples ([SCUTTLE/software/python/examples](https://github.com/MXET/SCUTTLE/tree/master/software/python/examples))

```examples``` contains example programs for reading sensors, driving motors, and more.

<br>


### Tools ([SCUTTLE/software/python/tools](https://github.com/MXET/SCUTTLE/tree/master/software/python/tools))

```tools``` contains tools written in python for managing your SCUTTLE.


## How to install Pygame on your beaglebone blue
To run pygame-based programs you need to install pygame on your BeagleBone.  (This is different than installing pygame/python on your PC). The steps for this are below.

Paste the following block of code into your shell and enter.

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

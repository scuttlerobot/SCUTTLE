# Explanation of Files in matlab directory:

**mrsDiffDriveDiscreteSCTL.m**

- This file originated from an example in Matlab's [Mobile Robotics Simulation Toolbox](https://www.mathworks.com/matlabcentral/fileexchange/66586-mobile-robotics-simulation-toolbox?s_tid=srchtitle)

- Mobile Robotics Simulation Toolbox as an ```.m``` file called

- mrsDiffDriveDiscrete.m  It was updated with SCUTTLE dimensions and renamed with SCTL suffix.

**Matlab GUI v1.1**

~ It's a binary that contains a ```.exe``` file to run the SCUTTLE GUI which was exported by Matlab Application Compiler.  This GUI pairs with the ```udp_matlab.py``` program to send keyboard driving commands to SCUTTLE and receive back telemetry data.

**udp_matlab.py**

- This file runs locally on the beaglebone in parallel with the matlab script or binary

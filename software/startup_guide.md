## Examples

### INA
* has instruction: plug vs unplug power to the battery & measure the voltage
* uses INA219
* does not need NodeRed flow
* Needs a slide for wiring updated (DM)

### Gamepad
* start with flow from 
* Learning:
  * joystick axes outputs and ranges
  * EITHER movement of xd, td (preferred) OR wheel speeds (needs a reason)
  * indicator for 1 button (y-button)
  * NO encoders

### SERVO
* on hold for DM - write the L1 file
* Needs a slide for connections (DM)

### ENCODER
* need to write a nodered flow including chart (2 values, 1 chart)
* L1 encoder --> L2_myEncoderExampleName --> nodered
* L1 log --> L2_myEncoderExampleName
* indicate the programs structure in a slide

### CAMERA
* Verify nominal values for radius/pixels (too far, too close)
* Update slide in software guide based on nominal values (DM)
* 

## Steps

### Downloading Image
  * DM to set up a link on scuttlerobot.org

### Location of Flows
  * flows belong in SCUTTLE/software/nodered
  * name should be descriptive of the contents, not the module
  * should have .json file extension

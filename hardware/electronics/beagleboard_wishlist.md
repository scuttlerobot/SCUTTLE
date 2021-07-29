## Wishlist for Beaglebone Blue upgrades by the SCUTTLE team:
#### STATUS: (re-collecting input from previous document as of 07.20)

### Performance Requests
* Charging & power sourcing from 3 cell LiPo batteries
* Servos must be able to be run from BOTH liPo and barrell jack, independently
* Keep at least 2 motor outputs based on PRU for high frequency driving
* make at least 4 hardware PWM outputs at TTL voltage [#313](https://github.com/adafruit/adafruit-beaglebone-io-python/issues/313#issuecomment-513881299)
* desired: increase digital GPIO input count (currently 2?) [#313](https://github.com/adafruit/adafruit-beaglebone-io-python/issues/313)
* Maintain UART function when utilizing software PWM output [#313](https://github.com/adafruit/adafruit-beaglebone-io-python/issues/313)

### Interfacing Requests - High Impact
* keeping 2 wifi hardware module is great
* gold plated pins for motors and servos to support higher current
* for I2C bus: convert JST-SH connectors to QWIIC connector shape & pin config
* countermeasure the motor output pins plastic cowling - they slide off

### Hardware Requests - Medium Impact
* Motor outputs that supports 12v 2A each
* Include reverse polarity protection on barrel power input

### Other Comments
* 5gHz wifi is low priority (to date)
* Motors functions: The need for SCUTTLE is EITHER A) drive motors at TTL voltages, with no need for high current OR B)make motor drivers able to output 12v and sufficient current.

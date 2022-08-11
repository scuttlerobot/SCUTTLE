Default Python script for running OLED and its service for executing on startup.

The script should be placed in: /usr/share/pyshared/ 
This ensures the display runs properly if the workspace is deleted for some reason.
It requires ina219.py, which is included, in the same directory to run the current sensor.

The service file goes in directory: /etc/systemd/system/ 
Use the command 'sudo systemctl daemon-reload' to register the changes.
By default the service is enabled and restarts on failure.
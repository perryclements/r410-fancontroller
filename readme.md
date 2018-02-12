# Dell R410 Fan controller

This python script reduces the noise of a Dell R410 server by controlling the fan speed with IPMI commands.

The original scrip was provided by marcusvb/r710-fancontroller on Github (Big thank you to Marcus)

The script was modified to run directly on a lightly loaded R410 running Ubuntu server with two L5630 processors.

Things changed:

1. Removed harddrive temperature check
2. Check CPU maximum temperature
3. Base CPU temperature settings on Tcase rating (63 deg C for L5630)
4. Script runs directly on server instead of on a remote machine

It's recommended to install this script via systemd, see the `.service` file provided. You can install it as follows:

```
# Place the file in the systemd directory
nano /etc/systemd/system/fan-controller.service

# Make executable
chmod 644 fan-controller.service

# Reload systemd, enable the service and start it.
systemctl daemon-reload
systemctl enable fan-controller.service
systemctl start fan-controller.service

# Check to see if it's running
service fan-controller status
```

This allows the script to be enabled at boot.

This script is provided as is. I am not responsible for any damage done to your server. See the license for more information.

By perryclements on Github.

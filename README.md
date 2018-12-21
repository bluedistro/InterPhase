### Requirements
* psutil
* smtplib

### Steps for setting up Script as a Service to enable autorun on Lunix Systems

* After cloning this repo, open the script messaging.py and enter your email credentials to enable email notification

* For simplicity sake, copy the folder to /usr/bin after editing messaging.py

* Create a service script using the command: sudo nano /lib/systemd/system/interface.service

* Add the following scripts to the file (interface.service), save and exit the nano editor using [CTRL-X], [Y] then [ENTER].:

	[Unit]
	Description=My Script Service
	After=multi-user.target

	[Service]
	Type=idle
	ExecStart=/usr/bin/python /usr/bin/interphase/interface.py > /usr/bin/interphase/logs.txt 2>&1

	[Install]
	WantedBy=multi-user.target

* Change the permission on the service file to read only using the command: sudo chmod 664 /lib/systemd/system/interface.service

### Configuring Systemd (Run the next lines)

* Run this command to reload daemon: sudo systemctl daemon-reload
* Enable the service by running this command: sudo systemctl enable interface.service

* finally reboot your system by running this command: sudo reboot 

* Afterwards, check status of service using the command: sudo systemctl status interface.service

### Note: When all is setup properly, the status should be active and running
 

Author - Kingsley Biney
Email - bineykingsley36@gmail.com

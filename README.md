flood-pi
========
> Flood detection for Rasperry Pi


Environment Set Up
---
```
$ sudo apt-get update
$ sudo apt-get install python-pip python-dev build-essential

$ sudo pip install virtualenv
$ sudo pip install virtualenvwrapper
```
- update .bashrc as described here: [http://virtualenvwrapper.readthedocs.org/en/latest/install.html](http://virtualenvwrapper.readthedocs.org/en/latest/install.html)
(had to change __virtuelenvwrapper.sh__ location to _$HOME/build/virtualenvwrapper/virtualenvwrapper.sh_)

Allow SPI interface & Reboot
---
As described here: [http://www.raspberrypi-spy.co.uk/2013/10/analogue-sensors-on-the-raspberry-pi-using-an-mcp3008/](http://www.raspberrypi-spy.co.uk/2013/10/analogue-sensors-on-the-raspberry-pi-using-an-mcp3008/)

__Actually had to follow instruction for local install of spidev - the one from pip isn't recognized for some reason__

Install
---
```
$ git clone https://github.com/bustardcelly/flood-pi.git flood-pi
$ cd flood-pi
$ mkvirtualenv flood-pi

$ workon flood-pi
$ sudo pip install -r requirements.txt ---system-site-packages
```

Start
---
```
$ sudo python floodpi.py -n bustardcelly@gmail.com
```

Add to init.d
---
```
$ sudo cp /home/pi/flood-pi/floodpi.sh /etc/init.d/floodpi
$ sudo update-rc.d floodpi defaults
$ sudo /etc/init.d/floodpi start
```
flood-pi
========
> Flood detection for Rasperry Pi

The basic premise is that a flood is detected by water completing a circuit and reading an analog value through an ADC on the Raspberry Pi. 

The end leads are 2 copper plates relatively close in proximity. When submersed in water, the circuit is complete and the ADC reports a value that is considered within "flood range" - the occasional low value is expected and higher values tend to mean that the plates have started to touch each other.

When a flood is detected, an email is sent out as notification.

Hardware
---
Check out the [setup](https://github.com/bustardcelly/flood-pi/blob/master/docs/flood-pi.png)

* [Raspberry Pi](http://www.raspberrypi.org/)
* [MCP3008](https://www.adafruit.com/products/856)
* [Edimax WiFi Adapter](http://www.edimax.com/edimax/merchandise/merchandise_detail/data/edimax/global/wireless_adapters_n150/ew-7811un)
* LED
* 100 ohm Resister
* Copper Plating (cut into 2 strips)

Environment Set Up
---
Base Image: [Raspbian-Wheezy](http://www.raspberrypi.org/downloads/)

SSH into your pi and issue the following:

```
$ sudo apt-get update
$ sudo apt-get install python-pip python-dev build-essential

$ sudo pip install virtualenv
$ sudo pip install virtualenvwrapper
```
- update .bashrc as described here: [http://virtualenvwrapper.readthedocs.org/en/latest/install.html](http://virtualenvwrapper.readthedocs.org/en/latest/install.html)

Allow SPI interface & Reboot
---
_This section is only if you intend to use the SPI interface. It is possible to use any other standard pin along with an ADC (such as the [mcp3008](https://www.adafruit.com/products/856) used in this project)._

Follow the instructions described here: [http://www.raspberrypi-spy.co.uk/2013/10/analogue-sensors-on-the-raspberry-pi-using-an-mcp3008/](http://www.raspberrypi-spy.co.uk/2013/10/analogue-sensors-on-the-raspberry-pi-using-an-mcp3008/)

__Actually had to follow instruction for local install of spidev - the one from pip isn't recognized for some reason__

Set-Up WiFi Adapter
---
The [Edimax WiFi Adapter](http://www.edimax.com/edimax/merchandise/merchandise_detail/data/edimax/global/wireless_adapters_n150/ew-7811un) was used in this project.

I set up VNC on my pi, and used the __WiFi Config__ program pre-installed on wheezy, as described [here](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-3-network-setup/setting-up-wifi-with-raspbian).

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
The program dependes upon a configuration file named __config.ini__ relative to the __floodpi.py__ file. A __config.ini.template__ file is available from the repo and should be copied and values changed as needed.

An example of the __config.ini__ file to provide is:

_config.ini_
```
[smtp]
user = <name@email.com>
password = <your password>
```

__** You must provide your own custom config.ini file in order for the notifications to work.__

```
$ sudo python floodpi.py -n bustardcelly@gmail.com
```

Add to init.d
---
Included in the repo is a __floodpi.sh.template__ file that can serve as an init script. You will need to modify the __YOU_EMAIL_HERE__ value to be your email and change the filename to __floodpi.sh__ before doing the following:

```
$ sudo cp /home/pi/flood-pi/floodpi.sh /etc/init.d/floodpi
$ sudo update-rc.d floodpi defaults
$ sudo /etc/init.d/floodpi start
```

Reporting
---
Reporting is optional and service properties can be set in the __config.ini__ file. The service properties are read from the _service_ option properties:

_config.ini_
```
[service]
baseUrl = <service host>
basePort = <service port>
postEndpoint = <endpoint to POST level reading data (eg, level)>
confEndpoint = <endpoint to POST configuration data (eg, configuration)>
```

As an example, the [flood-pi-admin](https://github.com/bustardcelly/flood-pi-admin) project is a RESTful service that provides an API to POST levels and present consumed data.

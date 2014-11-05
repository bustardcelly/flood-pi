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

```
$ git clone https://github.com/bustardcelly/flood-pi.git flood-pi
$ cd flood-pi
$ mkvirtualenv flood-pi

$ workon flood-pi
$ pip install -r requirements.txt --system-site-packages
$ sudo python flood-pi.py
```
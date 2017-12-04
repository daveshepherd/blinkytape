# BlinkyTape examples

This is a small collection of example scripts for working with a BlinkyTape LED strip.

## Install as a service

Clone the repository to /home/pi/blinkytape

```
$ sudo mv /home/pi/blinkytape/service-status.service /lib/systemd/system/
$ sudo systemctl daemon-reload
$ sudo systemctl enable service-status
$ sudo systemctl start service-status
$ sudo systemctl status service-status
```
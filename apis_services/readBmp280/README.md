# README for readBmp280

This programme reads pressure, temperature and humidity from a BMP280/bME280 sensor attached to a Pi via the GPIO header.

## Connection to the Pi
``` bash
Vin => 1 (or any 3.3v pin) 
Sda => 3 (but can be any of GP02,06,10,14,18,26)
Scl => 5 (but can be any of GP03,07,11,15,19,27)
Gnd => 9 (or any Gnd pin)
```
Note: you can use any of the specified pins, the device is actually addressed by its I2C address 0x76. 

## Python Requirements
I recommend creating a python virtual environment. Mine is called pywws: if you choose a different name you'll need to update *bmp280.sh* to activate it properly. 
Requirements are *paho-mqtt*, *smbus* and *bme280* and can be installed with pip using the requirements file. 

## Configuration
Update *mqConfig.py* with your MQ broker details.

Update *whConfig.py* with your SQL database details and your station's altitude above sea level. This is used to calibrate the pressure readings.  You can also change the logging location from the default of `~/weather/logs`.

Update `SRCDIR` in *bmp280.service* to reflect the location in which you've installed the script.

## Installation
Run *installservice.sh* to install and start a service *bmp280*
Check its status with *systemctl status bmp280*.
There should also be a log in `~/weather/logs` unless you changed the log location.

# Logging Output
The programme logs into `~/weather/logs`. You can change this by updating *whConfig.py* and restarting the service. 

# MQ output
The service publishes to four MQTT topics 
* bmp280/temp_in_c
* bmp280/press_rel
* bmp280/humidity_in
* bmp280/time 

The last is the timestamp of the data so you can check for stale values. 

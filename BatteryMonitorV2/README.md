# Readme for Battery Monitor V2

This repo provides code that can be run on an 8266-compatible Wemos D1 Mini with wifi board, to measure battery voltage and report it via MQ.

## Hardware Required
* Wemos D1 Mini with Wifi.
* Wemos power shield for D1 Mini.
* Assorted resistors.
* A multimeter to calibrate the device. 
* Soldering iron. 

## Hardware Build
To measure up to 20V:

* Solder the +3.3V, +5V, Gnd and A0 pins on the Mini to the corresponding pins on the shield.
* Then either:
  * Solder input leads to the two solder input pads. 
  * Solder a 2M resistor between +ve input pad and A0 on the Mini. 
* Or
  * Solder a 2M resistor between the +ve back of the jack socket and A0 on the Mini.
  * And then use the input jack to feed the measured voltage to the device. 

The resistor is required because the D1 Mini can only accept up to 1V on any of its analogue pins. 
Internally it contains a 220+100 Ohm resistor bridge so that natively it can measure up to 3.2V, but 
to measure more we need to increase the reistance of the first element. This can be done by adding a resistor from +ve in to A0. 
An additional at least 1.2M is required to measure 12V, but a 2M resistor will do fine. 

## Building the Code
Using the Arduino IDE:
* install the 8266 board as explained [here](https://arduino-esp8266.readthedocs.io/en/latest/installing.html) 
* Select board `Lolin(Wemos) D1 R2 and Mini`
* Install the `PubSubClient` library by Nick O'Leary.
* Rename `siteinfo.h.sample` to `siteinfo.h` and then update the file with your site-specific information. 
This file stores your Wifi details, MQ server and topic details, and a scaling factor you will 
adjust to get the voltage correct. For now, leave it at 4.2.

Now compile the sketch and deploy it to your Wemos D1 Mini.  
The code will publish to a topic "sensors/batteries/`topicname`/voltage" so if you were monitoring say a weatherstation you might set topicname to "weatherstation". 

## Calibration
Out of the box its likely the reported voltage will be initially incorrect. To calibrate it:
* Apply +12V to the input socket or pads (whichever you chose earlier)
* Using a multimeter measure the exact input voltage.
* Monitor MQ for the sensors/battery topic and note the reported voltage. 
* Adjust `scalefactor` as needed and redeploy the code. 

Note: At present, only unencrypted connections to MQ are supported.

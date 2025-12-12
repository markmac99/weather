# Readme for Battery Monitor V2

This repo provides instructions for monitoring battery voltage over WiFi, for example if you want
to monitor the voltage of a solar panel powered weatherstation or other off-grid device. 
It uses an 8266-compatible Wemos D1 Mini board with Wifi and the voltage data are published to MQ. 

## Hardware Required
* Wemos D1 Mini with Wifi.
* Wemos power shield for D1 Mini.
* Assorted resistors (see below).
* A multimeter to calibrate the device. 
* Soldering iron. 

You will obviously also need an MQ server to publish to. 
You can use the free one at [Mosquitto.org](https://test.mosquitto.org/) if you don't have your own. I don't 
think it'll work with HiveMQ as that requires TLS which is not supported. 

## Resistor selection
The resistor is required because the D1 Mini can only accept up to 1V on any of its analogue pins. 
Internally it contains a 220+100 Ohm resistor bridge so that natively it can measure up to 3.2V, but 
to measure more we need to increase the reistance of the first element. This can be done by adding a resistor from +ve in to A0. 

I used a 2.2M resistor which allows me to measure voltages up to about 25V with a step of 0.025V. This caters
for typical 12V and 24V situations. The spreadsheet in the `docs` folder explains the maths and lets you 
calculate your own requirements. 

## Hardware Build
To measure up to 20V:

* Solder the +3.3V, +5V, Gnd and A0 pins on the Mini to the corresponding pins on the shield.
* solder D0 to RST on the mini. This allows the device to wake from deep sleep (powersaving mode). 

* Then either:
  * Solder a 2M resistor between +ve input pad and A0 on the Mini. 
  * Solder input leads to the two solder input pads. 

* Or
  * Solder a 2M resistor between the +ve back of the jack socket and A0 on the Mini.
  * And then use the input jack to feed the measured voltage to the device.


## Building the Code
Using the Arduino IDE:
* Install the Wemos CH340 driver from [here](https://www.wemos.cc/en/latest/ch340_driver.html)
* install the 8266 board as explained [here](https://arduino-esp8266.readthedocs.io/en/latest/installing.html) 
* Select board `Lolin(Wemos) D1 R2 and Mini`
* Install the `PubSubClient` library by Nick O'Leary (see [here](https://docs.arduino.cc/libraries/pubsubclient/)).
* Copy `siteinfo.h.sample` to `siteinfo.h` and then update the file with your site-specific information. 
This file stores your Wifi details, MQ server and topic details, and a scaling factor you will 
adjust to get the voltage correct. For now, leave it at 24.4 which will be roughly right for 12V input.
* The appllication will publish to an MQ topic "sensors/batteries/`topicname`/voltage" for example if you are monitoring a weatherstation you might set topicname to "weatherstation". 

* Now compile the sketch and deploy it to your Wemos D1 Mini. 

## Calibration
Out of the box its likely the reported voltage will be initially incorrect. 

To calibrate it:

* Apply +12V to the input socket or pads (whichever you chose earlier)
* Using a multimeter measure the exact input voltage.
* Monitor MQ for the sensors/battery topic and note the reported voltage. 
* Adjust `scalefactor` as needed and redeploy the code. 

Note: At present, only unencrypted connections to MQ are supported.

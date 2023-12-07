# weather related stuff

Various weatherstation and weather related stuff

I run two weatherstations, a maplin WH1080 compatible unit and a Bresser 5-in-1 unit.

## pywws 
This is a copy of the excellent pywws python weatherstaton for Raspberry Pi. I originally used this to collect
data from the WH1080. However over time the unit developed a problem with its USB port and in 2023 i retired pywws. 

## website
An implementation of the dragontail weather website, consuming data initially from pywws, but later from other sources. 

## dummyusb
When the USB port on the WH1080 malfunctioned, i realised i could recover data from the outside sensors using an RTL-433 dongle. To replace the indoor sensors i am using a BME280 breakbout board in a Raspberry pi.  So i wrote some software to capture the data to file, and then created a dummy USB driver for pywws that reads the file and feeds the data to pywws. 

The RTL433 and BME280 data are being published to MQ Series along with data from my Bresser weatherstation. 

## mmwws
A replacement for pywws. Instead of using the dummy usb driver, i decided to simply read the data from MQ and directly generate the javascript required by the dragontail website. 

## apis_services
Various APIs and services to manage weather data

### getwu
Retrieve my bresser data from Weather Underground. Data can't be directly retrieved from the Bresser so i run this service on an AWS EC2 instance to retrive data from Weather Underground and publish it to my MQ server on a topic sensors/bresser_wu

In addition, I'm running a vanilla instance of RTL433 tuned to 833MHz to retrieve data from the Bresser's outside sensors and post it to MQ in a topic sensors/rtl_433/P172/C0. The config file for this is in this folder. 

### readBmp280
This service runs on a Pi and reads data from a BMP/BME280 temperature, humidity and pressure sensor to provide indoor readings. The data are published to MQ in a topic sensors/bmp280 and saved to file on a Pi3. 

### rtl433ToMQ
A second instance of RTL433 runs on the same Pi3 as the BME280 to retrieve the WH1080 outdoor sensor data at 433 MHz. For some reason this insance isn't able to directly publish to MQ, so i have a second process that reads the data from file and publishes it to MQ in topic sensors/wh1080. I need to revisit this klunky process. 

### weatherapi
This reads the data files created by readBmp280 and rtl433ToMQ and exposes it via a REST API so that i can consume the data on my webserver which is running on AWS. 

### getDataAws
Reads data from the above API and adds it to a datafile on my AWS server. The data are then consumed by mmwws. 

# pibackup
a backup of the installation on the Pi, in case i need to refer to it. 

## Retired APIs 
### subswh1080
subscribed to the MQ data and wrote to file. Never properly worked, not sure why.

### whotodummy 
This read the data created by the bmp280 and rtl433 and saved it as a file for consumption by the dummy USB driver for pywws. 

### weatherfwd 
Was used to read data from an API and publish it to OpenHAB. I had this running on the old PyWWS machine, before i was able to publsh the data directly via MQ. No longer used. 

### tofb 
legacy code to send data to facebook. No longer supported by FB, kept for historical purposes. 


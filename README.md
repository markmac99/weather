# weather related stuff

Various weatherstation and weather related stuff

I run two weatherstations, a WH1080 compatible unit from Maplin and a Bresser 5-in-1 unit. I also have a bmp280 chip providing pressure and indoor temperature and is being read by a Raspberry Pi via GPIO. 

The Weatherstations and bmp280 data are being published to MQ Series along with other data that i'm calculating such as wind chill, heat index and dew point. The APIs and Maplin data collection are running on a Pi3, imaginatively named `weatherpi3`. The Bresser data collection runs on a second Pi3 named `metsatpi` which is also running Raspberry NOAA v2 (hence the name!). 

Once collected, the Maplin and bmp280 data are pushed to a MySQL / MariaDB database running on webserver hosted on AWS with a backup database on `weatherpi3`. This minimises the chance of data loss. 

## website
An implementation of the dragontail weather website. This initially consumed data from from pywws, but later i changed it to read data from files created by my own programme `mmwws`. 

## mmwws
A replacement for pywws (see retired section below). The application reads from the SQL database and generates the javascript required by the dragontail pages, and which are then pushed to my website. 

## BatteryMonitorV2
This is an app that runs on a Wemos D1 Mini with Wifi to read the battery voltage of the solar array powering the Maplin station. Theres a full explanation in the folder's readme. 

## apis_services
Various APIs and services to manage weather data

### wh1080_433
A vanilla instance of RTL_433 tuned to 433MHz to retrieve data from the WH1080 outdoor sensor data, publishing to a topic on MQ, `sensors/rtl_433_2/P32/C0`. The config file for this is in this folder.

### bresser_rtl433
A vanilla instance of RTL_433 tuned to 833MHz to retrieve data from the Bresser's outside sensors and post it to MQ in a topic `sensors/rtl_433/P172/C0`. The config file for this is in this folder.

### maplin2mq
This service reads the Maplin data from MQ, posts the data to the SQL databases and then augments it with additional values `feels_like` and `dew_point` which are pubilshed back to MQ, . 

### readBmp280
This service reads data from a BMP/BME280 temperature, humidity and pressure sensor to provide indoor readings. The data are published to MQ in a topic `sensors/bmp280` and posted to SQL. 

### setupdb
creates the SQL database. 

### getbresserwu
Retrieve additional bresser data from Weather Underground. Some data can't be directly retrieved from the Bresser but is available from Wunderground somehow. So i run this service on one of my Raspberry Pis to retrive data from Weather Underground and publish it to my MQ server on a topic `sensors/bresser_wu`

### getbressrain
This simple script reads bresser rain data from MQ and calculates hourly rainfall stats. This isn't available from the station directly. The data are published to `weather/bresser/rain_hourly_mm`

### mqtoMastodon
Attempts to post weather data to Mastodon, but i tink this is borked. 

# pibackup
a backup of the installation on the Pi, in case i need to refer to it. 


## Retired APIs 
### subswh1080
subscribed to the MQ data and wrote to file. Never properly worked, not sure why.

### weatherfwd 
Was used to read data from an API and publish it to OpenHAB. I had this running on the old PyWWS machine, before i was able to publsh the data directly via MQ. No longer used. 

### weatherapi
This runs on the same Pi3 and reads the data files created by readBmp280 and rtl433ToMQ and exposes it via a REST API so that i can consume the data on my webserver which is running on AWS. 

### tofb 
legacy code to send data to facebook. No longer supported by FB, kept for historical purposes. 

## pywws 
This is a copy of the excellent pywws python weatherstaton for Raspberry Pi. I originally used this to collect
data from the WH1080. However over time the unit developed a problem with its USB port and in 2023 i retired pywws. 

## dummyusb
When the USB port on the WH1080 malfunctioned, i realised i can read data from the outside sensors using an RTL-433 dongle. To replace the indoor sensors i am using a BME280 breakbout board in a Raspberry pi.  So i wrote some software to capture the data to file (see services below), and then created a dummy USB driver for pywws that reads the file and feeds the data to pywws. 

### getDataAws
Read data from the file pushed by whtoAws and added it to a SQL database on my AWS server. The data are then consumed by mmwws. 

### whotoAws 
This reads the data created by `wh1080_433` and `bmp280` (see below) and pushes it to the SQL databases. 


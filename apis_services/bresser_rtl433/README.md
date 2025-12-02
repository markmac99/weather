# README for bresser_rtl433

This code reads from a Bresser 5-in-1 weatherstation and posts the results to MQTT. The process makes use of *rtl_433* to read from the weatherstation's outdoor sensors which broadcast at 833MHz. 

## Prerequisites
Clone the git repo [rtl_433](https://github.com/merbanan/rtl_433.git), and build it. 
Follow the CMake instructions in that repository's documentation (`docs/BUILDING.md). 

This will install the application into `/usr/local/bin/rtl_433` with a default config file in `/etc/rtl_433.conf`. We are not using the default file so you can ignore it. 

## Update the config file in this repo
Open *rtl_433.conf* in a text editor and fine the line starting with:
``` bash
output mqtt://
```
Update the hostname, port, user and password to reflect your own MQTT server details.
You can also alter the topic string if you want. 

## Testing rtl_433
Test *rtl_433* by plugging in your RTL-SDR dongle, and running 
```bash
/usr/local/bin/rtl_433 -c ./rtl_433.conf
```
You should get some initialisation messages, and then after a short while you should start getting data
from any 833 MHz sensors in your area published to your MQ server. This could include thermostats, garage door openers, tyre pressure monitors, and other household devices as well as your weatherstation!  Press Ctrl-C to end data capture. 

If you get an error that permissions are wrong, copy the UDEV rules file in this repository to the location
shown below and restart the pi:
``` bash
sudo cp rtl-sdr.rules /etc/udev/rules.d
sudo reboot
```
You should now be able to run *rtl_433* without error.

# Install the Service
Once you're happy its working you can install the service:
``` bash
./installservice.sh
```

Check the service' status as follows
```bash
systemctl status rtl_433
```

That's it. Your weatherstation data is now being written to MQTT to a topic named *sensors/rtl_433_2/P32/C0*

You can check this using any MQTT client. I use both `mosquitto` at the commandline and `MQTT-Explorer` for Windows. Here's some typical output from `mosquitto_sub`. 

``` bash
(pywws) pi@weatherpi3:~/source/wh1080_rtl433 $ mosquitto_sub -h metsatpi  -t 'sensors/rtl_433/#' -i frobozz
2025-12-02T13:15:48
172
576021508
0
1
0.5
0.5
338
1147.20007
1
1
CRC
...
```

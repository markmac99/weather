# README for rtl433ToMQ

This code reads from a WH1080 / Maplin weatherstation and posts the results to MQTT

The process makes use of *rtl_433* to read from the weatherstation's outdoor sensors. 
*rtl_433* can natively write to MQ however i found that 
this would not work on my Pi3 due to issues with SSL. Additionally i wanted to post 
some derived data not available directly from the weatherstation such as dew point, wind chill and heat index.
So it was easier to get *rtl_433* to write JSON to a file, then read this and post it to MQTT.

## Prerequisites
You'll need to install *rtl-sdr* and its development libraries, plus development tools to build *rtl_433*. I 
also strongly recommend you install into a python virtual environment to avoid corrupting your Pi's standard 
python environment used by apt and othe system tools.
``` bash
sudo apt-get install rtl-sdr librtlsdr-dev
sudo apt-get install libtool libusb-1.0-0-dev build-essential cmake pkg-config
sudo apt-get install python3-venv
```
## Building rtl_433
Download the code from [github](https://github.com/merbanan/rtl_433), then build and install it:
``` bash
mkdir -p  ~/source 
cd ~/source
git clone https://github.com/merbanan/rtl_433.git
cd rtl_433
mkdir build
cd build
cmake ..
make
sudo make install
```
This will install *rtl_433* into */usr/local/bin*

## Testing rtl_433, and a possible gotcha
Test *rtl_433* by plugging in your RTL-SDR dongle, and running 
```bash
rtl_433
```
You should get some initialisation messages, and then after a short while you should start getting data
from any 433 MHz sensors in your area. This could include thermostats, garage door openers, tyre pressure monitors,
and other household devices as well as your weatherstation! 

If you get an error that permissions are wrong, copy the UDEV rules file in this repository to the location
shown below and restart the pi:
``` bash
sudo cp rtl-sdr.rules /etc/udev/rules.d
sudo reboot
```
You should now be able to run *rtl_433* without error.

# Install the Services
Make a folder in the pi user's home directory called *~/weather* and copy all files from this repo into this location. 
``` bash
mkdir -p ~/source/wh1080_433
cp *.sh *.py *.service  ~/source/wh1080_433
mkdir -p ~/venvs
```
Next, create a python virtual environment, activate it and install the python libraries. 
``` bash
python3 -m venv ~/venvs/pywws
source ~/venvs/pywws/bin/activate
pip install -r ~/source/wh1080_433/requirements.txt
```

Edit the config file *mqConfig.py* to reference your MQTT broker and port, then you can install and start the services.  
``` bash
cd ~/source/wh1080_433
./installservice.sh
```
This should install two services *rtl_433* which reads from the weatherstation sensors. Test as follows:

```bash
systemctl status rtl_433
```

*rtl_433* writes data to a file *~/weather/maplinstn/weatherdata.json*. The service logfiles are written to *~/weather/logs*, and error messages may also be logged to syslog. 

Each time the service is restarted it will attempt to rename the JSON file and start a new one, and to delete any JSON and log files that are more than 14 days old. This ensures that space usage is not excessive. You should therefore either schedule your Pi to restart each day, or use cron to restart the service. 

That's it. Your weatherstation data is now being written to MQTT to a topic named *sensors/wh1080*

``` bash
$ mosquitto_sub -h someserver  -t sensors/# -i frobozz -d
Client frobozz received PUBLISH (d0, q0, r0, m0, 'sensors/wh1080/time', (19 bytes)) 2023-11-25 10:34:35
Client frobozz received PUBLISH (d0, q0, r0, m0, 'sensors/wh1080/model', (17 bytes)) Fineoffset-WHx080
Client frobozz received PUBLISH (d0, q0, r0, m0, 'sensors/wh1080/subtype', (1 bytes)) 0
Client frobozz received PUBLISH (d0, q0, r0, m0, 'sensors/wh1080/id', (2 bytes)) 86
Client frobozz received PUBLISH (d0, q0, r0, m0, 'sensors/wh1080/battery_ok', ... (1 bytes)) 1
Client frobozz received PUBLISH (d0, q0, r0, m0, 'sensors/wh1080/temperature_C', ... (3 bytes)) 5.0
Client frobozz received PUBLISH (d0, q0, r0, m0, 'sensors/wh1080/humidity', ... (2 bytes)) 34
Client frobozz received PUBLISH (d0, q0, r0, m0, 'sensors/wh1080/wind_dir_deg', ... (3 bytes)) 293
Client frobozz received PUBLISH (d0, q0, r0, m0, 'sensors/wh1080/wind_avg_km_h', ... (5 bytes)) 4.896
Client frobozz received PUBLISH (d0, q0, r0, m0, 'sensors/wh1080/wind_max_km_h', ... (5 bytes)) 7.344
Client frobozz received PUBLISH (d0, q0, r0, m0, 'sensors/wh1080/rain_mm', ... (3 bytes)) 0.3
Client frobozz received PUBLISH (d0, q0, r0, m0, 'sensors/wh1080/mic', ... (3 bytes)) CRC
Client frobozz received PUBLISH (d0, q0, r0, m0, 'sensors/wh1080/feels_like', ... (4 bytes)) 4.12
```
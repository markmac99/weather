# README for maplin2mq

This code reads WH1080 / Maplin weatherstation data from MQTT and posts it to my SQL database.
It also augments it by adding feels_like and dewpoint values. 

## Prerequisites
You must have a WH1080-compatible weatherstation such as the Maplin unit i have.
You must have installed [rtl_433](https://github.com/merbanan/rtl_433.git) and configured it to publish data to MQTT. 

See [wh1080_433](https://github.com/markmac99/weather/tree/master/apis_services/wh1080_433) in this repository for how to do that. 

# Install the Software
Clone this repo to a location of your choice such as `$HOME/source`.
Create a python virtual environment named `pywws` and install the requirements: 
``` bash
python3 -m venv ~/venvs/pywws
source ~/venvs/pywws/bin/activate
pip install -r $HOME/source/requirements.txt
```
Update *mqConfig.py* with the details of your MQTT server. 
Update *whconfig.py* with the details of your primary and backup SQL databases. 

# Install the Service
Now you can install and start the services.  
``` bash
./installservice.sh
```
Test that the service is running as follows: 
```bash
systemctl status maplin2mq
```

# Logging Output
The programme logs into `~/weather/logs`. You can change this by updating *whConfig.py* and then restarting the service. 


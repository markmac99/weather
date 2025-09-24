# README for rtl433ToMQ

This code reads WH1080 / Maplin weatherstation data from MQTT and saves it to a file.
It also augments it by adding feels_like and dewpoint values. 

## Prerequisites
You'll need to install `wh1080_433` from this repo to grab data from the weatherstation and post it to MQ. 

# Install the Service
Clone this repo to `$HOME/source` and then edit `mqConfig.py` to reflect your MQ server details. 

Create a virtual environment named `pywws` and install the requirements in it with 
``` bash
python3 -m venv ~/venvs/pywws
source ~/venvs/pywws/bin/activate
pip install -r $HOME/source/requirements.txt
```

You may need to edit the bash scripts to reflect your user's homedir. Mine was `/home/pi` but yours may be different

Now you can install and start the services.  
``` bash
./installservice.sh
```
Test that the service is running as follows: 
```bash
systemctl status maplin2mq
```

This process will add two new topics to MQ for the feels_like and dewepoint values, and will also write the raw data to `~/weather/maplinstn/weatherdata.json`. 

Logs are written to `~/weather/logs/wh1080_mq.log`

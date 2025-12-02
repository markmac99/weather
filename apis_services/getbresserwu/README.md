# README for getbresserwu

My Bresser 5-in-1 weatherstation has very limited interfaces to collect data from it programatically. Notably the *indoor* sensor data is not accessible via the API. However, you can configure the station to publish to Weather Underground. This programme collects the indoor sensor data from Weather Underground via their API and publishes it to MQTT. The programme also publishes some data to my OpenHAB installation, via OpenHAB's cloud API gateway. 

## Keys
To use Weather Underground you'll need a StationID and API Key. 
To use Openhab you'll need an OH username and password. 
* The WU API key must be stored in *~/.ssh/wupass*. This file should be set to 0600 permissions and consdered secret.
* The OH user/pass must be stored in *~/.ssh/myohpass* on separate lines. Again treat this as a secret file. 

## Configuration
Update *mqConfig.py* with your MQ server details.
Update *wuconfig.py* with your station WU ID 
Update SRCDIR in *getbresswu.service*
Update HOMEDIR in *GetBresserData.sh*

Now run `installGetWu.sh` to install and start the `getbresswu` service. 

## Logs
Logs are written to `~/weather/logs` - you can change this by updating the logdir in *wuconfig.py* and restarting the service. 
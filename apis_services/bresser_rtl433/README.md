# README for bresser_rtl433

My Bresser 5-in-1 weatherstation has very limited interfaces to collect data from it programatically.

## Outdoor sensors
An instance of `rtl_433` tuned to 833MHz can read the *outdoor* sensors and publish 
their values to MQTT.

## Indoor sensors
These aren't published but can be read back from Weather Underground - see `getbresserwu` for more info. 

## Rain data
The sensor data only shows instantaneous rain measurements, so i have another programme `bressrain` that calculates hourly and daily stats and publishes them to MQTT. 
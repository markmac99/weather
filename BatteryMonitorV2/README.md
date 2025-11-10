# Readme for Battery Monitor V2

This repo provides code that can be run on an 8266-compatible Wemos D1 Mini with wifi board, to measure battery voltage and report it via MQ.
At present, only unencrypted connections to MQ are supported.

To use the code, compile and deploy it to your Wemos D1 Mini using the Arduino IDE. 

You'll need to create a file `secrets.h` containing the following secrets:

``` bash
const char ssid[] = "yourssid";
const char password[] = "yourwifipasssord";
const char mqtt_username[] = "your MQ username";
const char mqtt_password[] = "your MQ password";
```

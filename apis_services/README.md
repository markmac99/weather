# How the APIs hang together

## WeatherPi3

* `rtl433` reads Bresser weatherstation data and publishs whats avalable to MQ.
* `bressrain` reads total rain data from MQ and works out the hourly rain rate then publishes back to MQ.
* The Bresser weatherstation is also configured to publish to WeatherUnderground.
* `getbresserwu` reads additional Bresser WS data from WeatherUnderground and publishes to MQ. These data are not available via its 433MHz wireless interface for some reason..
  
* `wh1080_433` reads from the Maplin weatherstation and publishes to MQ.
* `readBmp280` reads from the BMP280 in my study and writes to `~/weather/maplinstn/bmp280.json`.
* `maplin2mq` reads the data from MQ and adds it to a JSON file `~/weather/maplinstn/weatherdata.json`. Also publishes extra fields to MQ.
* `whtoAws` reads the Maplin and BMP280 JSON data, writes a single record in `~/weather/` and then sends the data to the SQL database running on AWS.

* `mqToMastodon` reads some weather data from MQ and publishes it to Mastodon. 

* `checks` contains some service monitoring

## AWS Server
* `mmwws` reads from the SQL database to create the required javascript. 
  
## Other Servers
* `diskspacechecks` monitors the hardware on my Linux server and publishes data to MQ
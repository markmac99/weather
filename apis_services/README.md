# How the APIs hang together

## WeatherPi3

* `rtl433` reads Bresser weatherstation data and publishs whats avalable to MQ.
* `bressrain` reads total rain data from MQ and works out the hourly rain rate then publishes back to MQ.
* The Bresser weatherstation is also configured to publish to WeatherUnderground.
* `getbresserwu` reads additional Bresser WS data from WeatherUnderground and publishes to MQ. These data are not available via its 433MHz wireless interface for some reason..
  
* `wh1080_433` reads from the Maplin weatherstation and writes to `~/weather/maplinstn/weatherdata.json`.
* `readBmp280` reads from the BMP280 in my study and writes to `~/weather/maplinstn/bmp280.json`.
* `whtoAws` reads the Maplin and BMP280 data merges it into a single file `~/weather/weatherdata.json` and pushes the file to AWS for use in the website.
* * `maplin2mq` reads the file created by `whToAws` and publishes to MQ.

* `mqToMastodon` reads some weather data from MQ and publishes it to Mastodon. 

* `checks` contains some service monitoring

## AWS Server
* `getweatherdata` reads the uploaded json file and updates the Parquet tables
  
## Other Servers
* `diskspacechecks` monitors the hardware on my Linux server and publishes data to MQ
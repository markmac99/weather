# How the APIs hang together

* `wh1080_433` reads from the Maplin weatherstation and publishes to MQ.
* `bresser_rtl433` reads Bresser weatherstation data and publishs whats avalable to MQ.
* `readBmp280` reads from the BMP280 in my study and sends it to a mySQL or MariaDB database.
* `getbresserwu` reads additional Bresser WS data from WeatherUnderground and publishes to MQ. These data are not available via its 433MHz wireless interface for some reason..
* `bressrain` reads total rain data from MQ and works out the hourly rain rate then publishes back to MQ.
* The Bresser weatherstation is also configured to publish to WeatherUnderground.
* `maplin2mq` reads the data from MQ and sends it to a mySQL or MariaDB database. Also publishes extra fields to MQ.
  
* `checks` contains some service monitoring
* `diskspacechecks` monitors the hardware on my Linux server and publishes data to MQ
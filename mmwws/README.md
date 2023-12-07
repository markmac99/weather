# README for mmwws

In 2023, i retired pywws. To ensure continuity on my weather website, i wrote  code to create the javasacript and png files required by Dragontail. The python code in this folder reads data from a pandas dataframe and generates these files 
- temperature graphs
- pressure graphs
- rainfall graphs
- wind graphs
- wind roses
- tables of the last 24h to 24 mths
- uploads to the Met Office, Wunderground and OpenWeathermap

Data are read from an API thats running on a Pi3 and is reading from my weatherstation and an indoor sensor. See 
[here](https://github.com/markmac99/weather/tree/master/apis_services/getDataAws) for the code that reads the API, and [here](https://github.com/markmac99/weather/tree/master/apis_services/weatherapi) for the code that publishes it.

Improvements that could be made
- merge the API reader into this tool.
- secure the API.
- 
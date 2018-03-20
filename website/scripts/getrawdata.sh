#!/bin/bash
rsync -avz pi@raspberrypi:weather/data/ /var/www/html/weather/raw 

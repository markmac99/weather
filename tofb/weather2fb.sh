#!/bin/bash
python -m pywws.Template /home/pi/weather/data /home/pi/weather/templates/tweet.txt /tmp/tweet.txt
python tofb.py
rm -f /tmp/tweet.txt

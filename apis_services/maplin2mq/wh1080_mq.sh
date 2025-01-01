#!/bin/bash
here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here
source /home/pi/venvs/pywws/bin/activate
weatherdir=/home/pi/weather
rm -f $weatherdir/stopwhfwd
python $here/wh1080_mq.py $weatherdir/maplinstn/weatherdata.json $weatherdir

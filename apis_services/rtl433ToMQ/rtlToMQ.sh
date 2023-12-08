#!/bin/bash
here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here
source /home/pi/venvs/pywws/bin/activate
weatherdir=/home/pi/weather
rm -f $weatherdir/stopwhfwd
find $weatherdir/logs -name "WH1080Fwd*.log" -mtime +14 -exec rm -f {} \;
python $here/rtl43ToMQ.py $weatherdir/maplinstn/weatherdata.json $weatherdir

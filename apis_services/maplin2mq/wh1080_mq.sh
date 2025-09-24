#!/bin/bash
here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here
source /home/pi/venvs/pywws/bin/activate
datadir=/home/pi/weather/maplinstn
rm -f $datadir/stopwhfwd
python $here/wh1080_mq.py $datadir /home/pi/weather/logs

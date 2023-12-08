#!/bin/bash

# copyright Mark McIntyre, 2023-

here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here

weatherdir=/home/pi/weather

source /home/pi/venvs/pywws/bin/activate
rm -f $weatherdir/stopbmp280
if [ ! -f $weatherdir/maplinstn/bmp280.json.$(date +%Y%m%d) ] ; then
    mv $weatherdir/maplinstn/bmp280.json $weatherdir/maplinstn/bmp280.json.$(date +%Y%m%d)
fi
find $datadir -name "bmp280-*.log" -mtime +14 -exec rm -f {} \;
find $datadir -name "bmp280.json.*" -mtime +14 -exec rm -f {} \;
python $here/readBmp280.py $weatherdir

#!/bin/bash

# copyright Mark McIntyre, 2023-

here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here

weatherdir=WEATHERDIR

source /home/pi/venvs/pywws/bin/activate
rm -f $weatherdir/stopbmp280
yday=$(date --date yesterday +%Y%m%d)
if [ ! -f $weatherdir/maplinstn/bmp280.json.${yday} ] ; then
    mv $weatherdir/maplinstn/bmp280.json $weatherdir/maplinstn/bmp280.json.${yday}
fi
python $here/readBmp280.py $weatherdir

#!/bin/bash

# copyright Mark McIntyre, 2023-

here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here

weatherdir=WEATHERDIR

source /home/pi/venvs/pywws/bin/activate
rm -f /tmp/stopbmp280
python $here/readBmp280.py $weatherdir

#!/bin/bash
# copyright Mark McIntyre, 2023

here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here
source /home/pi/venvs/pywws/bin/activate
rm -f /tmp/stopwhfwd
python $here/maplintomq.py

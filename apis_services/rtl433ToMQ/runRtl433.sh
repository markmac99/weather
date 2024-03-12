#!/bin/bash
here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here
datadir=/home/pi/weather/maplinstn
logdir=/home/pi/weather/logs
mkdir -p $datadir
mkdir -p $logdir

if [ ! -f $datadir/weatherdata.json.$(date +%Y%m%d) ] ; then
    mv $datadir/weatherdata.json $datadir/weatherdata.json.$(date +%Y%m%d)
fi
find $datadir -name "weatherdata.json*" -mtime +365 -exec rm -f {} \;
/usr/local/bin/rtl_433 -R 32 -R 155 -F json::$datadir/weatherdata.json

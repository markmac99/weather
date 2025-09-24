#!/bin/bash
here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here
datadir=/home/pi/weather/maplinstn
logdir=/home/pi/weather/logs
mkdir -p $datadir
mkdir -p $logdir

yday=$(date --date yesterday +%Y%m%d)
if [ ! -f $datadir/weatherdata.json.${yday} ] ; then
    mv $datadir/weatherdata.json $datadir/weatherdata.json.${yday}
fi
#/usr/local/bin/rtl_433 -R 32 -R 155 -F json::$datadir/weatherdata.json -M time:utc
/usr/local/bin/rtl_433  -c /etc/rtl_433/rtl_433.conf
#!/bin/bash

# copyright Mark McIntyre, 2023-

# install cronjob to copy data for pywws

here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here
appname=whToAws.sh

if [ "$(crontab -l | grep $appname)" == "" ] ; then 
    echo "installing cron job"
    (crontab -l && echo "* * * * * $here/$appname > $HOME/weather/logs/whtoaws.log 2>&1" ) | crontab -
else
    echo "nothing to install"
fi

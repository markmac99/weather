#!/bin/bash

# copyright Mark McIntyre, 2023-

# install cronjob to copy data for pywws

here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here
appname=whtoaws

sudo cp $appname.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable $appname
sudo systemctl start $appname

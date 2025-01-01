#!/bin/bash

# copyright Mark McIntyre, 2023-

# install service to read from my WH1080 / Maplin weatherstation outdoor sensors
# and republish on MQ, with some additional derived data

here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here

sudo cp wh1080_rtl433.service /etc/systemd/system/
sudo cp rtl-sdr.rules /etc/udev/rules.d/
sudo systemctl enable wh1080_rtl433
sudo systemctl daemon-reload
sudo systemctl start wh1080_rtl433

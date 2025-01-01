#!/bin/bash

# copyright Mark McIntyre, 2023-

# install service to republish the WH1080 data on MQ, with some additional derived data

here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here

sudo systemctl stop rtl2mq
sudo systemctl disable rtl2mq
sudo rm /etc/systemd/system/rtl2mq.service
sudo cp maplin2mq.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable maplin2mq
sudo systemctl start maplin2mq

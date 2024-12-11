#!/bin/bash
here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here
source $HOME/venvs/openhabstuff/bin/activate

sudo systemctl stop getweatherdata
sudo systemctl status getweatherdata
sleep 30
sudo reboot
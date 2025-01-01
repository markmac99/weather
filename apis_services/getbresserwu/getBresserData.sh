#!/bin/bash
here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here
source HOMEDIR/venvs/pywws/bin/activate
export LOGDIR=HOMEDIR/weather/logs
python getwu.py

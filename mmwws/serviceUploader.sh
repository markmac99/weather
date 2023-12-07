#!/bin/bash
here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here
source $HOME/venvs/openhabstuff/bin/activate
active=$(ps -ef | grep sendToServices | grep -v grep | awk '{print $2}')
if [ "$active" == "" ] ; then 
    python $here/sendToServices.py $HOME/weather/data
fi

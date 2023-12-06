#!/bin/bash
here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here
source $HOME/venvs/openhabstuff/bin/activate
active=$(ps -ef | grep createWsFiles | grep -v grep | awk '{print $2}')
if [ "$active" == "" ] ; then 
    python $here/createWsFiles.py $HOME/weather/data
fi

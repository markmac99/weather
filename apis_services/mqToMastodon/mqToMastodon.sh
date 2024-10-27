#!/bin/bash

# simple script to push Weather reports to mastodon

here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
source ~/venvs/pywws/bin/activate

cd $here
python ./postWeather.py 
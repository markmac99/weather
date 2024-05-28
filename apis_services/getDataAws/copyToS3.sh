#!/bin/bash
here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here
source $HOME/venvs/openhabstuff/bin/activate

# done here rather than in python because Parquet rewrites every file every time
# it saves, and so we would have tens of thousands of writes per day, driving up cost
# unacceptably

cd ~/weather/raw
aws s3 sync . s3://mjmm-weatherdata --no-progress --size-only

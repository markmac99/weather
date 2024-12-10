#!/bin/bash
here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here
source $HOME/venvs/openhabstuff/bin/activate

# done here rather than in python because Parquet rewrites every file every time
# it saves, and so we would have tens of thousands of writes per day, driving up cost
# unacceptably

cd ~/weather/raw

# check parquet file isn't corrupted
yr=$(date +%Y)
python -c "import pandas as pd;df=pd.read_parquet('raw-2023.parquet')"
if [ $? == 0 ] ; then 
    aws s3 sync . s3://mjmm-weatherdata --no-progress --size-only
else
    echo "parquet file unreadable"
fi

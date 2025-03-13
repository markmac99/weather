#!/bin/bash
here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here
source $HOME/venvs/openhabstuff/bin/activate

# done here rather than in python because Parquet rewrites every file every time
# it saves, and so we would have tens of thousands of writes per day, driving up cost
# unacceptably

datadir=~/weather/raw

# check parquet file isn't corrupted or being written to
yr=$(date +%Y)
python << EOD
import pandas as pd
from time import sleep
import os
loopctr=0
while loopctr < 5:
    try:
        df=pd.read_parquet(os.path.expanduser('${datadir}/raw-${yr}.parquet'))
        exit(0)
    except Exception:
        sleep(6)
        loopctr +=1
exit(1)
EOD
if [ $? == 0 ] ; then 
    echo "backing up to S3"
    sudo systemctl stop getweatherdata    
    aws s3 sync ${datadir} s3://mjmm-weatherdata  --size-only
    sudo systemctl start getweatherdata
else
    echo "parquet file unreadable"
    python $here/sendAnEmail.py markmcintyre99@googlemail.com "weather parquet file unreadable" "alert from weather" weather@wordpresssite
fi

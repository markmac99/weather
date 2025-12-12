#!/bin/bash

source ~/vAWS/bin/activate

logger -s -t pushtoaws creating index file
baseurl=https://d3jdcxriig76vh.cloudfront.net/satdata

idxfile=/tmp/satindex.js

echo "\$(function() {" > $idxfile
echo "var table = document.createElement(\"table\");" >> $idxfile
echo "table.className = \"table table-striped table-bordered table-hover table-condensed\";" >> $idxfile
echo "var header = table.createTHead(); " >> $idxfile
echo "header.className = \"h4\"; " >> $idxfile

echo "var row = table.insertRow(-1);" >> $idxfile
i=0
ls /srv/images/thumb/*web* -1t | head -20 | while read img ; do
    if [ $i -eq 5 ] ; then
        echo "var row = table.insertRow(-1);" >> $idxfile
        i=0
    fi
    echo "var cell = row.insertCell(-1);" >> $idxfile
    baseimg=$(basename $img)
    thumbfile=${baseurl}/thumb/$baseimg
    nameroot=${baseimg:0:28}
    if compgen -G "/srv/images/${nameroot}equidistant_67_composite.jpg" > /dev/null ; then 
        targfile=${baseurl}/${nameroot}equidistant_67_composite.jpg
    elif compgen -G "/srv/images/${nameroot}spread_67.jpg" > /dev/null ; then 
        targfile=${baseurl}/${nameroot}spread_67.jpg
    else
        targfile=${baseurl}/${nameroot}equidistant_67.jpg
    fi
    compfile=${baseurl}/${nameroot}
    echo "cell.innerHTML = \"\\<a href=$targfile\\>\\<img src=$thumbfile width=100\\%\>\\</a\\>\";" >> $idxfile
    i=$((i+1))
done 

echo "var outer_div = document.getElementById(\"img-list\");"   >> $idxfile
echo "outer_div.appendChild(table);"  >> $idxfile
echo "})"  >> $idxfile

logger -s -t pushtoaws copying to server
scp -i ~/.ssh/markskey.pem /tmp/satindex.js bitnami@wordpresssite:data/mjmm-data/satdata/
logger -s -t pushtoaws done

logger -s -t pushtoaws syncing files to AWS
/usr/local/bin/aws s3 sync /srv/images s3://mjmm-data/satdata/
logger -s -t pushtoaws done

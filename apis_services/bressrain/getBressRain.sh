#!/bin/bash
here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here

lhr=-1
lval=0
[ -f ./lastdata.txt ] &&  source ./lastdata.txt

hr=$(date +%H)
val=$(mosquitto_sub -h wxsatpi -t sensors/rtl_433/P172/C0/rain_mm -i readrain -C 1)
diff=$(echo "$val $lval" | awk '{print $1-$2}')

if [ $hr != $lhr ] ; then
    echo "hr=$hr" > ./lastdata.txt
    echo "val=$val" >> ./lastdata.txt
fi 
[ $lval == 0 ] && diff=0
mosquitto_pub -h wxsatpi -t weather/bresser/rain_hourly_mm -m $diff -q 1 -i rainrate
ts=$(date +%Y-%m-%dT%H:%M:%SZ)
mosquitto_pub -h wxsatpi -t weather/bresser/time -m $ts -q 1 -i rainrate
echo $(date) "posted $diff"
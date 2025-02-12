#!/bin/bash

# simple script to check the various weather services and APIs

svcs="getbresswu bmp280 maplin2mq wh1080_rtl433 bressrain.timer bressrain.service"
for svc in $svcs
do 
    systemctl status $svc | grep Started
    if [ $? != 0 ] ; then 
        echo $svc not running
    fi 
done

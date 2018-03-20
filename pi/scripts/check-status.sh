#!/bin/bash
df -H | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{ print $5 " " $1 }' | while read output;
do
  echo $output
  usep=$(echo $output | awk '{ print $1}' | cut -d'%' -f1  )
  partition=$(echo $output | awk '{ print $2 }' )
  if [ $usep -ge 90 ]; then
    echo "Running out of space \"$partition ($usep%)\" on $(hostname) as on $(date)" |
     mail -s "Alert: Almost out of disk space $usep%" mark.jm.mcintyre@cesmail.net
  fi
done

tail -20 /home/pi/log/weather.log | grep error | while read i ;
do 
  echo $i;
    echo "piwws error $i on $(hostname) as on $(date)" |
     mail -s "Alert: piwws error" mark.jm.mcintyre@cesmail.net
done

#!/bin/bash
RECP=mark@themcintyres.dnsalias.net

df -H | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{ print $5 " " $1 }' | while read output;
do
  echo $output
  usep=$(echo $output | awk '{ print $1}' | cut -d'%' -f1  )
  partition=$(echo $output | awk '{ print $2 }' )
  if [ $usep -ge 90 ]; then
    echo "Running out of space \"$partition ($usep%)\" on $(hostname) as on $(date)" |
     mail -s "Alert: Almost out of disk space $usep%" $RECP
  fi
done

tail -20 /home/pi/log/livelog.log | grep error | while read i ;
do 
  echo $i;
    echo "piwws error $i on $(hostname) as on $(date)" |
     mail -s "Alert - piwws error" -r pi@weatherstation $RECP
done

pgrep livelog
if [ $? -ne 0 ]
then
    echo "piwws livelog not running on $(hostname) on $(date)" |
     mail -s "Alert: piwws error" $RECP
fi



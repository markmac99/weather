#!/bin/sh
export PATH=$PATH:/usr/local/bin
# exit if NTP hasn't set computer clock
#[ `ntpdc -c sysinfo | awk '/stratum:/ {print $2}'` -ge 10 ] && exit
pidfile=/var/run/pywws.pid
datadir=/home/pi/weather/data
logfile=/home/pi/log/livelog.log
# exit if process is running
[ -f $pidfile ] && kill -0 `cat $pidfile` && exit
# email last few lines of the logfile to see why it died
if [ -f $logfile ]; then
log=/tmp/log-weather
tail -40 $logfile >$log
~pi/weather/scripts/email-log.sh $log "weather log"
#rm $log
fi
# restart process
pywws-livelog-daemon -v -p $pidfile $datadir $logfile start


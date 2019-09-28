c:\cygwin\bin\rsync -e 'c:\cygwin\bin\ssh -i /home/mark/.ssh/raspberry-pi' -avz pi@raspberrypi:weather/* pi
c:\cygwin\bin\rsync -e 'c:\cygwin\bin\ssh -i /home/mark/.ssh/mark.pem' -avz weather@thelinux:/var/www/html/weather/* website
echo done
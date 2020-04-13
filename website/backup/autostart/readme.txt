Copy pywws.service to /etc/systemd/system/
copy *weather* to /etc/udev/rules.d/
check files have correct userid, path to livelog
reboot server
test
ps -ef | grep livelog
service pywws status


#!/bin/sh

mailx -s $2 -r weather@raspberrypi  mark@themcintyres.dnsalias.net < $1


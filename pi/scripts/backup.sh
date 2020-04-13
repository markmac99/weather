#!/bin/bash
cd /home/pi
tar cvfz weather-`date +%Y%m%d`.tgz weather/*
aws s3 cp weather-`date +%Y%m%d`.tgz s3://mjmm-website-backups
rm  weather-`date +%Y%m%d`.tgz

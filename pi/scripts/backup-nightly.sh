#!/bin/bash

cd /home/pi
aws s3 sync weather s3://mjmm-website-backups/weatherstation/
